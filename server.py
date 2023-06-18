from flask import Flask, request, jsonify
import json
import os
from dotenv import load_dotenv
from ocr import perform_ocr, capture_camera

load_dotenv(verbose=True)

SERVER = os.getenv("SERVER_PATH")
CONFIG = 'config'
app = Flask(__name__)

@app.route("/ocr", methods=["GET"])
def get_ocr_data():
    #camera = cv2.VideoCapture(0)
    #ret, frame = camera.read()

    #image_path = '/home/cjw/flaskweb/images/gasimage2.jpg'
    #cv2.imwrite(image_path, frame)
    image_path = '/home/cjw/flaskweb/images/test5.jpg'
    region_of_interest = (115, 74, 331, 120)

    ocr_data = perform_ocr(image_path, region_of_interest)

    if ocr_data is not None:
        print(ocr_data)
        return jsonify(ocr_data)
    else:
        return jsonify({'error': 'No text found in the specified region.'}), 404

@app.route("/init", methods=["POST"])
def init_raspi():
    try:
        params = json.loads(request.data)
        print(params)
        uid = params['uid']
        handle_command(command="CREATE", uid=uid)
        return jsonify({"status": "success"})
    except:
        return jsonify({"status": "fail"})

@app.route("/remove", methods=["POST"])
def handle_command():
    handle_command(command="DELETE")
    return jsonify({"status": "success"})

def handle_command(command, uid=""):
    if command == 'CREATE':
        with open('config', 'w') as f:
            f.write(str(uid))
    elif command == 'DELETE':
        if os.path.isfile(CONFIG):
            os.remove(CONFIG)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
