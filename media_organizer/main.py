import os
from pathlib import Path

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

from media_organizer import MyApp

load_dotenv()

MOVIES_PATH = Path(os.getenv("MOVIES_FILEPATH", None))


def main():
    engine = create_engine("sqlite:///database.db", echo=False)
    with Session(engine) as session:
        MyApp.run(
            title="Media Organizer",
            log="textual.log",
            path=str(MOVIES_PATH.absolute()),
            session=session,
        )


if __name__ == "__main__":
    main()
