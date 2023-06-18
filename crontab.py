import os
from dotenv import load_dotenv
import httpx
import asyncio
import json
from ocr import perform_ocr, capture_camera

load_dotenv(verbose=True)

SERVER = os.getenv("SERVER_PATH")
CONFIG = 'config'

async def crontab():
    if os.path.isfile(CONFIG):
        with open('config', 'r') as file:
            uid = file.readline().strip()

        print(uid)
        print(SERVER)
        #camera = cv2.VideoCapture(0)
        #ret, frame = camera.read()

        #image_path = '/home/cjw/flaskweb/images/gasimage2.jpg'
        #cv2.imwrite(image_path, frame)
        image_path = '/home/cjw/flaskweb/images/gasimage.jpg'
        region_of_interest = (40, 346, 603, 96)

        ocr_data = perform_ocr(image_path, region_of_interest)

        async with httpx.AsyncClient() as client:
            data = {
                'ocr_data': ocr_data
            }
            print(data)
            json_data = json.dumps(data)
            response = await client.post(SERVER + '/gas-meter/' + uid, content=json_data)

async def schedule_job():
    while True:
        await crontab()
        await asyncio.sleep(6000)

if __name__ == "__main__":
    asyncio.run(schedule_job())
