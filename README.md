# Ludus Admin
A shell interface for the administration of the Ludus personal movie cataloging system, written in Python 3.

## Required
[Python 3.5 or newer](https://www.python.org/)<br />
[Ludus](https://gitlab.com/ekimsey/ludus)

## Usage
1. Ludus must be running on the same machine as Ludus Admin in order to administrate the database in real time. Another approach is to keep a copy of your movie library database file on your Ludus server as well as with your Ludus Admin project, then copy the database file to your Ludus server after making changes to the database using Ludus Admin.
2. Obtain a developer API key from the [The Movie Database](https://www.themoviedb.org/). This is necessary to be able to perform any searches of The Movie Database, scraping of movie data from The Movie Database. This API key is integral to the operation of Ludus Admin. Details on how to obtain an API key can be found under The Movie Database's API FAQ. Create a text file in the root of the Ludus Admin project called "*api_key.txt*" and place your API key on the first line of the file followed by a newline.
3. Change *globals.py* to point to your movie database. Change LIBRARYDB_PATH to the path of your database. Example: `LIBRARYDB_PATH = '../my_db/MovieLibrary.db'`
4. Start Ludus Admin with: `./ludus_admin.py` or `python ludus_admin.py`
