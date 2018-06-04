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

# title           :confirm_insert.py
# description     :ConfirmInsert menu definition.
# author          :Eric Kimsey
# usage           :
# notes           :
# python_version  :3.5+
# =======================================================================

import globals
from menu_system import menu_manager
from database import librarydb
from menu_system.menu_types.option_select import OptionSelect
from menu_system.menu_types.status_message import StatusMessage
from movie.librarydb_movie import LibraryDBMovie


class ConfirmInsert(OptionSelect):
    TITLE = 'Insert into LibraryDB'

    def __init__(self, movie: LibraryDBMovie):
        """
        Create ConfirmInsert selection menu.
        :param LibraryDBMovie movie: LibraryDBMovie to be inserted into LibraryDB
        """
        prompt = 'Insert into LibraryDB? '
        options = {
            'Y': 'Yes',
            'N': 'No'
        }
        special_options = {
            'B': 'Back',
            'Q': 'Quit'
        }
        self._movie = movie
        super().__init__(globals.VERSION + ' - ' + self.TITLE, prompt, options, special_options)

    def process_input(self, entry: str) -> tuple:
        """
        Handle all option and special option actions.
        :param str entry: User's input
        :return tuple: False (to drop back into the Menu Manager loop), status message
        """
        if entry.upper() == 'B' or entry.upper() == 'N':
            return False, ''
        elif entry.upper() == 'Q':
            quit()
        elif entry.upper() == 'Y':
            result = librarydb.insert_movie(self._movie)
            if result[0]:
                # Success
                title = globals.VERSION + ' - Insert Successful'
                prompt = 'Press [Enter] to return to the main menu...'
                message = 'Movie was successfully inserted into LibraryDB!'
                status = StatusMessage(title, prompt, message)
                status.menu_logic()
                menu_manager.to_menu_root()
                return False, ''
            else:
                # Failures
                return result
        else:
            return False, 'WARNING: Invalid option! '
