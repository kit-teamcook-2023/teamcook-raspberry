import cv2

# 좌표 변수
x1, y1 = 0, 0  # 왼쪽 위 좌표
x2, y2 = 0, 0  # 오른쪽 아래 좌표

# 마우스 이벤트 처리 함수
def mouse_callback(event, x, y, flags, param):
    global x1, y1, x2, y2

    if event == cv2.EVENT_LBUTTONDOWN:
        if x1 == 0 and y1 == 0:
            x1, y1 = x, y
        else:
            x2, y2 = x, y
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.imshow("Image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            # 영역 좌표 계산
            x = min(x1, x2)
            y = min(y1, y2)
            w = abs(x2 - x1)
            h = abs(y2 - y1)

            print(x,y,w,h)
            # 이미지 잘라내기
            cropped_image = image[y:y+h, x:x+w]

            # 잘라낸 이미지 출력
            cv2.imshow("Cropped Image", cropped_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

image_path = '/home/cjw/flaskweb/images/test7.jpg'

image = cv2.imread(image_path)
# 이미지 창 생성 및 마우스 이벤트 콜백 함수 등록
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", mouse_callback)

# 이미지 출력
cv2.imshow("Image", image)

# 키 입력 대기
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
            break

# 윈도우 제거
cv2.destroyAllWindows()
