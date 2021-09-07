import os
from pathlib import Path

from app import MyApp
from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

MOVIES_PATH = Path(os.getenv("MOVIES_FILEPATH", None))

dbfile = Path("database.db")
engine = create_engine("sqlite:///database.db", echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def main():
    if not dbfile.exists():
        create_db_and_tables()

    with Session(engine) as session:
        MyApp.run(
            title="Media Organizer",
            log="textual.log",
            path=str(MOVIES_PATH.absolute()),
            session=session,
        )


if __name__ == "__main__":
    main()
