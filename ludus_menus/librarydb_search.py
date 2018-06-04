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

# title           :librarydb_search.py
# description     :librarydbSearch class definitions.
# author          :Eric Kimsey
# usage           :
# notes           :
# python_version  :3.5+
# =======================================================================

import globals
from logger import logger
from menu_system import menu_manager
from menu_system.menu_types.text_entry import TextEntry
from database import librarydb
from ludus_menus.movie_select import MovieSelect


class LibraryDBSearch(TextEntry):
    TITLE = 'Search librarydb text fields'

    def __init__(self):
        """
        Create LibraryDBSearch menu.
        """
        prompt = 'Search term: '
        special_options = {
            'B': 'Back',
            'Q': 'Exit'
        }
        add_message = 'Search term must be 4 characters or more.'
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
        if len(entry) < 4:
            # Entry is too short or too long, redisplay prompt
            logger.log_message(1, 'User entered less than four characters! ' + entry)
            return False, 'WARNING: Input was less than 4 characters! '
        else:
            # Input is good, query MovieDB
            response = librarydb.search_by_text(entry)
            if response[0]:
                if len(response[1]) == 0:
                    # Logger.log_message(1, 'No movie found!')
                    return False, 'WARNING: No movie found! '
                else:
                    # Movies found, open MovieSelect
                    next_menu = MovieSelect(response[1], 'U')
                    return True, next_menu
            else:
                return response
