import cv2
import pytesseract
import json
import re

#상황에 따라 알맞은 필터 적용

def perform_ocr(image_path, region):
    ocr_data = {
        'gas' : 0
    }
    image = cv2.imread(image_path)
    
    # 특정 영역 추출
    x, y, w, h = region
    cropped_image = image[y:y+h, x:x+w]
    #resized_image = cv2.resize(cropped_image, (800, 200))
    
    # 밝기 조정
    #bright = 50
    #adjusted_image = cv2.convertScaleAbs(cropped_image, alpha=1.0, beta=bright)

    # 채도 조정
    #saturation = 1.5
    #hsv_image = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2HSV)
    #hsv_image[..., 1] = hsv_image[..., 1] * saturation
    #saturated_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    
    # 이미지 반전
    inverted_image = cv2.bitwise_not(cropped_image)
    
    # 가우시안 블러 적용
    gausian_image = cv2.GaussianBlur(inverted_image, (5, 5), 0)
    
    # 노이즈 제거
    denoised_image = cv2.fastNlMeansDenoisingColored(gausian_image, None, 10, 10, 7, 21)
    
    # 그레이스케일로 변환
    #gray_image = cv2.cvtColor(denoised_image, cv2.COLOR_BGR2GRAY)
    
    # 대비 조정
    #equalized_image = cv2.equalizeHist(gray_image)

    # 곽선 검출 적용
    #edges_image = cv2.Canny(equalized_image, 50, 150)
    
    # 이진화
    #_, binary_image = cv2.threshold(resized_image, 150, 255, cv2.THRESH_BINARY)
    
    # 텍스트 추출
    text = pytesseract.image_to_string(denoised_image, config='--psm 6')
    
    # 추출된 텍스트 정제
    cleaned_text = re.sub(r'\D', '', text)
    
    # 추출된 텍스트가 비어 있는지 확인
    if cleaned_text == '':
        return ocr_data
        
    cv2.imshow('ex',denoised_image)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()
    
    ocr_data = {
        'gas': int(cleaned_text)
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

    #image_path = '/home/cjw/flaskweb/images/gasimage2.jpg'
    #cv2.imwrite(image_path, frame)

    image_path = '/home/cjw/flaskweb/images/gasimage.jpg'

    # 특정 영역 좌표 (x1, y1, x2, y2)
    region_of_interest = (40, 346, 603, 96)

    extracted_data = perform_ocr(image_path, region_of_interest)

    if extracted_data is not None:
        ocr_data = json.dumps(extracted_data)
        print(ocr_data)
    else:
        print("No text found in the image.")
