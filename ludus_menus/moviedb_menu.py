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

# title           :moviedb_menu.py
# description     :MovieDBMenu menu definition.
# author          :Eric Kimsey
# usage           :
# notes           :
# python_version  :3.5+
# =======================================================================

import globals
from menu_system import menu_manager
from menu_system.menu_types.option_select import OptionSelect
from ludus_menus.moviedb_imdb_id import MovieDBIMDBID
from ludus_menus.moviedb_search import MovieDBSearch


class MovieDBMenu(OptionSelect):
    TITLE = 'Search MovieDB'

    def __init__(self):
        """
        Create MovieDBMenu object, for selecting search options in MovieDB.
        """
        prompt = 'Selection: '
        options = {
            '1': MovieDBIMDBID.TITLE,
            '2': MovieDBSearch.TITLE
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
            # Create MovieDB IMDB ID search Option_Select menu
            next_menu = MovieDBIMDBID()
            return True, next_menu
        elif entry == '2':
            # Create MovieDB text search Option_Select menu
            next_menu = MovieDBSearch()
            return True, next_menu
        elif entry == 'B':
            menu_manager.back()
            return False, ''
        else:
            # Quit
            quit()
