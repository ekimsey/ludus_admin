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

# title           :librarydb_movie.py
# description     :LibraryDBMovie object definition
# author          :Eric Kimsey
# usage           :
# notes           :
# python_version  :3.5+
# =======================================================================

from logger import logger
from movie import moviedb_genre
from movie import librarydb_format
from movie import librarydb_status
from movie.moviedb_movie import MovieDBMovie


class LibraryDBMovie(MovieDBMovie):

    def __init__(self, title: str, movie_db_id: int, title_format: int, title_status: int = 1, imdb_id: str = None,
                 genre_ids: str = None, description: str = None, release_date: str = None,
                 poster_url: str = None, title_id: int = None):
        """
        Create LibraryDBMovie object.
        :param str title: Title of the movie
        :param int movie_db_id: MovieDB ID number of the movie
        :param int title_format: Format ID of the movie
        :param int title_status: Status ID of the movie
        :param str imdb_id: IMDB ID tag of the movie in the form: ttNNNNNNN
        :param str genre_ids: String list of genre ID's in the form: NN,NN,NNN,...
        :param str description: Description of the movie
        :param str release_date: Release date of the movie in the form: YYYY-MM-DD
        :param str poster_url: Poster URL
        :param int title_id: LibraryDB primary key for this movie. Not to be manually entered!
        """
        super().__init__(title, movie_db_id, description, release_date, poster_url, genre_ids, imdb_id)
        self.title_format = int(title_format)
        self.title_status = int(title_status)
        self.title_id = title_id

    def __str__(self) -> str:
        """
        Convert LibraryDB_Movie object into a string.
        :return str: String representation of the LibraryDB_Movie object
        """
        str_rep = ''

        # Title
        str_rep += self.title

        # Release date
        if self.release_date is not None and self.release_date != '':
            str_rep += ' (' + self.release_date + ')'

        # Format
        try:
            format_name = librarydb_format.FORMAT_DICT[str(self.title_format)]
            str_rep += ' - ' + format_name
        except KeyError as err:
            logger.log_message(0, str(err))

        # Status
        try:
            status_name = librarydb_status.STATUS_DICT[str(self.title_status)]
            str_rep += '\nStatus: ' + status_name
        except KeyError as err:
            logger.log_message(0, str(err))

        # Genres
        if self.genre_ids is not None and self.genre_ids != '':
            str_rep += '\n'
            written = False
            for genre_num in self.genre_ids.split(','):
                movie_genre = moviedb_genre.GENRE_DICT[genre_num]
                if movie_genre is Exception:
                    logger.log_message(0, movie_genre)
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
