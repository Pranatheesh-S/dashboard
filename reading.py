import csv
import asyncio
import struct
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from pymodbus.client import AsyncModbusTcpClient

async def read():
    client = AsyncModbusTcpClient("192.168.1.3", port=502)
    connected = await client.connect()
    if not connected:
        print("Connection failed.")
        return
    x = []
    y = []
    overallmax=-1
    overallmin=float('inf')
    plt.plot(x,y)
    freqmax = float('-inf')
    next_time = asyncio.get_event_loop().time()
    while True:
        result = await client.read_holding_registers(address=0, count=2, slave=1)
        if not result.isError():
            registers = result.registers
            byte_data = struct.pack('<HH', *registers)
            float_data = struct.unpack('<f', byte_data)[0]
            freqmax = max(freqmax, float_data)
            overallmin=min(float_data,overallmin)
            overallmax=max(float_data,overallmax)
            print(float_data)
            current = asyncio.get_event_loop().time()
            with open('frequency.csv','w',newline='') as f:
                writer=csv.writer(f)
                csv.writerows([[float_data,overallmin,overallmax]])
            if current >= next_time:
                timestamp = datetime.now()
                x.append(timestamp)
                y.append(freqmax)
                freqmax = float('-inf')
                next_time += 0.5
                x = x[-1000:]
                y = y[-1000:]
                plt.clf()
                plt.plot(x, y, marker='o',color='#00e676')
                plt.xlabel("Time")
                plt.ylabel("Frequency (Hz)")
                plt.title("Frequency over Time")
                plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=10))
                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
                if x:
                    plt.xlim([x[-1] - timedelta(seconds=60), x[-1]])
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.grid(True)
                plt.gca().set_facecolor('#2c2f5c')
                plt.savefig("graph.png")

asyncio.run(read())
