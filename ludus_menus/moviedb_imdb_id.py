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

# title           :moviedb_imdb_id.py
# description     :MovieDBIMDBID search menu definition.
# author          :Eric Kimsey
# usage           :
# notes           :
# python_version  :3.5+
# =======================================================================

import re
import globals
from logger import logger
from menu_system import menu_manager
from menu_system.menu_types.text_entry import TextEntry
from ludus_menus.format_select import FormatSelect
from ludus_menus.movie_params import MovieParams
from database import moviedb


class MovieDBIMDBID(TextEntry):
    TITLE = 'Search MovieDB by IMDB ID'

    def __init__(self):
        """
        Create MovieDBIMDBID search menu.
        """
        prompt = 'Selection: '
        special_options = {
            'B': 'Back',
            'Q': 'Exit'
        }
        selection = 'IMDB ID\'s are in the form of tt1234567.'
        super().__init__(globals.VERSION + ' - ' + self.TITLE, prompt, special_options, selection)

    @staticmethod
    def process_input(entry: str) -> tuple:
        """
        Handle all option and special option actions.
        :param str entry: User's input
        :return tuple: False (to drop back into the Menu Manager loop), status message or next menu
        """
        if entry.upper() == 'B':
            menu_manager.back()
            return False, ''
        elif entry.upper() == 'Q':
            # Quit
            quit()
        # Check if entry is in the form of IMDB ID
        # tt9999999
        if len(entry) != 9:
            # Entry is too short or too long, redisplay prompt
            logger.log_message(1, 'Entry is ' + str(len(entry)) + ' characters long. Entry: ' + entry)
            return False, 'WARNING: Input should be 9 characters! '
        else:
            pattern = re.compile('tt\d{7}')
            match = pattern.search(entry)
            # logger.log_message(1, 'Looking for regex match...')
            if match:
                # Matches IMDB ID form, query MovieDB
                # logger.log_message(1, 'Searching MovieDB...')
                response = _query_moviedb(entry)
                if response[0] is False:
                    return response
                else:
                    # logger.log_message(1, 'Proper IMDB ID entered, opening Format_Select.')
                    format_menu = FormatSelect(response[1])
                    while True:
                        response = format_menu.menu_logic()
                        if response[0]:
                            # If selection is in options/special_options, process input
                            response = format_menu.process_input(response[1])
                            if response[0]:
                                # If format was successfully selected, return LibraryDB_Movie object
                                return True, MovieParams(response[1], 'I')
                            else:
                                # Format not successfully selected, back to format select menu
                                format_menu.val_input = False
                                format_menu.inval_prompt = response[1]
                                continue
                        else:
                            # Format not successfully selected, back to format select menu
                            format_menu.val_input = False
                            format_menu.inval_prompt = response[1]
                            continue
            else:
                # Entry is not IMDB ID, redisplay prompt
                logger.log_message(1, 'NOT AN IMDB ID! ' + entry)
                return False, 'NOT AN IMDB ID! '


def _query_moviedb(entry: str) -> tuple:
    """
    Query MovieDB using API to find a movie matching the IMDB ID.
    :param str entry: Query term (IMDB ID)
    :return moviedb_movie: MovieDB movie object
    """
    # Build MovieDB query from entry
    # Query MovieDB
    # Parse results
    # Store results in Movie objects
    # return list of Movie objects
    imdb_id = entry.strip()
    response = moviedb.query_by_imdb_id(imdb_id)

    return response
