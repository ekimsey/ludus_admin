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

# title           :param_edit.py
# description     :ParamEdit menu class definition.
# author          :Eric Kimsey
# usage           :
# notes           :
# python_version  :3.5+
# =======================================================================

import re
import globals
from logger import logger
from menu_system.menu_types.text_entry import TextEntry
from movie import librarydb_format
from movie import moviedb_genre


class ParamEdit(TextEntry):
    TITLE = 'Movie Parameter Edit'

    def __init__(self, curr_val: tuple):
        """
        Create ParamEdit menu.
        :param tuple curr_val: parameter name, parameter value
        """
        prompt = 'New value: '
        special_options = {
            'B': 'Back',
            'Q': 'Exit'
        }
        self._param_name = curr_val[0]
        self._param_value = curr_val[1]
        add_message = curr_val[0] + ': ' + str(curr_val[1])
        if self._param_name == 'format':
            add_message = add_message + '\n\nValid format numbers:\n'
            for format_num in librarydb_format.FORMAT_DICT.keys():
                add_message = add_message + format_num + ':\t' + librarydb_format.FORMAT_DICT[format_num] + '\t\t'
            add_message = add_message[:-1]
        elif self._param_name == 'genres':
            add_message = add_message + '\n\nValid genre id numbers:\n'
            i = 0
            for genre_num in moviedb_genre.GENRE_DICT.keys():
                if len(genre_num) < 3:
                    add_message = add_message + genre_num + ':\t\t'
                else:
                    add_message = add_message + genre_num + ':\t'
                add_message = add_message + moviedb_genre.GENRE_DICT[genre_num]
                if len(moviedb_genre.GENRE_DICT[genre_num]) > 9:
                    add_message = add_message + '\t'
                elif 3 < len(moviedb_genre.GENRE_DICT[genre_num]) < 8:
                    add_message = add_message + '\t\t\t'
                elif len(moviedb_genre.GENRE_DICT[genre_num]) < 4:
                    add_message = add_message + '\t\t\t\t'
                else:
                    add_message = add_message + '\t\t'
                i = i + 1
                if i == 3:
                    add_message = add_message + '\n'
                    i = 0
            add_message = add_message[:-1]
        super().__init__(globals.VERSION + ' - ' + self.TITLE, prompt, special_options, add_message)

    def process_input(self, entry: str) -> tuple:
        """
        Handle all option and special option actions.
        :param str entry: User's input
        :return tuple: True = Success or False = Fail, new value of parameter or status message
        """
        if entry.upper() == 'B':
            return False, ''
        elif entry.upper() == 'Q':
            quit()
        # Check input validity
        # Check if key is in menu
        if self._param_name == 'format' or self._param_name == 'movie_db_id':
            try:
                entry = int(entry)
            except Exception as err:
                logger.log_message(0, str(err))
                self.val_input = False
                return False, self._param_name + ' is not int! '

            if self._param_name == 'format':
                try:
                    librarydb_format.FORMAT_DICT[str(entry)]
                except KeyError:
                    logger.log_message(0, 'Format not valid! ' + str(entry))
                    self.val_input = False
                    return False, 'Format entered is not valid! '
                # Add to movie object
                return True, str(entry)

            elif self._param_name == 'movie_db_id':
                # No special criteria, add to movie object
                return True, entry
        elif self._param_name == 'imdb_id' or self._param_name == 'genres' or self._param_name == 'release_date' \
                or self._param_name == 'posterUrl' or self._param_name == 'name' or self._param_name == 'description':
            # String format
            if self._param_name == 'imdb_id':
                # Match IMDB ID in the form of 'tt9999999'
                p = re.compile('^tt\d{7}$')
                match = p.search(entry)
                if match:
                    # Good input
                    return True, entry
                else:
                    self.val_input = False
                    return False, 'Invalid IMDB ID! '
            elif self._param_name == 'genres':
                print('genre regex check.')
                # Match genres in comma-separated list, without trailing comma
                p = re.compile('^(\d+)(,(\d+))*$')
                match = p.search(entry)
                if match:
                    print('checking genres entered')
                    for genre_num in entry.split(','):
                        try:
                            moviedb_genre.GENRE_DICT[genre_num]
                        except KeyError:
                            logger.log_message(0, str(genre_num) + ' is not a valid genre number!')
                            self.val_input = False
                            return False, str(genre_num) + ' is not a valid genre number! '
                    # Good input
                    print('Good to go!')
                    return True, entry
                else:
                    self.val_input = False
                    return False, 'Improper Genre string! '
            elif self._param_name == 'release_date':
                # Match date YYYY-MM-DD
                p = re.compile('^(19|20)\d{2}-(0?[1-9]|1[0-2])-(0?[1-9]|[12]\d|3[01])$')
                match = p.search(entry)
                if match:
                    # Good input
                    return True, entry
                else:
                    self.val_input = False
                    return False, 'Improper release date format! '
            elif self._param_name == 'posterUrl':
                # Match poster url
                p = re.compile('^(http|https)://image.tmdb.org/t/p/original/[\d\w]+.(jpg|png)$')
                match = p.search(entry)
                if match:
                    # Good input
                    return True, entry
                else:
                    self.val_input = False
                    return False, 'Improper poster url format! '
            elif self._param_name == 'name':
                # No special criteria, add to movie object
                return True, entry
            elif self._param_name == 'description':
                # No special criteria, add to movie object
                return True, entry
        else:
            # param_name not properly set
            logger.log_message(0, 'param_name not properly set! ' + self._param_name)
            self.val_input = False
            return False, 'param_name not properly set! See logs. '
