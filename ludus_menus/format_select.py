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

# title           :format_select.py
# description     :FormatSelect class definitions.
# author          :Eric Kimsey
# usage           :
# notes           :
# python_version  :3.5+
# =======================================================================

import globals
from menu_system.menu_types.option_select import OptionSelect
from movie import librarydb_format
from movie.librarydb_movie import LibraryDBMovie


class FormatSelect(OptionSelect):
    TITLE = 'Movie Format Selection'

    def __init__(self, movie):
        """
        Create FormatSelect menu.
        :param MovieDBMovie movie: MovieDBMovie to which a format needs assigned
        """
        prompt = 'Format # of this movie: '
        options = librarydb_format.FORMAT_DICT
        special_options = {
            'B': 'Back',
            'Q': 'Exit'
        }
        super().__init__(globals.VERSION + ' - ' + self.TITLE, prompt, options, special_options)
        self._movie = movie

    def process_input(self, entry: str) -> tuple:
        """
        Handle all option and special option actions.
        :param str entry: User's input
        :return tuple: True = Success or False = Fail, LibraryDBMovie object
        """
        if entry.upper() == 'B':
            return False, ''
        elif entry.upper() == 'Q':
            quit()
        else:
            librarydb_movie = LibraryDBMovie(self._movie.title,
                                             self._movie.movie_db_id,
                                             int(entry),
                                             1,
                                             self._movie.imdb_id,
                                             self._movie.genre_ids,
                                             self._movie.description,
                                             self._movie.release_date,
                                             self._movie.poster_url)
            return True, librarydb_movie
