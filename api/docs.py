model_responses = {
    400: {
        "description": "Invalid ...",  # Fill here
        "content": {
            "application/json": {
                "example": {
                    "message": "Invalid ...",  # Fill here
                }
            }
        },
    },
    404: {
        "description": "... not found",  # Fill here
        "content": {
            "application/json": {"example": {"message": "... not found"}}
        },  # Fill here
    },
    200: {
        "description": "... found.",  # Fill here
        "content": {
            "application/json": {
                "example": {
                    # Fill here
                    "...": "....",
                    ".....": "......",
                    "#": {
                        "##": "###",
                        "####": "#####",
                    },
                },
            },
        },
    },
}
