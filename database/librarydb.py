#!/usr/bin/python3

"""
Ludus Admin is a shell interface for Ludus movie library administration.
Copyright (C) 2018  Eric Kimsey

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# title           :librarydb.py
# description     :Library database interface.
# author          :Eric Kimsey
# usage           :
# notes           :
# python_version  :3.5+
# =======================================================================

import sqlite3
import logger
import globals
from movie.librarydb_movie import LibraryDBMovie


def insert_movie(movie: LibraryDBMovie) -> tuple:
    """
    Insert movie object into LibraryDB.
    :param LibraryDB_Movie movie: LibraryDB_Movie to be inserted into LibraryDB
    :return tuple: Status code. True = Success or False = Error, string description of status
    """
    conn = sqlite3.connect(globals.LIBRARYDB_PATH)
    try:
        c = conn.cursor()
        c.execute(
            'INSERT INTO Titles (name, movie_db_id, imdb_id, genres, description, release_date, format, posterUrl) '
            + 'VALUES (?,?,?,?,?,?,?,?)',
            (movie.title, movie.movie_db_id, movie.imdb_id, movie.genre_ids,
             movie.description, movie.release_date, movie.title_format, movie.poster_url))

        conn.commit()
        conn.close()
    except Exception as err:
        conn.commit()
        conn.close()
        logger.log_message(0, str(err))
        return False, "INSERT ERROR: Check logs for details! "

    return True, 'Successful LibraryDB Insert!'


def update_movie(movie: LibraryDBMovie) -> tuple:
    """
    Update movie object in LibraryDB.
    :param LibraryDB_Movie movie: LibraryDB_Movie to be updated in LibraryDB
    :return tuple: Status code. True = Success or False = Error, string description of status
    """
    conn = sqlite3.connect(globals.LIBRARYDB_PATH)
    try:
        c = conn.cursor()
        # UPDATE table_name SET column1 = value1, column2 = value2...., columnN = valueN WHERE [condition];
        c.execute(
            'UPDATE Titles SET name = ?, movie_db_id = ?, imdb_id = ?, genres = ?, description = ?, release_date = ?, '
            + 'format = ?, posterUrl = ? WHERE title_id = ?',
            (movie.title, movie.movie_db_id, movie.imdb_id, movie.genre_ids,
             movie.description, movie.release_date, movie.title_format, movie.poster_url, movie.title_id))

        conn.commit()
        conn.close()
    except Exception as err:
        conn.commit()
        conn.close()
        logger.log_message(0, str(err))
        return False, "UPDATE ERROR: Check logs for details! "

    return True, 'Successful LibraryDB Update!'


def search_by_title(entry: str) -> tuple:
    """
    Query LibraryDB's movie titles for the search term.
    :param str entry: Search term
    :return tuple: True = Success or False = Error, List of LibraryDB movies
    """
    try:
        conn = sqlite3.connect(globals.LIBRARYDB_PATH)
        c = conn.cursor()

        t = ('%' + entry + '%',)
        c.execute('SELECT * FROM Titles WHERE name LIKE ?', t)

        movies = []
        while True:
            result = c.fetchone()
            if result is None:
                break
            else:
                movie = LibraryDBMovie(result[1],  # title
                                       result[2],  # movie_db_id
                                       result[7],  # title_format
                                       result[9],  # title_status
                                       result[3],  # imdb_id
                                       result[4],  # genre_ids
                                       result[5],  # description
                                       result[6],  # release_date
                                       result[8],  # poster_url
                                       result[0])  # title_id
                movies.append(movie)

        conn.commit()
        conn.close()
    except Exception as err:
        logger.log_message(0, str(err))
        return False, 'ERROR: Check logs. '

    return True, movies


def search_by_text(entry: str) -> tuple:
    """
    Query LibraryDB's text fields (title and description) for the search term.
    :param str entry: Search term
    :return tuple: True = Success or False = Error, List of LibraryDB movies
    """
    try:
        conn = sqlite3.connect(globals.LIBRARYDB_PATH)
        c = conn.cursor()

        t = ('%' + entry + '%',)
        c.execute('SELECT * FROM Titles WHERE name or description LIKE ?', t)

        movies = []
        while True:
            result = c.fetchone()
            if result is None:
                break
            else:
                movie = LibraryDBMovie(result[1],  # title
                                       result[2],  # movie_db_id
                                       result[7],  # title_format
                                       result[9],  # title_status
                                       result[3],  # imdb_id
                                       result[4],  # genre_ids
                                       result[5],  # description
                                       result[6],  # release_date
                                       result[8],  # poster_url
                                       result[0])  # title_id
                movies.append(movie)

        conn.commit()
        conn.close()
    except Exception as err:
        logger.log_message(0, str(err))
        return False, 'ERROR: Check logs. '

    return True, movies
