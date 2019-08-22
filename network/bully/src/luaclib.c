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
#include <stdio.h>

#include <lua.h>
#include <lualib.h>
#include <lauxlib.h>

#include "pingen.h"

/* For debugging when developing */
static void stack_dump(lua_State *L)
{
	int i;
	int top = lua_gettop(L);
	for (i = 1; i <= top; i++) { /* Repeat for each level */
		int t = lua_type(L, i);
		switch (t) {
		case LUA_TSTRING: /* Strings */
			printf("`%s'", lua_tostring(L, i));
			break;
		case LUA_TBOOLEAN: /* Booleans */
			printf(lua_toboolean(L, i) ? "true" : "false");
			break;
		case LUA_TNUMBER: /* Numbers */
			printf("%g", lua_tonumber(L, i));
			break;
		default: /* Other values */
			printf("%s", lua_typename(L, t));
			break;
		};
		printf("  "); /* Put a separator */
	};
	printf("\n"); /* End the listing */
};

/* Lua wrapper around 'wps_pin_checksum' */
static int l_wps_checksum(lua_State *L)
{
	if (lua_gettop(L) == 1) { /* 1 argument passed */
		if (lua_isnumber(L, -1)) { /* Either number or string representing number */
			unsigned int n = lua_tonumber(L, -1);
			n = m_wps_pin_checksum(n);
			lua_pushnumber(L, n); /* Push result */
			return 1; /* Number of results returned */
		};
	};
};

/* Lua wrapper around 'wps_pin_valid' */
static int l_wps_valid(lua_State *L)
{
	if (lua_gettop(L) == 1) { /* 1 argument passed */
		if (lua_isnumber(L, -1)) { /* Either number or string representing number */
			unsigned int n = lua_tonumber(L, -1);
			n = m_wps_pin_valid(n);
			lua_pushnumber(L, n); /* Push result */
			return 1; /* Number of results returned */
		};
	};
};

/* Exposed functions */
const struct luaL_Reg wps_fn[] = {
	{"pin_checksum", l_wps_checksum},
	{"pin_valid",    l_wps_valid   },
	{NULL, NULL}
};

/* Load functions */
int luaopen_wpslib(lua_State *L)
{
	luaL_newlibtable(L, wps_fn);
	luaL_setfuncs(L, wps_fn, 0);
	return 1;
};

/* Wrapper for pair (bssid, offset) function generators */
static int l_gen_wrapper(lua_State *L, unsigned int (*f)(uint8_t *, int), int change)
{
	unsigned int num_args = lua_gettop(L);
	int index = -1;
	int offset = change;
	int type;
	if (num_args == 1) {

redo:
		type = lua_type(L, index);
		if (type == LUA_TSTRING) {
			unsigned int len = lua_rawlen(L, index);
			if (len == 12 || len == 6) {
				const char *bssid = lua_tostring(L, index) + (len - 6);
				uint8_t bmac[6]; unsigned int imac[3];
				sscanf(bssid, "%02X%02X%02X", &imac[0], &imac[1], &imac[2]);
				bmac[3] = imac[0]; bmac[4] = imac[1]; bmac[5] = imac[2];
				unsigned int pin = f(bmac, offset);
				lua_pushnumber(L, pin);
				return 1; /* Number of results */
			};
		} else if (type == LUA_TTABLE) {
			unsigned int len = lua_rawlen(L, index);
			if (len == 6 || len == 3) {
				uint8_t bmac[6];
				for (unsigned int i = 0; i < 3; i++) {
					lua_rawgeti(L, index - i, len - 3 + 1 + i);
					bmac[3 + i] = (uint8_t) lua_tonumber(L, -1);
				};
				lua_pop(L, 3);
				unsigned int pin = f(bmac, offset);
				lua_pushnumber(L, pin);
				return 1; /* Number of results */
			};
		};
	} else if (num_args == 2) {
		int current = -1;
		if (lua_type(L, current) == LUA_TNUMBER) {
			index = -2;
		} else if (lua_type(L, --current) == LUA_TNUMBER) {
			index = -1;
		} else {
			lua_pushnil(L);
			return 1;
		};
		offset = lua_tonumber(L, current);
		goto redo; /* If the code is readable, GOTOs are not a bad practice */
	};
	lua_pushnil(L); /* Error */
	return 1;
};

/* Lua wrapper around 'gen_hex2dec' */
static int l_gen_hex2dec(lua_State *L)
{
	#define HEX2DEC_OFFSET 0
	return l_gen_wrapper(L, gen_hex2dec, HEX2DEC_OFFSET);
};

/* Lua wrapper around 'gen_zyxel' */
static int l_gen_zyxel(lua_State *L)
{
	#define ZYXEL_OFFSET 0
	return l_gen_wrapper(L, gen_zyxel, ZYXEL_OFFSET);
};

