import os
from dotenv import load_dotenv
import httpx
import asyncio
import json
from ocr import perform_ocr

load_dotenv(verbose=True)

SERVER = os.getenv("SERVER_PATH")
CONFIG = 'config'

async def crontab():
    if os.path.isfile(CONFIG):
        with open('config', 'r') as file:
            uid = file.readline().strip()

        print(uid)
        print(SERVER)
        image_path = '/home/cjw/flaskweb/images/test5.jpg'
        region_of_interest = (115, 74, 331, 120)

        ocr_data = perform_ocr(image_path, region_of_interest)

        async with httpx.AsyncClient() as client:
            data = {
                'ocr_data': "123456"
            }
            json_data = json.dumps(data)
            response = await client.post(SERVER + '/gas-meter/' + uid, content=json_data)

async def schedule_job():
    while True:
        await crontab()
        await asyncio.sleep(6000)

if __name__ == "__main__":
    asyncio.run(schedule_job())
