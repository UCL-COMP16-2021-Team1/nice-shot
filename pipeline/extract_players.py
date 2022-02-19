import cv2
import numpy as np

def extract_players(cap):
    _, old_frame = cap.read()
    while cap.isOpened():
        ret, new_frame = cap.read()
        if not ret:
            break
        diff = cv2.absdiff(old_frame, new_frame)
        diff = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)

        diff = cv2.GaussianBlur(diff, (5,5), 0)
        _, diff_threshold = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)

        morph_kernel = np.ones((5,5))
        diff_threshold = cv2.dilate(diff_threshold, morph_kernel, iterations=20)
        
        contours, _ = cv2.findContours(diff_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        annotated_frame = new_frame.copy()

        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(annotated_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        old_frame = new_frame
        cv2.imshow("annotated frame", annotated_frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
