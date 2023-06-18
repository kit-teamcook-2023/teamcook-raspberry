import cv2

x1, y1 = 0, 0
x2, y2 = 0, 0

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

            x = min(x1, x2)
            y = min(y1, y2)
            w = abs(x2 - x1)
            h = abs(y2 - y1)

            print(x,y,w,h)
            cropped_image = image[y:y+h, x:x+w]

            cv2.imshow("Cropped Image", cropped_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

image_path = '/home/cjw/flaskweb/images/gasimage2.jpg'

image = cv2.imread(image_path)
cv2.namedWindow("Image")

cv2.setMouseCallback("Image", mouse_callback)

cv2.imshow("Image", image)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
            break

cv2.destroyAllWindows()
