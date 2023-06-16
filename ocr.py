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
    
    # 이미지에 가우시안 블러 적용
    gausian_image = cv2.GaussianBlur(cropped_image, (5, 5), 0)
    
    # 이미지에 노이즈 제거
    denoised_image = cv2.fastNlMeansDenoisingColored(gausian_image, None, 10, 10, 7, 21)
    
    # 이미지를 그레이스케일로 변환
    #gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    
    # 이미지 대비 조정
    #equalized_image = cv2.equalizeHist(gray)

    # 이미지에 윤곽선 검출 적용
    #edges = cv2.Canny(gray, 50, 150)
    
    # 이미지 이진화
    #_, binary_image = cv2.threshold(resized_image, 150, 255, cv2.THRESH_BINARY)
    
    # 이미지에서 텍스트 추출
    text = pytesseract.image_to_string(denoised_image, config='--psm 6')
    
    # 추출된 텍스트 정제
    cleaned_text = re.sub(r'\D', '', text)
    
    # 추출된 텍스트가 비어 있는지 확인
    #if cleaned_text == '':
        #return ocr_data
        
    cv2.imshow('ex',denoised_image)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()
    # 추출된 텍스트를 JSON 형식으로 변환
    ocr_data = {
        'gas': int(cleaned_text)
    }
    
    # JSON 데이터 반환
    return ocr_data

# 이미지 파일 경로
image_path = '/home/cjw/flaskweb/images/test7.jpg'

# 특정 영역 좌표 (x1, y1, x2, y2)
region_of_interest = (184, 275, 231, 45)

extracted_data = perform_ocr(image_path, region_of_interest)

# 추출된 데이터가 있을 경우에만 JSON 형식으로 출력
if extracted_data is not None:
    ocr_data = json.dumps(extracted_data)
    print(ocr_data)
else:
    print("No text found in the image.")
