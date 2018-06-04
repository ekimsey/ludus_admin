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

# title           :main_menu.py
# description     :MainMenu definition.
# author          :Eric Kimsey
# usage           :
# notes           :
# python_version  :3.5+
# =======================================================================

import globals
from ludus_menus.moviedb_menu import MovieDBMenu
from ludus_menus.librarydb_menu import LibraryDBMenu
from menu_system.menu_types.option_select import OptionSelect


class MainMenu(OptionSelect):
    TITLE = 'Main Menu'

    def __init__(self):
        """
        Create MainMenu object for selecting which database to search.
        """
        prompt = 'Which database? '
        options = {
            '1': MovieDBMenu.TITLE,
            '2': LibraryDBMenu.TITLE
        }
        special_options = {
            'Q': 'Quit'
        }
        super().__init__(globals.VERSION + ' - ' + self.TITLE, prompt, options, special_options)

    @staticmethod
    def process_input(entry: str) -> tuple:
        """
        Handle all option and special option actions.
        :param str entry: User's input
        :return tuple: True = Success or False = Fail, next menu to display or status message
        """
        entry = entry.upper()
        if entry == '1':
            # Create MovieDB Option_Select menu
            next_menu = MovieDBMenu()
            return True, next_menu
        elif entry == '2':
            # Create LibraryDB Option_Select menu
            next_menu = LibraryDBMenu()
            return True, next_menu
        else:
            # Quit
            quit()
