"""
=========================================================
AI Smart Building Optimization System

Application Entry Point
=========================================================
"""

import uvicorn

from config import HOST, PORT


def main():
    """
    Starts the FastAPI server.
    """

    uvicorn.run(
        "backend.app:app",
        host=HOST,
        port=PORT,
        reload=True
    )


if __name__ == "__main__":
    main()