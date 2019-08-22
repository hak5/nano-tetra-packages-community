--[[
 Pure implementations in Lua 5.2 (without using the 'wps' library)
]]--

-- Same as 'wps.pin_checksum(pin)'
function wps_pin_checksum(pin)
	local accum = 0
	pin = pin * 10
	accum = accum + 3 * (math.floor(pin / 10000000) % 10)
	accum = accum + 1 * (math.floor(pin / 1000000) % 10)
	accum = accum + 3 * (math.floor(pin / 100000) % 10)
	accum = accum + 1 * (math.floor(pin / 10000) % 10)
	accum = accum + 3 * (math.floor(pin / 1000) % 10)
	accum = accum + 1 * (math.floor(pin / 100) % 10)
	accum = accum + 3 * (math.floor(pin / 10) % 10)
	return (10 - (accum % 10)) % 10
end

-- Same as 'wps.pin_valid(pin)' except this one returns true or false (!)
function wps_pin_valid(pin)
	return wps_pin_checksum(math.floor(pin / 10)) == (pin % 10)
end
