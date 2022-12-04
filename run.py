import Momento
import nest_asyncio
import asyncio
nest_asyncio.apply()


async def main():
    await Momento.run()

if __name__ == "__main__":
    # run async func main()
    asyncio.run(main())