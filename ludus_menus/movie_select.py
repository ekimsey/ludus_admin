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

# title           :movie_select.py
# description     :MovieSelect menu definition.
# author          :Eric Kimsey
# usage           :
# notes           :
# python_version  :3.5+
# =======================================================================

import globals
from database import moviedb
from menu_system import menu_manager
from ludus_menus.format_select import FormatSelect
from ludus_menus.movie_params import MovieParams
from menu_system.menu_types.option_select import OptionSelect
from movie.librarydb_movie import LibraryDBMovie


class MovieSelect(OptionSelect):
    TITLE = 'Select a movie'

    def __init__(self, movie_list: list, mode: str):
        """
        Create MovieSelect menu object.
        :param list movie_list: List of movies
        :param str mode: 'I' or 'U' for either inserting or updating a movie in LibraryDB
        """
        prompt = 'Selection: '
        options = {}
        self._movie_list = movie_list
        self._mode = mode
        i = 1
        for movie in movie_list:
            options[str(i)] = str(movie)
            i = i + 1
        special_options = {
            'B': 'Back',
            'Q': 'Exit'
        }
        super().__init__(globals.VERSION + ' - ' + self.TITLE, prompt, options, special_options)

    def process_input(self, entry) -> tuple:
        """
        Handle all option and special option actions.
        :param str entry: User's input
        :return tuple: True = Success or False = Fail, next menu to display or failure message
        """
        if entry.upper() == 'B':
            menu_manager.back()
            return False, ''
        elif entry.upper() == 'Q':
            # Quit
            quit()

        if self._mode == 'I':
            format_menu = FormatSelect(self._movie_list[int(entry) - 1])
        while True:
            if self._mode == 'I':
                response = format_menu.menu_logic()
            else:
                response = True, ''
            if response[0]:
                # If format entry is in options/special_options, pass entry to process input
                if self._mode == 'I':
                    response = format_menu.process_input(response[1])
                if response[0]:
                    # If format was successfully chosen, retrieve movie's IMDB ID from MovieDB
                    if self._mode == 'I':
                        movie = response[1]
                        response = moviedb.get_movie_imdb_id(response[1].movie_db_id)
                    else:
                        movie = self._movie_list[int(entry) - 1]
                    if response[0]:
                        # If movie's IMDB ID was successfully retrieved, create LibraryDB_Movie object with IMDB ID
                        if self._mode == 'I':
                            movie = LibraryDBMovie(movie.title,
                                                   movie.movie_db_id,
                                                   movie.title_format,
                                                   movie.title_status,
                                                   response[1],
                                                   movie.genre_ids,
                                                   movie.description,
                                                   movie.release_date,
                                                   movie.poster_url)
                        return True, MovieParams(movie, self._mode)
                    else:
                        # Couldn't obtain IMDB ID, back to format select menu.
                        format_menu.val_input = False
                        format_menu.inval_prompt = response[1]
                        continue
                else:
                    # Error choosing format, back to format select
                    format_menu.val_input = False
                    format_menu.inval_prompt = response[1]
                    continue
            else:
                # Error choosing format, back to format select
                format_menu.val_input = False
                format_menu.inval_prompt = response[1]
                continue
