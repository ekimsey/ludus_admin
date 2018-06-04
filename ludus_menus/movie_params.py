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

# title           :movie_params.py
# description     :MovieParams menu definition.
# author          :Eric Kimsey
# usage           :
# notes           :
# python_version  :3.5+
# =======================================================================

from typing import Union
import globals
from logger import logger
from menu_system import menu_manager
from menu_system.menu_types.status_message import StatusMessage
from menu_system.menu_types.option_select import OptionSelect
from ludus_menus.confirm_insert import ConfirmInsert
from ludus_menus.confirm_update import ConfirmUpdate
from ludus_menus.param_edit import ParamEdit
from movie.librarydb_movie import LibraryDBMovie
from movie import librarydb_format
from movie import moviedb_genre
from movie import librarydb_status


class MovieParams(OptionSelect):
    TITLE = 'Edit Movie Parameters'

    def __init__(self, movie: LibraryDBMovie, mode: str):
        """
        Create MovieParams menu object.
        :param LibraryDBMovie movie: Movie that needs edited.
        :param str mode: I or U, whether the movie is to be inserted or updated in LibraryDB
        """
        prompt = 'Selection: '
        self.mode = mode
        # Create a string of all the genre names of this movie
        genre_names = ' ('
        written = False
        for genre_num in movie.genre_ids.split(','):
            movie_genre = moviedb_genre.GENRE_DICT[genre_num]
            if movie_genre is Exception:
                logger.log_message(0, movie_genre)
            else:
                genre_names += movie_genre + ", "
                written = True
        if written:
            genre_names = genre_names[:-2]
        genre_names += ')'

        format_name = ' (' + librarydb_format.FORMAT_DICT[str(movie.title_format)] + ')'
        status_name = ' (' + librarydb_status.STATUS_DICT[str(movie.title_status)] + ')'

        options = {
            '1': 'Title: ' + movie.title,
            '2': 'MovieDB ID: ' + str(movie.movie_db_id),
            '3': 'Format: ' + str(movie.title_format) + format_name,
            '4': 'IMDB ID: ' + movie.imdb_id,
            '5': 'Genres: ' + movie.genre_ids + genre_names,
            '6': 'Description: ' + movie.description,
            '7': 'Release Date: ' + movie.release_date,
            '8': 'Poster URL: ' + movie.poster_url,
            '9': 'Status: ' + str(movie.title_status) + status_name
        }
        if mode == 'I':
            special_options = {
                'I': 'Insert into LibraryDB',
                'B': 'Back',
                'Q': 'Exit'
            }
        elif mode == 'U':
            special_options = {
                'U': 'Update LibraryDB Movie',
                'B': 'Back',
                'Q': 'Exit'
            }
        else:
            special_options = {
                'B': 'Back',
                'Q': 'Exit'
            }
        super().__init__(globals.VERSION + ' - ' + self.TITLE, prompt, options, special_options)
        self.movie = movie

    def process_input(self, entry: str) -> tuple:
        """
        Handle all option and special option actions.
        :param str entry: User's input
        :return tuple: True = Success or False = Fail, next menu to display or failure message
        """
        param_menu = None
        if entry == '1':
            # Param_Edit title
            param_menu = ParamEdit(('name', self.movie.title))
        elif entry == '2':
            # Param_Edit movie_db_id
            param_menu = ParamEdit(('movie_db_id', self.movie.movie_db_id))
        elif entry == '3':
            # Param_Edit format
            param_menu = ParamEdit(('format', self.movie.title_format))
        elif entry == '4':
            # Param_Edit imdb_id
            param_menu = ParamEdit(('imdb_id', self.movie.imdb_id))
        elif entry == '5':
            # Param_Edit genres
            param_menu = ParamEdit(('genres', self.movie.genre_ids))
        elif entry == '6':
            # Param_Edit description
            param_menu = ParamEdit(('description', self.movie.description))
        elif entry == '7':
            # Param_Edit release_data
            param_menu = ParamEdit(('release_date', self.movie.release_date))
        elif entry == '8':
            # Param_Edit posterUrl
            param_menu = ParamEdit(('posterUrl', self.movie.poster_url))
        elif entry.upper() == 'I':
            confirm_insert = ConfirmInsert(self.movie)
            entry = confirm_insert.menu_logic()
            if entry[0]:
                entry = confirm_insert.process_input(entry[1])
                return entry
        elif entry.upper() == 'U':
            confirm_update = ConfirmUpdate(self.movie)
            entry = confirm_update.menu_logic()
            if entry[0]:
                entry = confirm_update.process_input(entry[1])
                return entry
        elif entry.upper() == 'B':
            menu_manager.back()
            return False, ''
        else:
            # Quit
            quit()

        while True:
            sel = param_menu.menu_logic()
            print(sel)
            if sel[0]:
                sel = param_menu.process_input(sel[1])
                if sel[0]:
                    self.update_movie(entry, sel[1])
                    return False, ''
                else:
                    if len(sel[1]) > 0:
                        param_menu.inval_prompt = sel[1]
                        continue
                    else:
                        return sel
            else:
                return sel

    def update_movie(self, param_num: str, new_param_val: Union[str, int]) -> None:
        """
        Update LibraryDB_Movie parameter.
        :param str param_num: Number of parameter to be updated
        :param Union[str, int] new_param_val: New value of the parameter
        :return None: Nothing
        """
        if param_num == 0:
            # parameter wasn't properly updated.
            pass
        if param_num == '1':
            # Param_Edit title
            self.movie.title = new_param_val
            self._options[param_num] = 'Title: ' + new_param_val
        elif param_num == '2':
            # Param_Edit movie_db_id
            self.movie.movie_db_id = new_param_val
            self._options[param_num] = 'MovieDB ID: ' + new_param_val
        elif param_num == '3':
            # Param_Edit format
            self.movie.title_format = new_param_val
            format_name = ' (' + librarydb_format.FORMAT_DICT[new_param_val] + ')'
            self._options[param_num] = 'Format: ' + new_param_val + format_name
        elif param_num == '4':
            # Param_Edit imdb_id
            self.movie.imdb_id = new_param_val
            self._options[param_num] = 'IMDB ID: ' + new_param_val
        elif param_num == '5':
            # Param_Edit genres
            self.movie.genre_ids = new_param_val
            # Create a string of all the genre names of this movie
            genre_names = ' ('
            written = False
            for genre_num in new_param_val.split(','):
                movie_genre = moviedb_genre.GENRE_DICT[genre_num]
                if movie_genre is Exception:
                    logger.log_message(0, movie_genre)
                else:
                    genre_names += movie_genre + ', '
                    written = True
            if written:
                genre_names = genre_names[:-2]
            genre_names += ')'
            self._options[param_num] = 'Genres: ' + new_param_val + genre_names
        elif param_num == '6':
            # Param_Edit description
            self.movie.description = new_param_val
            self._options[param_num] = 'Description: ' + new_param_val
        elif param_num == '7':
            # Param_Edit release_data
            self.movie.release_date = new_param_val
            self._options[param_num] = 'Release Date: ' + new_param_val
        elif param_num == '8':
            # Param_Edit posterUrl
            self.movie.poster_url = new_param_val
            self._options[param_num] = 'Poster URL: ' + new_param_val
        else:
            logger.log_message(0, 'Param num not set in Movie_Params.update_movie()')
            status_message = StatusMessage('An Error Occurred', 'Press [Enter] to exit...',
                                           'An error occurred in Movie_Params.update_movie(). See logs for details.')
            status_message.menu_logic()
            exit(1)
