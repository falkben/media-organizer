import os
import sys
from typing import Optional, Type

from rich.console import Console
from rich.pretty import Pretty
from rich.traceback import Traceback
from sqlmodel import Session
from textual.app import App
from textual.driver import Driver
from textual.widgets import DirectoryTree, FileClick, Footer, Header, ScrollView
from tmdb_interface import get_movie_from_path


class MyApp(App):
    """An example of a very simple Textual App
    based on: https://github.com/willmcgugan/textual/blob/main/examples/code_viewer.py
    """

    def __init__(
        self,
        console: Optional[Console] = None,
        screen: bool = True,
        driver_class: Optional[Type[Driver]] = None,
        log: str = "",
        log_verbosity: int = 1,
        title: str = "Textual Application",
        path: str = None,
        session: Optional[Session] = None,
    ):
        self.path = path
        self.session = session
        super().__init__(
            console=console,
            screen=screen,
            driver_class=driver_class,
            log=log,
            log_verbosity=log_verbosity,
            title=title,
        )

    async def on_load(self) -> None:
        """Sent before going in to application mode."""

        # Bind our basic keys
        await self.bind("b", "view.toggle('sidebar')", "Toggle sidebar")
        await self.bind("q", "quit", "Quit")

        # Get path to show
        if not self.path:
            try:
                self.path = sys.argv[1]
            except IndexError:
                self.path = os.path.abspath(
                    os.path.join(os.path.basename(__file__), "../../")
                )

    async def on_mount(self) -> None:
        """Call after terminal goes in to application mode"""

        # Create our widgets
        # In this a scroll view for the code and a directory tree
        self.body = ScrollView()
        self.directory = DirectoryTree(self.path, "Movies")

        # Dock our widgets
        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")

        # Note the directory is also in a scroll view
        await self.view.dock(
            ScrollView(self.directory), edge="left", size=48, name="sidebar"
        )
        await self.view.dock(self.body, edge="top")

    async def handle_file_click(self, message: FileClick) -> None:
        """A message sent by the directory tree when a file is clicked."""

        self.app.sub_title = os.path.basename(message.path)
        movie = get_movie_from_path(message.path, self.session)
        if movie:
            try:
                movie_data = Pretty(movie)
            except Exception:
                movie_data = Traceback(width=None, show_locals=True)
            await self.body.update(movie_data)
        else:
            await self.body.update(f"not found: {message.path}")


if __name__ == "__main__":
    # Run our app class
    MyApp.run(title="Media Organizer", log="textual.log")
