#!/usr/bin/env python3

import sys
import asyncio
import time
from ble_central import Controller
from ble_discover import *

args = sys.argv
 
if(len(args) < 2):
    js_num = str(0)
else:
    js_num = args[1]

class WirelessController():
    class MyController(Controller):
        _pressed = 0b0000000000000000
        def __init__(self, **kwargs):
            Controller.__init__(self, **kwargs)

        # share_press + options_press + circle_press
        async def toggle_connect(self):
            if (self._pressed & 0b1100000000000000) != 0b1100000000000000:
                return
            if self._ble is None:
                return
            if self._ble.is_connected:
                print("disconnect")
                await self._ble.disconnect()
            else:
                print("connect")
                await self._ble.connect()

        # share_press + L1_press + circle_press
        async def activate(self):
            if (self._pressed & 0b0110000000000000) != 0b0110000000000000:
                return
            if self._ble is not None:
                return
            address = await get_address()
            if address.__eq__(""):
                print("not found target")
                return
            await self.pair(address)            

        # Implementation if any input is received.
        # Example
        # ---
        async def on_circle_press(self):
            await super().on_circle_press()
            eventname = sys._getframe().f_code.co_name
            await self.send(eventname.encode('utf-8'))
            await self.activate()
            await self.toggle_connect()

        async def on_R2_press(self,value):
            await super().on_R2_press(value)
            eventname = sys._getframe().f_code.co_name
            await self.send(eventname.encode('utf-8'))
            await self.send("{}".format(value).encode('utf-8'))

        async def on_L2_press(self,value):
            await super().on_L2_press(value)
            eventname = sys._getframe().f_code.co_name
            await self.send(eventname.encode('utf-8'))
            await self.send("{}".format(value).encode('utf-8'))

        async def on_L1_press(self):
            self._pressed = self._pressed | 0b0010000000000000
            print(bin(self._pressed))
            await super().on_L1_press()
            eventname = sys._getframe().f_code.co_name
            await self.send(eventname.encode('utf-8'))

        async def on_L1_release(self):
            self._pressed = self._pressed ^ 0b0010000000000000
            print(bin(self._pressed))
            await super().on_L1_release()
            eventname = sys._getframe().f_code.co_name
            await self.send(eventname.encode('utf-8'))
        
        async def on_share_press(self):
            self._pressed = self._pressed | 0b0100000000000000
            print(bin(self._pressed))
            await super().on_share_press()
            eventname = sys._getframe().f_code.co_name
            await self.send(eventname.encode('utf-8'))

        async def on_share_release(self):
            self._pressed = self._pressed ^ 0b0100000000000000
            print(bin(self._pressed))
            await super().on_share_release()
            eventname = sys._getframe().f_code.co_name
            await self.send(eventname.encode('utf-8'))          

        async def on_options_press(self):
            self._pressed = self._pressed | 0b1000000000000000
            print(bin(self._pressed))
            await super().on_options_press()
            eventname = sys._getframe().f_code.co_name
            await self.send(eventname.encode('utf-8'))

        async def on_options_release(self):
            self._pressed = self._pressed ^ 0b1000000000000000
            print(bin(self._pressed))
            await super().on_options_release()
            eventname = sys._getframe().f_code.co_name
            await self.send(eventname.encode('utf-8'))
            
        async def on_playstation_button_press(self):
            await super().on_playstation_button_press()
            eventname = sys._getframe().f_code.co_name
            await self.send(eventname.encode('utf-8'))
            self.stop = True
        # ---

    async def listen(self):
        controller = self.MyController(interface="/dev/input/js" + js_num, connecting_using_ds4drv=False)
        await controller.listen()

ds4 = WirelessController()
asyncio.run(ds4.listen())