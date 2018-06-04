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

# title           :Ludus_Admin.py
# description     :This program displays an interactive menu on CLI to control Ludus admin functions.
# author          :Eric Kimsey
# usage           :python Ludus_Admin.py
# notes           :
# python_version  :3.5+
# =======================================================================

from menu_system import menu_manager
from ludus_menus.main_menu import MainMenu


# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == '__main__':
    # Create Menu Manager
    main_menu = MainMenu()
    menu_manager.menu_logic(main_menu)
