/*
    bully - retrieve WPA/WPA2 passphrase from a WPS-enabled AP

    Copyright (C) 2017  wiire         <wi7ire@gmail.com>

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
*/
#include <lua.h>

/* Open WPS-related library */
int luaopen_wpslib(lua_State *L);

/* Open PIN algorithms library */
int luaopen_algolib(lua_State *L);

/* Create a basic Lua environment (omit some libraries) */
lua_State *basic_env();
