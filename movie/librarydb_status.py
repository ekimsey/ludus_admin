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

# title           :librarydb_status.py
# description     :Status dictionary
# author          :Eric Kimsey
# usage           :
# notes           :
# python_version  :3.5+
# =======================================================================

STATUS_DICT = {
    '1': 'Checked In',
    '2': 'Requested',
    '3': 'Checked Out',
    '4': 'Missing'
}
