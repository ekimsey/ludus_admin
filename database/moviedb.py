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

# title           :MovieDB.py
# description     :MovieDB API interface.
# author          :Eric Kimsey
# usage           :
# notes           :
# python_version  :3.5+
# =======================================================================

import re
import urllib.request
from urllib.error import HTTPError
from urllib.error import URLError
from logger import logger
import globals
from movie.moviedb_movie import MovieDBMovie


def get_api_key():
    key_file = open(globals.API_KEY, 'r')
    key = key_file.readline().replace('\n', '').replace('\r', '')
    key_file.close()
    return key


def query(search_term: str) -> tuple:
    """
    Query MovieDB API with a general search term.
    :param str search_term: Search term
    :return tuple: True = Success or False = Fail, List of MovieDB movies or status message
    """
    base_url = 'https://api.themoviedb.org/3/search/movie?'
    api_key = 'api_key=' + get_api_key()
    query1 = '&language=en-US&query='
    search_term = search_term.replace(' ', '%20')
    query2 = '&page=1&include_adult=false&region=US'

    url = base_url + api_key + query1 + search_term + query2

    response = moviedb_api_call(url)
    if response[0] is False:
        return response
    else:
        response_str = response[1]

    # Debug
    # logger.log_message(1, response_str)

    pattern = re.compile('{[\s\S]*?"id":(\d+),[\s\S]*?' +
                         '"title":"([\s\S]+?)",[\s\S]*?' +
                         '"poster_path":"([\s\S]+?)",[\s\S]*?' +
                         '"genre_ids":\[([\d,]+?)],[\s\S]*?' +
                         '"overview":"([\s\S]+?)",[\s\S]*?' +
                         '"release_date":"(\d{4}-\d{2}-\d{2})"(},|}])')
    matches = pattern.findall(response_str)
    # logger.log_message(1, str(matches))
    movie_list = []
    for i in range(9):
        try:
            match = matches[i]
        except IndexError:
            break
        movie = MovieDBMovie(match[1], int(match[0]), match[4], match[5],
                             'http://image.tmdb.org/t/p/original/' + match[2], match[3])
        movie_list.append(movie)

    return True, movie_list


def get_movie_imdb_id(moviedb_id: int) -> tuple:
    """
    Retrieve a movie's IMDB ID given it's MovieDB ID.
    :param int moviedb_id: The movie's MovieDB ID
    :return tuple: True = Success or False = Fail, The movie's IMDB ID or status message
    """
    base_url = 'https://api.themoviedb.org/3/movie/'
    api_key = '?api_key=' + get_api_key()
    language = '&language=en-US'

    url = base_url + str(moviedb_id) + api_key + language

    response = moviedb_api_call(url)
    if response[0] is False:
        return response
    else:
        response_str = response[1]

    # print(response_str)

    # response_str = response_str.replace('\\\'', "'")
    # DEBUG
    # Logger.log_message(1, response_str)

    pattern = re.compile('"imdb_id":\s*"(tt\d{7})"')
    match = pattern.search(response_str)

    if match:
        return True, match.group(1)
    else:
        # MovieDB response does not match RegEx pattern. No IMDB ID.
        logger.log_message(1, 'MovieDB response does not match RegEx pattern. No imdb_id found.')
        return False, 'WARNING: No IMDB found! '


def query_by_imdb_id(imdb_id: str) -> tuple:
    """
    Query MovieDB API using an IMDB ID.
    :param str imdb_id: IMDB ID in the form ttNNNNNNN
    :return tuple: True = Success or False = Fail, MovieDB_Movie object or status message
    """
    base_url = 'https://api.themoviedb.org/3'
    api_key = 'api_key=' + get_api_key()

    find_by_imdb_id = '/find/'
    find_by_imdb_id2 = '?external_source=imdb_id&'

    url = base_url + find_by_imdb_id + imdb_id + find_by_imdb_id2 + api_key

    response = moviedb_api_call(url)
    if response[0] is False:
        return response
    else:
        response_str = response[1]

    # response_str = response_str.replace('\\\'', "'")
    # DEBUG
    # Logger.log_message(1, response_str)

    pattern = re.compile('"genre_ids":\[([\d,]+)\]'
                         + '[\s\S]*'
                         + '"id":([\d]+?),'
                         + '[\s\S]*'
                         + '"original_title":"([\s\S]+?)",'
                         + '[\s\S]*'
                         + '"overview":"([\s\S]+?)",'
                         + '[\s\S]*'
                         + '"release_date":"([\s\S]+?)",'
                         + '[\s\S]*'
                         + '"poster_path":"/([\s\S]+?)"')
    match = pattern.search(response_str)

    if match:
        movie = MovieDBMovie(match.group(3), int(match.group(2)), match.group(4), match.group(5),
                             'http://image.tmdb.org/t/p/original/' + match.group(6), match.group(1), imdb_id)
        return True, movie
    else:
        # MovieDB response does not match RegEx pattern. Incorrect imdb_id.
        logger.log_message(1, 'MovieDB response does not match RegEx pattern. Incorrect imdb_id.')
        return False, 'WARNING: Movie not found! '


def moviedb_api_call(url: str) -> tuple:
    """
    Make MovieDB API call and return the server response.
    :param url: API call URL
    :return tuple: True = Success or False = Fail, server response or status message
    """
    tries = 0
    while True:
        try:
            response = urllib.request.urlopen(url)
            response_str = str(response.read())
            break
        except HTTPError as err:
            logger.log_message(0, str(err))
            tries += 1
            if tries <= 5:
                logger.log_message(1, 'Retrying...(' + tries + ')')
            else:
                logger.log_message(0, 'Exceeded retry count. Try again later')
                return False, 'ERROR: Request to MovieDB timed out! '
        except URLError as err:
            logger.log_message(0, str(err))
            return False, 'ERROR: URLError, see logs! '

    response_str = response_str.replace("\\\'", "'")
    response_str = response_str.replace("\\\\/", "")
    return True, response_str
