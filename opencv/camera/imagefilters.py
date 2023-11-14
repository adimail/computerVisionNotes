import sys
import cv2
import numpy as np

PREVIEW = 0
BLUR = 1
FEATURES = 2
CANNY = 3

feature_params = dict(maxCorners = 500,
                      qualityLevel = 0.2,
                      minDistance = 15,
                      blockSize = 9)

s=0
if len(sys.argv)>1:
    s=sys.argv[1]

image_filter = PREVIEW
alive = True

winName = "Preview Window"
cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
result = None

source = cv2.VideoCapture(s)

while alive:
    hasFrame, frame = source.read()

    if not hasFrame:
        break

    frame = cv2.flip(frame,1)
    if image_filter == PREVIEW:
        result = frame
    elif image_filter == CANNY:
        result = cv2.Canny(frame, 145, 150)
    elif image_filter == BLUR:
        result = cv2.blur(frame, (13,13))
    elif image_filter == FEATURES:
        result = frame
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners = cv2.goodFeaturesToTrack(frame_gray, **feature_params)
        if corners is not None:
            for x,y in np.float32(corners).reshape(-1,2):
                cv2.circle(result, (int(x), int(y)), 10, (0, 225, 0), 1)

    cv2.imshow(winName, result)

    key = cv2.waitKey(1)
    if key==ord('Q') or key == ord('q') or key == 27:
        alive = False
    elif key==ord('C') or key==ord('c'):
        image_filter = CANNY
    elif key==ord('B') or key==ord('b'):
        image_filter = BLUR
    elif key==ord('F') or key==ord('f'):
        image_filter = FEATURES
    elif key==ord('P') or key==ord('p'):
        image_filter = PREVIEW
    
source.release()
cv2.destroyWindow(winName)