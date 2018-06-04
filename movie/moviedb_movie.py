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

# title           :MovieDB_Movie.py
# description     :MovieDBMovie object definition
# author          :Eric Kimsey
# usage           :
# notes           :
# python_version  :3.5+
# =======================================================================

import logger
from movie import moviedb_genre


class MovieDBMovie:

    def __init__(self, title: str, movie_db_id: int, description: str, release_date: str,
                 poster_url: str, genre_ids: str = None, imdb_id: str = None):
        """
        Create MovieDBMovie object.
        :param str title: Title of the movie
        :param int movie_db_id: MovieDB ID number of the movie
        :param str description: Description of the movie
        :param str release_date: Release date of the movie in the form: YYYY-MM-DD
        :param str poster_url: Poster URL
        :param str genre_ids: String list of genre ID's in the form: NN,NN,NNN,...
        :param str imdb_id: IMDB ID tag of the movie in the form: ttNNNNNNN
        """
        title = title.replace('\\xe2\\x80\\x94', '-')
        self.title = title
        self.movie_db_id = int(movie_db_id)
        description = description.replace('\\xe2\\x80\\x94', '-')
        self.description = description
        self.release_date = release_date
        self.poster_url = poster_url
        self.genre_ids = genre_ids
        self.imdb_id = imdb_id

    def __str__(self) -> str:
        """
        Create string representation of this MovieDB object.
        :return str: String representation of the moviedb_movie object
        """
        str_rep = ''

        # Title
        str_rep += self.title

        # Release date
        if self.release_date is not None and self.release_date != '':
            str_rep += ' (' + self.release_date + ')'

        # Genres
        if self.genre_ids is not None and self.genre_ids != '':
            str_rep += '\n'
            written = False
            for genre_num in self.genre_ids.split(','):
                movie_genre = moviedb_genre.GENRE_DICT[genre_num]
                if movie_genre is Exception:
                    logger.log_message(0, str(movie_genre))
                else:
                    str_rep += movie_genre + ", "
                    written = True
            if written:
                str_rep = str_rep[:-2]

        # IMDB ID
        if self.imdb_id is not None and self.imdb_id != '':
            str_rep += '\nIMDB: ' + self.imdb_id + '\t'
            # MovieDB ID
            str_rep += 'MovieDB: ' + str(self.movie_db_id)
        else:
            str_rep += '\nMovieDB: ' + str(self.movie_db_id)

        # Poster URL
        if self.poster_url is not None and self.poster_url != '':
            str_rep += '\nPoster: ' + self.poster_url

        # Description
        if self.description is not None and self.description != '':
            str_rep += '\n' + self.description

        return str_rep

    def __add__(self, other: str) -> str:
        """
        Concatenate MovieDB string representation with another string.
        :param str other: String to concatenate with the movie
        :return str: String representation of the movie concatenated with the other object
        """
        return str(self) + str(other)

    def __radd__(self, other: str) -> str:
        """
        Concatenate MovieDB string representation with another string.
        :param str other: String to concatenate the movie to
        :return str: String representation of the other object concatenated with the movie
        """
        return str(other) + str(self)
