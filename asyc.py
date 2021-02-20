import asyncio
import time

async def wait_for(t):
    "Wait for t seconds asynchronamente"
    print(f"Vou esperar {t} segundos")
    await asyncio.sleep(t)
    print(f"Esperei {t} segundos")

async def main():
    print(f"started at {time.strftime('%X')}")
    await wait_for(2)
    await wait_for(3)
    print(f"started at {time.strftime('%X')}")

async def main2():
    task1 = asyncio.create_task(wait_for(2))

    task2 = asyncio.create_task(wait_for(3))
    print("Começando")
    print(f"started at {time.strftime('%X')}")
    await task1
    print("Segui a vida")
    await task2
    print(f"started at {time.strftime('%X')}")

#asyncio.run(main2())
