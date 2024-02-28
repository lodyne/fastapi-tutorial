import asyncio

async def main():
    print("hello world")
    # task = asyncio.create_task(txt("waiting"))
    # await task
    asyncio.create_task(txt("waiting"))
    await asyncio.sleep(5)
    # await txt("waiting")
    print("Good Morning")
    
async def txt(text):
    print(text)
    await asyncio.sleep(10)
    
    
asyncio.run(main())