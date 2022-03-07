import cv2
import json

# create data folder.

def create_images():
    with open('data/test_shot.json') as file:
        data = json.load(file)

        current_frame: int = 0
        shotCount: int = 0;

        cam = cv2.VideoCapture("data/p1_backhand_s1.mp4") # get directory
        print(cam.isOpened())
        
        for shot in data['shots']:
            while (True):
                _, frame = cam.read()
                
                if current_frame == shot['start_frame_idx']:
                    imgName = "data/shot" + str(shotCount) + '.jpg'
                    cv2.imwrite(imgName, frame)
                    current_frame += 1
                    shotCount += 1
                    break
                current_frame += 1
        
        cam.release()
        cv2.destroyAllWindows()
