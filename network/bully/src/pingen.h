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
#ifndef _PINGEN_H
#define _PINGEN_H

#include <stdint.h>

unsigned int gen_hex2dec(uint8_t *bssid, const int offset);
unsigned int gen_zyxel(uint8_t *bssid, const int offset);
unsigned int gen_dlink(uint8_t *bssid, const int offset);
unsigned int gen_belkin(uint8_t *bssid, const char *serial);

/* Included to avoid possible linking issues with main project */
unsigned int m_wps_pin_checksum(unsigned int pin);
unsigned int m_wps_pin_valid(unsigned int pin);

#endif /* _PINGEN_H */
