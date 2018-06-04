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

# title           :librarydb_menu.py
# description     :LibraryDBMenu class definitions.
# author          :Eric Kimsey
# usage           :
# notes           :
# python_version  :3.5+
# =======================================================================

import globals
from menu_system import menu_manager
from ludus_menus.librarydb_search import LibraryDBSearch
from ludus_menus.librarydb_title import LibraryDBTitle
from menu_system.menu_types.option_select import OptionSelect


class LibraryDBMenu(OptionSelect):
    TITLE = 'LibraryDB Search'

    def __init__(self):
        """
        Create LibraryDBMenu, for selecting search options in LibraryDB.
        """
        prompt = 'Selection: '
        options = {
            '1': LibraryDBSearch.TITLE,
            '2': LibraryDBTitle.TITLE
        }
        special_options = {
            'B': 'Back',
            'Q': 'Exit'
        }
        super().__init__(globals.VERSION + ' - ' + self.TITLE, prompt, options, special_options)

    @staticmethod
    def process_input(entry) -> tuple:
        """
        Handle all option and special option actions.
        :param str entry: User's input
        :return tuple: Success = True or Fail = False, next menu or status message
        """
        entry = entry.upper()
        if entry == '1':
            # Create LibraryDB text search OptionSelect menu
            next_menu = LibraryDBSearch()
            return True, next_menu
        elif entry == '2':
            # Create LibraryDB title search OptionSelect menu
            next_menu = LibraryDBTitle()
            return True, next_menu
        elif entry == 'B':
            menu_manager.back()
            return False, ''
        else:
            # Quit
            quit()
