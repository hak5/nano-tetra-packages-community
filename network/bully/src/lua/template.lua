--[[
DO NOT modify directly global variables IF you want to preserve
their original value throughout the execution of the script
(tables and numbers; strings are immutable)
]]--

-- Make use of provided libraries!
require("algorithm")
-- require("wps")

-- Entry point (returns an arbitrary list of PINs)
function main()
	return algorithm.hex2dec(str_bssid), 12345670
end

--[[
Global variables:
 * tbl_bssid[1..6] (or 'str_bssid' as string variant)
 * str_essid       (string)
 * str_wps_serial  (string)
 * wps_version     (real)
]]--
