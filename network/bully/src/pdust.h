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
#ifndef _PDUST_H
#define _PDUST_H

#include <stdint.h>

/* Pixiewps modes */
#define PWPS_NONE             0
#define PWPS_RT               1
#define PWPS_ECOS_SIMPLE      2
#define PWPS_RTL819x          3
#define PWPS_ECOS_SIMPLEST    4
#define PWPS_ECOS_KNUTH       5

#define OUI_STR_LEN    8 + 1
struct vendor_oui {
	uint8_t oui[3];
	char name[OUI_STR_LEN];
	uint8_t pixiewps_mode;
};
typedef struct vendor_oui vendor_t;

extern char OUI_NULL[OUI_STR_LEN];
extern vendor_t vendor_list[];

char *get_vendor(uint8_t *oui);

struct wps_info {
	uint8_t vendor[3];
	uint8_t vendor_p;
	uint8_t version;
	uint8_t uuid[16];
	uint16_t category;
	uint16_t subcategory;
	uint16_t passw_id;
	uint8_t passw_id_p;
	uint16_t config_methods;
	char manufacturer[64 + 1];
	char device_name[32 + 1];
	char model_name[32 + 1];
	char model_number[32 + 1];
	char serial_number[32 + 1];
};
typedef struct wps_info wps_info_t;

#endif /* _PDUST_H */
