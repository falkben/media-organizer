# media-organizer

terminal app for media and metadata organization

## install

[Get poetry](https://python-poetry.org/docs/#installation)

Then:

```command
poetry install
```

## run

```command
poetry run python media_organizer/main.py
```

## API Key for TMDB

1. Register for and verify an [account](https://www.themoviedb.org/account/signup).
2. [Log into](https://www.themoviedb.org/login) your account.
3. Select the [API section](https://www.themoviedb.org/settings/api) on account settings.
4. Click on the link to generate a new API key and follow the instructions.

Copy the `.env.example` into a new `.env` file

Edit the new file and enter your API token.

## Add media path to env file

Edit the `.env` file to add the full path to your media files

## Test

run the example to ensure the environment and API token has been set up correctly

```cmd
$ python example.py
Movie title: The Matrix
```

## Examples

Reads an example movie into a load database file (`database.db`)

```cmd
python examples/load_into_db.py
```
