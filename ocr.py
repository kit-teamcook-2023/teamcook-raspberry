import cv2
import pytesseract
import json
import re
import numpy as np

x1, y1, x2, y2 = 0, 0, 0, 0
roi = None
image = None

#관심영역지정
def mouse_callback(event, x, y, flags, param):
    global x1, y1, x2, y2, roi, image

    if event == cv2.EVENT_LBUTTONDOWN:
        if x1 == 0 and y1 == 0:
            x1, y1 = x, y
        else:
            x2, y2 = x, y
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.imshow("Image", image)

            x = min(x1, x2)
            y = min(y1, y2)
            w = abs(x2 - x1)
            h = abs(y2 - y1)

            roi = (x, y, w, h)

#상황에 따라 알맞은 필터 적용

def perform_ocr(image_path, region):
    ocr_data = {
        'gas' : 0
    }
    img = cv2.imread(image_path)
    
    #특정 영역 추출
    x, y, w, h = region
    img = img[y:y+h, x:x+w]
    #img = cv2.resize(img, (800, 200))
    
    # 이미지 반전
    #img = cv2.bitwise_not(img)
    
    # 밝기 조정
    bright = 10
    img = cv2.convertScaleAbs(img, alpha=1.0, beta=bright)

    # 채도 조정
    saturation = 1.0
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img[..., 1] = img[..., 1] * saturation
    img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    
    # 가우시안 블러 적용
    #img = cv2.GaussianBlur(img, (5, 5), 0)
    
    # 노이즈 제거
    #img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    
    #이미지 샤프닝
    kernel = np.array([[0, -1, 0],
                       [-1, 6, -1],
                       [0, -1, 0]], dtype=np.float32)
                       
    img = cv2.filter2D(img, -1, kernel)
    
    # 그레이스케일로 변환
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 대비 조정
    #img = cv2.equalizeHist(img)

    # 윤곽선 검출 적용
    #img = cv2.Canny(img, 50, 150)
    
    # 이진화
    #_, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
    
    cv2.imshow('ex',img)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()
    
    # 텍스트 추출
    text = pytesseract.image_to_string(img, config='--psm 6')
    
    # 한글 문자만 필터링
    #KOR_text = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣]', '', text)
    
    # 영어 문자만 필터링
    #ENG_text = re.sub(r'[^a-zA-Z]', '', text)
    
    # 숫자만 필터링
    #cleaned_text = re.sub(r'\D', '', text)
    
    # 영어와 숫자만 필터링
    cleaned_text = re.sub(r'\D', '', text)
    ENG_text = re.sub(r'[^a-zA-Z]', '', text)
    
    # 추출된 텍스트가 비어 있는지 확인
    if cleaned_text == '':
        return ocr_data
    
    #추출(숫자만)
    #ocr_data = {
    #    'gas': int(cleaned_text)
    #}
    
    #추출(문자만)
    #ocr_data = {
    #    'gas': cleaned_text.strip()
    #}
    
    #추출(문자, 숫자)
    ocr_data = {
        'english': ENG_text,
        'num': int(cleaned_text)
    }
    
    return ocr_data

def capture_camera():
    camera = cv2.VideoCapture(0)
    
    ret, frame = camera.read()
    
    camera.release()
    
    return frame

if __name__ == "__main__":
    #camera = cv2.VideoCapture(0)
    #ret, frame = camera.read()

    #image_path = '/home/cjw/flaskweb/images/test5.jpg'
    #cv2.imwrite(image_path, frame)

    image_path = '/home/cjw/flaskweb/images/test5.jpg'
    
    image = cv2.imread(image_path)
    cv2.namedWindow("Image")

    cv2.setMouseCallback("Image", mouse_callback)

    cv2.imshow("Image", image)

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27 or roi is not None:
            break

    cv2.destroyAllWindows()
    print(roi)

    region_of_interest = roi

    extracted_data = perform_ocr(image_path, region_of_interest)

    if extracted_data is not None:
        ocr_data = json.dumps(extracted_data)
        print(ocr_data)
    else:
        print("No text found in the image.")