/* Lua wrapper around 'gen_dlink' */
static int l_gen_dlink(lua_State *L)
{
	#define DLINK_OFFSET 1 /* WAN mac is BSSID + 1 */
	return l_gen_wrapper(L, gen_dlink, DLINK_OFFSET);
};

/* Lua wrapper around 'gen_belkin' */
static int l_gen_belkin(lua_State *L)
{
	unsigned int num_args = lua_gettop(L);
	if (num_args == 2) {
		int type_first = lua_type(L, -1);
		int type_second = lua_type(L, -2);
		if (type_second == LUA_TTABLE && type_first == LUA_TSTRING) {
			unsigned int len = lua_rawlen(L, -2);
			if (len == 6 || len == 3) {
				uint8_t bmac[6];
				for (unsigned int i = 0; i < 3; i++) {
					lua_rawgeti(L, -2 - i, len - 3 + 1 + i);
					bmac[3 + i] = (uint8_t) lua_tonumber(L, -1);
				};
				lua_pop(L, 3);
				const char *serial = lua_tostring(L, -1);
				unsigned int pin = gen_belkin(bmac, serial);
				lua_pushnumber(L, pin);
				return 1; /* Number of results */
			} else {
				goto error; /* Error */
			};
		} else if (type_second == LUA_TSTRING && type_first == LUA_TTABLE) {
			unsigned int len = lua_rawlen(L, -1);
			if (len == 6 || len == 3) {
				uint8_t bmac[6];
				for (unsigned int i = 0; i < 3; i++) {
					lua_rawgeti(L, -1 - i, len - 3 + 1 + i);
					bmac[3 + i] = (uint8_t) lua_tonumber(L, -1);
				};
				lua_pop(L, 3);
				const char *serial = lua_tostring(L, -2);
				unsigned int pin = gen_belkin(bmac, serial);
				lua_pushnumber(L, pin);
				return 1; /* Number of results */
			} else {
				goto error; /* Error */
			};
		} else if (type_second == LUA_TSTRING && type_first == LUA_TSTRING) {
			unsigned int len1 = lua_rawlen(L, -1);
			unsigned int len2 = lua_rawlen(L, -2);
			int idx_bssid;
			int idx_serial;
			const char *bssid;
			const char *serial;
			unsigned int bssidlen;
			if ((len2 == 6 || len2 == 12) && (len1 != 6 && len1 != 12)) {
				idx_bssid = -2;
				idx_serial = -1;
			} else if ((len1 == 6 || len1 == 12) && (len2 != 6 && len2 != 12)) {
				idx_bssid = -1;
				idx_serial = -2;
			} else { /* If undistinguishable assume first parameter is bssid */
				idx_bssid = -2;
				idx_serial = -1;
			};
			serial = lua_tostring(L, idx_serial);
			bssidlen = lua_rawlen(L, idx_bssid);
			if (bssidlen == 12 || bssidlen == 6) {
				const char *bssid = lua_tostring(L, idx_bssid) + (bssidlen - 6);
				uint8_t bmac[6]; unsigned int imac[3];
				sscanf(bssid, "%02X%02X%02X", &imac[0], &imac[1], &imac[2]);
				bmac[3] = imac[0]; bmac[4] = imac[1]; bmac[5] = imac[2];
				unsigned int pin = gen_belkin(bmac, serial);
				lua_pushnumber(L, pin);
				return 1;
			};
		};
	};

error:
	lua_pushnil(L);
	return 1;
};

/* Exposed functions */
const struct luaL_Reg algo_fn[] = {
	{"hex2dec", l_gen_hex2dec},
	{"zyxel",   l_gen_zyxel  },
	{"dlink",   l_gen_dlink  },
	{"belkin",  l_gen_belkin },
	{NULL, NULL}
};

/* Load functions */
int luaopen_algolib(lua_State *L)
{
	luaL_newlibtable(L, algo_fn);
	luaL_setfuncs(L, algo_fn, 0);
	return 1;
};

/* Create a basic Lua environment (omit some libraries) */
lua_State *basic_env() {
	lua_State *L = luaL_newstate();
	if (L) {
		lua_pushcfunction(L, luaopen_base);
		lua_pushstring(L, "");
		lua_call(L, 1, 0);
		lua_pushcfunction(L, luaopen_package);
		lua_pushstring(L, LUA_LOADLIBNAME);
		lua_call(L, 1, 0);
		lua_pushcfunction(L, luaopen_string);
		lua_pushstring(L, LUA_LOADLIBNAME);
		lua_call(L, 1, 0);
		lua_pushcfunction(L, luaopen_table);
		lua_pushstring(L, LUA_LOADLIBNAME);
		lua_call(L, 1, 0);
		lua_pushcfunction(L, luaopen_math);
		lua_pushstring(L, LUA_LOADLIBNAME);
		lua_call(L, 1, 0);
	}
	return L;
};
