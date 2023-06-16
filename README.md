# teamcook-raspberry
라즈베리파이 코드 보관용

### !각 코드의 경로는 코드 및 이미지를 다운 받아 각자 경로에 맞춰 수정!

### 요구하는 pip 설치 사항
* pip install camera : 기본 카메라 라이브러리
* pip install Flask : Flask 서버 제작
* pip install python-dotenv : 서버 주소 저장
* pip install pytesseract : pytesseract ocr 실행
* pip install cv2 : 이미지 전처리 라이브러리

### 사용한 OCR 도구 Tesseract 설치법
1. sudo apt install tesseact-ocr
2. 설치 파일 실행
3. 원하는 언어 추가(이번 코드는 숫자 OCR을 요구하므로 아무거나 추가했다.)
4. 경로(찾기 쉬운곳으로)
5. (경로 추가가 안되었을 경우) 시스템 환경 변수에서 방금 설치한 경로 추가

### 사용한 cv2 전처리 기능
* image[y:y+h, x:x+w] : 이미지의 원하는 부분의 좌표를 가져와 자른다
* cv2.resize(image, (800, 200)) : 이미지를 원하는 크기로 재조정한다.
* cv2.GaussianBlur(image, (x, y), 0) : 이미지의 가우시안 블러를 적용하여 이미지를 흐리게 만든다 '(x, y)'는 가우시안 커널의 크기이며 0은 x,y축 표준편차이다.
*  cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21) : 이미지에서 노이즈를 제거한다. 10과 10은 필터링과 사전필터의 강도이며, 7은 사전 필터의 커널 크기이며, 21은 비슷한 픽셀을 찾기 위한 사전 필터 이웃의 크기이다.
*  cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) : 이미지를 그레이스케일로 변환한다.
*  cv2.equalizeHist(image) : 그레이스케일 된 이미지의 대비를 조정한다.
*  cv2.Canny(image, 50, 150) : 그레이스케일 이미지에서 윤곽선을 검출한다.
*  cv2.threshold(image, 150, 255, cv2.THRESH_BINARY) : 이미지를 이진화한다. 그레이스케일과는 다르게 완전히 흑백화한다. 임계값을 기준으로 픽셀을 검은색(0) 또는 흰색(255)으로 설정한다.
*  cv2.convertScaleAbs(image, alpha, beta), cv2.cvtColor(image, cv2.COLOR_BGR2HSV) : 이미지의 밝기 및 채도 조정을 한다.
*  cv2.bitwise_not(image) : 이미지의 모든 색을 반전시킨다.
