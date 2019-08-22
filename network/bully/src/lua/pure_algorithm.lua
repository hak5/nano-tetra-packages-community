--[[
 Pure implementations in Lua 5.2 (without using the 'algorithm' library)
]]--

-- Same as 'algorithm.hex2dec(tbl_bssid, [offset])'
-- or      'algorithm.hex2dec(str_bssid, [offset])'
function gen_hex2dec(offset)
	local pin = tonumber(str_bssid:sub(-6), 16)
	pin = pin + (offset == nil and 0 or offset) -- Default offset = 0
	pin = pin % 10000000
	return pin * 10 +  wps_pin_checksum(pin)
end

-- Same as 'algorithm.zyxel(tbl_bssid, [offset])'
-- or      'algorithm.zyxel(str_bssid, [offset])'
function gen_zyxel(offset)
	local pin = tonumber(str_bssid:sub(-1, -2) .. str_bssid:sub(-3, -4)
			.. str_bssid:sub(-5, -6), 16)
	pin = pin + (offset == nil and 0 or offset)
	pin = pin % 10000000
	return pin * 10 + wps_pin_checksum(pin)
end

-- Same as 'algorithm.dlink(tbl_bssid, [offset])'
-- or      'algorithm.dlink(str_bssid, [offset])
function gen_dlink(offset)
	local pin = tonumber(str_bssid:sub(-6), 16)
	pin = pin + (offset == nil and 1 or offset) -- WAN mac is BSSID + 1 (default)
	pin = bit32.bxor(pin, tonumber("0x55AA55"))
	pin = bit32.bxor(pin, (bit32.lshift(bit32.band(pin, 15), 4)
			+ bit32.lshift(bit32.band(pin, 15), 8)
			+ bit32.lshift(bit32.band(pin, 15), 12)
			+ bit32.lshift(bit32.band(pin, 15), 16)
			+ bit32.lshift(bit32.band(pin, 15), 20)))
	pin = pin % 10000000
	if (pin < 1000000) then pin = pin + ((pin % 9) * 1000000) + 1000000 end
	return pin * 10 +  wps_pin_checksum(pin)
end

-- Same as 'algorithm.belink(tbl_bssid, str_wps_serial)'
-- or      'algorithm.belink(str_bssid, str_wps_serial)'
function gen_belkin()
	local sn = {
		tonumber(str_wps_serial:sub(-1, -1), 16),
		tonumber(str_wps_serial:sub(-2, -2), 16),
		tonumber(str_wps_serial:sub(-3, -3), 16),
		tonumber(str_wps_serial:sub(-4, -4), 16)
	}
	local nic = {
		tonumber(str_bssid:sub(-1, -1), 16),
		tonumber(str_bssid:sub(-2, -2), 16),
		tonumber(str_bssid:sub(-3, -3), 16),
		tonumber(str_bssid:sub(-4, -4), 16)
	}
	local k1 = (sn[3] + sn[4] + nic[1] + nic[2]) % 16
	local k2 = (sn[1] + sn[2] + nic[4] + nic[3]) % 16
	local pin = bit32.bxor(k1, sn[2])
	local t1, t2 = bit32.bxor(k1, sn[1]), bit32.bxor(k2, nic[2])
	local p1 = bit32.bxor(nic[1], sn[2], t1)
	local p2 = bit32.bxor(k2, nic[1], t2)
	local p3 = bit32.bxor(k1, sn[3], k2, nic[3])

	k1 = bit32.bxor(k1, k2)

	pin = bit32.bxor(pin, k1) * 16
	pin = (pin + t1) * 16;
	pin = (pin + p1) * 16;
	pin = (pin + t2) * 16;
	pin = (pin + p2) * 16;
	pin = (pin + k1) * 16;
	pin = pin + p3
	pin = (pin % 10000000) - (math.floor((pin % 10000000) / 10000000) * k1)
	return pin * 10 + wps_pin_checksum(pin)
end
