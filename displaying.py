import asyncio
from pymodbus.client import AsyncModbusTcpClient
import struct
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

x = []
y = []

plt.style.use('dark_background')
fig, ax = plt.subplots()
plt.ion() 

async def read():
    register_addr = int(sys.argv[1])
    client = AsyncModbusTcpClient("192.168.1.3", port=502)
    connected = await client.connect()
    if not connected:
        print("Connection failed.")
        return

    freqmax = float('-inf')
    next_time = asyncio.get_event_loop().time()

    while True:
        result = await client.read_holding_registers(address=register_addr, count=2, slave=1)
        if not result.isError():
            registers = result.registers
            byte_data = struct.pack('<HH', *registers)
            float_data = struct.unpack('<f', byte_data)[0]

            freqmax = max(freqmax, float_data)
            current = asyncio.get_event_loop().time()
            if current >= next_time:
                timestamp = datetime.now()
                x.append(timestamp)
                y.append(freqmax)
                freqmax = float('-inf')
                next_time += 5
                x = x[-1000:]
                y = y[-1000:]
                ax.clear()
                ax.plot(x, y, marker='o', color='#00e676')
                ax.set_xlabel("Time")
                ax.set_ylabel("Frequency (Hz)")
                ax.set_title(f"Register {register_addr} Frequency over Time")
                ax.xaxis.set_major_locator(mdates.SecondLocator(interval=10))
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
                if x:
                    ax.set_xlim([x[-1] - timedelta(seconds=60), x[-1]])
                plt.setp(ax.get_xticklabels(), rotation=45)
                ax.grid(True)
                ax.set_facecolor('#2c2f5c')
                plt.tight_layout()
                plt.pause(0.01)
        await asyncio.sleep(0.1)  # small delay to prevent high CPU usage

asyncio.run(read())
