import asyncio
from pymodbus.client import AsyncModbusTcpClient
import struct
import csv

async def read():
    client = AsyncModbusTcpClient("192.168.1.3", port=502)
    connected = await client.connect()
    if not connected:
        print("Connection failed.")
        with open('frequency.csv', 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["not connected"])
        return

    overallmax =[0,0,0,0]
    next_time = asyncio.get_event_loop().time()

    while True:
        result = await client.read_holding_registers(address=0, count=8, slave=1)
        if not result.isError():
            registers = result.registers  
            float_values = []
            for i in range(0, 8, 2):
                byte_data = struct.pack('<HH', registers[i], registers[i+1])  
                float_val = struct.unpack('<f', byte_data)[0]
                float_values.append(float_val)
            overallmax[0]=max(overallmax[0],float_values[0])
            overallmax[1]=max(overallmax[1],float_values[1])
            overallmax[2]=max(overallmax[2],float_values[2])
            overallmax[3]=max(overallmax[3],float_values[3])
            current = asyncio.get_event_loop().time()
            if current >= next_time:
                with open('frequency.csv', 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(float_values)
                next_time += 5
        await asyncio.sleep(0.1)  

asyncio.run(read())
