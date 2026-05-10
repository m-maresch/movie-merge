import cv2


def show_common_frame(path1, idx1):
    cap1 = cv2.VideoCapture(path1)
    cap1.set(cv2.CAP_PROP_POS_FRAMES, idx1)
    ret, frame = cap1.read()
    if ret:
        cv2.imshow("Review Match (Press any key to continue)", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        for _ in range(10):
            cv2.waitKey(1)
    cap1.release()
