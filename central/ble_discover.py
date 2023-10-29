import asyncio
from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import (
    AdvertisementData,
)
from typing import (
    Dict,
    Tuple,
)
from bleak import uuids

async def discover_devices() -> Dict[str, Tuple[BLEDevice, AdvertisementData]]: 
    devices = await BleakScanner.discover(return_adv=True)
    for key in devices:
        d,a = devices[key]
        print(f"{d} : {a}")
    return devices

async def get_address() -> str:
    devices = await BleakScanner.discover(return_adv=True)
    for key in devices:
        d,a = devices[key]
        print(f"{d} : {a}")
        if d.name.__eq__('Pico Terminal'):
            return d.address
    return ""    

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(discover_devices())
