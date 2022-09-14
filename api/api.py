from bs4 import BeautifulSoup as bs
from dotenv import dotenv_values
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from http import HTTPStatus
from pydantic import BaseModel
from starlette.responses import RedirectResponse
import docs
import httpx
import os
import utils
import uvicorn

CONFIG = dict(dotenv_values(".env") or dotenv_values(".env.example"))
if not CONFIG:
    CONFIG = {
        "backlog": os.getenv("backlog", 2048),
        "debug": os.getenv("debug", False),
        "host": os.getenv("host", "0.0.0.0"),
        "log_level": os.getenv("log_level", "trace"),
        "port": os.getenv("port", 8080),
        "reload": os.getenv("reload", True),
        "timeout_keep_alive": os.getenv("timeout_keep_alive", 5),
        "workers": os.getenv("workers", 4),
    }
CONFIG = utils.check_config(CONFIG)
api = FastAPI()


class Game(BaseModel):
    """Model for the Game Information."""

    game: str
    information: dict
    offers: dict


@api.get("/", include_in_schema=False)
async def root():
    """Redirects to the documentation."""
    return RedirectResponse(url="/docs")


async def request_treatment(url: str, simple: bool = False) -> JSONResponse:
    """Makes an async request and treats the data.

    Args:
        url (str): URL to make the asynchronous request to.

    Returns:
        JSONResponse: JSON Response with the status code and the content of the response.
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, follow_redirects=True, timeout=2)
        if resp.status_code != 200:
            status_code = resp.status_code
            detail = HTTPStatus(status_code).phrase
            return JSONResponse(status_code=status_code, content={"detail": detail})
        soup = bs(resp.text)
        csv = utils.extract_data(soup, simple)
        return JSONResponse(status_code=HTTPStatus.OK, content=csv)


@api.get("/myendpoint", response_model=utils.Model, responses=docs.model_responses)
async def get() -> JSONResponse:
    """Checks the ..."""
    url = "https://www.myurl.com/"
    return await request_treatment(url)


def start() -> None:
    """Starts the Uvicorn server with the provided configuration."""
    uviconfig = {"app": "api:api", "interface": "asgi3"}
    uviconfig |= CONFIG
    try:
        uvicorn.run(**uviconfig)
    except Exception as e:
        print("Unable to run server.", e)


if __name__ == "__main__":
    start()
