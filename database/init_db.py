"""
=========================================================
Initialize Database
=========================================================
"""

from database.base import Base
from database.database import engine

# Import models
from database import models


def create_database():

    Base.metadata.create_all(bind=engine)

    print("Database Created Successfully")


if __name__ == "__main__":

    create_database()