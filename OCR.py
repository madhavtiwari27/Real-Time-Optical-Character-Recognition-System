import os
from pathlib import Path
import sys
from datetime import datetime
import time
import threading
from threading import Thread

import cv2
import numpy
import pytesseract

import LIG


def tesseract_location(root):
    
    try:
        pytesseract.pytesseract.tesseract_cmd = root
    except FileNotFoundError:
        print("Please double check the Tesseract file directory or ensure it's installed.")
        sys.exit(1)


class RateCounter:
    

    def __init__(self):
        self.start_time = None
        self.iterations = 0

    def start(self):
        
        self.start_time = time.perf_counter()
        return self

    def increment(self):
        
        self.iterations += 1

    def rate(self):
        
        elapsed_time = (time.perf_counter() - self.start_time)
        return self.iterations / elapsed_time


class VideoStream:
    

    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        
        while not self.stopped:
            (self.grabbed, self.frame) = self.stream.read()

    def get_video_dimensions(self):
        
        width = self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)
        return int(width), int(height)

    def stop_process(self):
        
        self.stopped = True


class OCR:

    
    def __init__(self):
        self.boxes = None
        self.stopped = False
        self.exchange = None
        self.language = None
        self.width = None
        self.height = None
        self.crop_width = None
        self.crop_height = None

    def start(self):
        
        Thread(target=self.ocr, args=()).start()
        return self

    def set_exchange(self, video_stream):
        
        self.exchange = video_stream

    def set_language(self, language):
        
        self.language = language

    def ocr(self):
        
        while not self.stopped:
            if self.exchange is not None:  
                frame = self.exchange.frame

                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                               

                frame = frame[self.crop_height:(self.height - self.crop_height),
                              self.crop_width:(self.width - self.crop_width)]

                self.boxes = pytesseract.image_to_data(frame, lang=self.language)

    def set_dimensions(self, width, height, crop_width, crop_height):
       
        self.width = width
        self.height = height
        self.crop_width = crop_width
        self.crop_height = crop_height

    def stop_process(self):
      
        self.stopped = True


def capture_image(frame, captures=0):
   
    cwd_path = os.getcwd()
    Path(cwd_path + '/images').mkdir(parents=False, exist_ok=True)

    now = datetime.now()
    
    name = "OCR " + now.strftime("%Y-%m-%d") + " at " + now.strftime("%H:%M:%S") + '-' + str(captures + 1) + '.jpg'
    path = 'images/' + name
    cv2.imwrite(path, frame)
    captures += 1
    print(name)
    return captures


def views(mode: int, confidence: int):
   
    conf_thresh = None
    color = None

    if mode == 1:
        conf_thresh = 75  
        color = (0, 255, 0)  

    if mode == 2:
        conf_thresh = 0  
        if confidence >= 50:
            color = (0, 255, 0)  
        else:
            color = (0, 0, 255)  

    if mode == 3:
        conf_thresh = 0  
        color = (int(float(confidence)) * 2.55, int(float(confidence)) * 2.55, 0)

    if mode == 4:
        conf_thresh = 0  
        color = (0, 0, 255)  

    return conf_thresh, color


def put_ocr_boxes(boxes, frame, height, crop_width=0, crop_height=0, view_mode=1):
    

    if view_mode not in [1, 2, 3, 4]:
        raise Exception("A nonexistent view mode was selected. Only modes 1-4 are available")

    text = ''  
    if boxes is not None:  
        for i, box in enumerate(boxes.splitlines()):  
            box = box.split()
            if i != 0:
                if len(box) == 12:
                    x, y, w, h = int(box[6]), int(box[7]), int(box[8]), int(box[9])
                    conf = box[10]
                    word = box[11]
                    x += crop_width  
                    y += crop_height

                    conf_thresh, color = views(view_mode, int(float(conf)))

                    if int(float(conf)) > conf_thresh:
                        cv2.rectangle(frame, (x, y), (w + x, h + y), color, thickness=1)
                        text = text + ' ' + word

        if text.isascii():  
            cv2.putText(frame, text, (5, height - 5), cv2.FONT_HERSHEY_DUPLEX, 1, (200, 200, 200))

    return frame, text


def put_crop_box(frame: numpy.ndarray, width: int, height: int, crop_width: int, crop_height: int):
    
    cv2.rectangle(frame, (crop_width, crop_height), (width - crop_width, height - crop_height),
                  (255, 0, 0), thickness=1)
    return frame


def put_rate(frame: numpy.ndarray, rate: float) -> numpy.ndarray:
    
    cv2.putText(frame, "{} Iterations/Second".format(int(rate)),
                (10, 35), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255))
    return frame


def put_language(frame: numpy.ndarray, language_string: str) -> numpy.ndarray:
    
    cv2.putText(frame, language_string,
                (10, 65), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255))
    return frame


def ocr_stream(crop: list[int, int], source: int = 0, view_mode: int = 1, language=None):
   
    captures = 0  

    video_stream = VideoStream(source).start()  
    img_wi, img_hi = video_stream.get_video_dimensions()

    if crop is None:  
        cropx, cropy = (200, 200)  
    else:
        cropx, cropy = crop[0], crop[1]
        if cropx > img_wi or cropy > img_hi or cropx < 0 or cropy < 0:
            cropx, cropy = 0, 0
            print("Impossible crop dimensions supplied. Dimensions reverted to 0 0")

    ocr = OCR().start()  
    print("OCR stream started")
    print("Active threads: {}".format(threading.activeCount()))
    ocr.set_exchange(video_stream)
    ocr.set_language(language)
    ocr.set_dimensions(img_wi, img_hi, cropx, cropy)  

    cps1 = RateCounter().start()
    lang_name = LIG.language_string(language)  

    
    print("\nPUSH c TO CAPTURE AN IMAGE. PUSH q TO VIEW VIDEO STREAM\n")
    while True:

        
        pressed_key = cv2.waitKey(1) & 0xFF
        if pressed_key == ord('q'):
            video_stream.stop_process()
            ocr.stop_process()
            print("OCR stream stopped\n")
            print("{} image(s) captured and saved to current directory".format(captures))
            break

        frame = video_stream.frame  

        
        frame = put_rate(frame, cps1.rate())
        frame = put_language(frame, lang_name)
        frame = put_crop_box(frame, img_wi, img_hi, cropx, cropy)
        frame, text = put_ocr_boxes(ocr.boxes, frame, img_hi,
                                    crop_width=cropx, crop_height=cropy, view_mode=view_mode)
        

        
        if pressed_key == ord('c'):
            print('\n' + text)
            captures = capture_image(frame, captures)

        cv2.imshow("realtime OCR", frame)
        cps1.increment()  
