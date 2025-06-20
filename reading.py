import csv
import asyncio
import struct
from datetime import datetime
from datetime import datetime
from pymodbus.client import AsyncModbusTcpClient

async def read():
    client = AsyncModbusTcpClient("192.168.1.3", port=502)
    connected = await client.connect()
    if not connected:
        print("Connection failed.")
        return
    overallmax = -1
    next_time = asyncio.get_event_loop().time()

    while True:
        result = await client.read_holding_registers(address=0, count=2, slave=1)
        if not result.isError():
            registers = result.registers
            byte_data = struct.pack('<HH', *registers)
            float_data = struct.unpack('<f', byte_data)[0]
            overallmax = max(float_data, overallmax)
            current = asyncio.get_event_loop().time()
            if current >= next_time:
                with open('frequency.csv', 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows([[overallmax]])

                next_time += 5
                # All matplotlib plotting code has been removed

asyncio.run(read())
