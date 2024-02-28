import time
import asyncio

# def drinkWater():
#     print("start")
#     time.sleep(3)
#     print("stop")
#     return "ready"

# def eatFood():
#     print("start")
#     time.sleep(2)
#     print("stop")
#     return "ready"

# def main():
#     start_time = time.time()
    
#     result_water=drinkWater()
#     result_food=eatFood()
    
#     end_time=time.time()
#     elapsed_time = end_time-start_time
#     print(f"Result for Drinking Water: {result_water}")
#     print(f"Result for Eating Food: {result_food}")
#     print(f"Total Execution Time:{elapsed_time}")

# if __name__ == "__main__":
#     main()  
    

async def drinkWater():
    print("start")
    await asyncio.sleep(3)
    print("stop")
    return "ready"

async def eatFood():
    print("start")
    await asyncio.sleep(2)
    print("stop")
    return "ready"

async def main():
    start_time = time.time()
    
    # batch = asyncio.gather(drinkWater(), eatFood())
    # result_water,result_food= await batch
    
    water_task = asyncio.create_task(drinkWater())
    food_task = asyncio.create_task(eatFood())
    
    result_water = await water_task
    result_food = await food_task
    
    end_time=time.time()
    elapsed_time = end_time - start_time
    print(f"Result for Drinking Water: {result_water}")
    print(f"Result for Eating Food: {result_food}")
    print(f"Total Execution Time:{elapsed_time}")

if __name__ == "__main__":
    asyncio.run(main())  