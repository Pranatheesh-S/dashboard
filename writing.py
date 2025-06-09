import sys
import asyncio
import struct
from pymodbus.client import AsyncModbusTcpClient

async def write_frequency(value):
    float_bytes = struct.pack('<f', value)
    registers = struct.unpack('<HH', float_bytes)

    client = AsyncModbusTcpClient("192.168.1.3", port=502)
    connected = await client.connect()
    if not connected:
        print("Connection failed.")
        return

    result = await client.write_registers(address=0, values=registers, slave=1)
    if result.isError():
        print("Failed to write registers")
    else:
        print(f"Wrote frequency {value} Hz as {registers}")

    await client.close()

if __name__=='__main__':
    asyncio.run(write_frequency(sys.argv[1]))
