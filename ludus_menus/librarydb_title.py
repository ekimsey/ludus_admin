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

# title           :librarydb_title.py
# description     :LibraryDBTitle class definitions.
# author          :Eric Kimsey
# usage           :
# notes           :
# python_version  :3.5+
# =======================================================================

import globals
import logger
from menu_system import menu_manager
from database import librarydb
from ludus_menus.movie_select import MovieSelect
from menu_system.menu_types.text_entry import TextEntry


class LibraryDBTitle(TextEntry):
    TITLE = 'Search LibraryDB by title'

    def __init__(self):
        """
        Create LibraryDBTitle menu.
        """
        prompt = 'Search term: '
        special_options = {
            'B': 'Back',
            'Q': 'Exit'
        }
        add_message = 'Search term must be 2 characters or more.'
        super().__init__(globals.VERSION + ' - ' + self.TITLE, prompt, special_options, add_message)

    @staticmethod
    def process_input(entry: str) -> tuple:
        """
        Handle all option and special option actions.
        :param str entry: User's input
        :return tuple: True = Success or False = Fail, next menu or status message
        """
        if entry.upper() == 'B':
            menu_manager.back()
            return False, ''
        elif entry.upper() == 'Q':
            # Quit
            quit()
        if len(entry) < 2:
            # Entry is too short or too long, redisplay prompt
            logger.log_message(1, 'User entered less than two characters! ' + entry)
            return False, 'WARNING: Input was less than 2 characters! '
        else:
            # Input is good, query MovieDB
            response = librarydb.search_by_title(entry)
            if response[0]:
                if len(response[1]) == 0:
                    # logger.log_message(1, 'No movie found!')
                    return False, 'WARNING: No movie found! '
                else:
                    # Movies found, open Movie_Select
                    next_menu = MovieSelect(response[1], 'U')
                    return True, next_menu
            else:
                return response
