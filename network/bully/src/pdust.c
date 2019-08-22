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
#include <stdint.h>
#include <string.h>

#include "pdust.h"

char OUI_NULL[OUI_STR_LEN] = "-";
vendor_t vendor_list[] = {
	{"\x00\x03\x7f", "AtherosC", PWPS_NONE},        /* Atheros Communications */
	{"\x00\x10\x18", "Broadcom", PWPS_ECOS_SIMPLE}, /* Broadcom */
	{"\x00\x50\x43", "MarvellS", PWPS_NONE},        /* MARVELL SEMICONDUCTOR, INC */
	{"\x00\x0c\x43", "RalinkTe", PWPS_RT},          /* Ralink Technology, Corp. */
	{"\x00\xe0\x4c", "RealtekS", PWPS_RTL819x}      /* REALTEK SEMICONDUCTOR CORP. */
};

#define VENDOR_LIST_SIZE (sizeof(vendor_list)/sizeof(vendor_list[0]))

char *get_vendor(uint8_t * oui)
{
	int i;
	for (i = 0; i < VENDOR_LIST_SIZE; i++) {
		if (!memcmp(vendor_list[i].oui, oui, 3))
			return vendor_list[i].name;
	};
	return OUI_NULL;
};
