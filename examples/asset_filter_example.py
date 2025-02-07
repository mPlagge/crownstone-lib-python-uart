#!/usr/bin/env python3

"""
Example to upload asset filters via UART.
"""
import asyncio

import crownstone_core
from crownstone_core.packets.assetFilter.FilterMetaDataPackets import FilterType
from crownstone_core.packets.assetFilter.builders.AssetFilter import AssetFilter
from crownstone_uart import CrownstoneUart

import logging

##### Settings #####

# The uart port to use.
# Can be set to /dev/ttyUSB0 for example.
port = None

# Set to true for debug logs.
verbose = False


if verbose:
	logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s', level=logging.DEBUG)

# Init the Crownstone UART lib.
uart = CrownstoneUart()

print("core version:", crownstone_core.__version__)
print("uart version:", uart.__version__)

async def main():
	# The try except part is just to catch a control+c to gracefully stop the libs.
	try:
		await uart.initialize_usb(port=port, writeChunkMaxSize=64)

		filterId = 0
		filter1 = AssetFilter(filterId)
		filter1.filterByMacAddress(["01:23:45:67:89:AB", "01:23:45:67:89:CD"])
		filter1.outputMacRssiReport()
		filter1.setProfileId(0)
		print("filter1:")
		print(filter1)

		filterId += 1
		filter2 = AssetFilter(filterId)
		filter2.filterByNameWithWildcards("c?w*", complete=False)
		filter2.outputAssetId().basedOnName()
		filter2.setFilterType(FilterType.CUCKOO)
		print("filter2:")
		print(filter2)

		filters = [filter1, filter2]

		print("Set filters via UART.")
		masterVersion = await uart.control.setFilters(filters)
		print("Master version:", masterVersion)

		# Simply keep the program running.
		while True:
			await asyncio.sleep(0.1)
	except KeyboardInterrupt:
		pass
	finally:
		print("\nStopping UART..")
		uart.stop()
		print("Stopped")

asyncio.run(main())
