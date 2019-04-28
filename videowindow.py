from tkinter import Label, Tk, Frame
# from ttkthemes import themed_tk as tk
import threading
import numpy as np
import cv2
from PIL import Image
from PIL import ImageTk
import imutils
import socket
import wave
import os
import pyaudio
import speech_recognition as sr
import shutil
from google_images_search import GoogleImagesSearch

s = socket.socket()
s.bind(('192.168.43.115', 8090))

s.listen(0)
r = sr.Recognizer()
mic = sr.Microphone(device_index=5)
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 2
API_KEY = 'AIzaSyCki8KIN6wWL06X5bvbVVykYBrLgQoMofw'
CX = '009518592146397428949:hm3iqr4gpv4'
gis = GoogleImagesSearch(API_KEY, CX)
WAVE_OUTPUT_FILENAME = "recorded_audio.wav"
frames = []

query_images = {
    'images': [],
    'coords': []
}


class videofeed:
    def __init__(self, vs, outputPath):

        self.vs = vs
        self.outputPath = outputPath
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.root = Tk()
        self.panel = None
        self.panel2 = None
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread2 = threading.Thread(target=self.penLoop, args=())
        self.thread3 = threading.Thread(target=self.get_image, args=())
        self.thread.start()
        self.thread2.start()
        self.root.wm_title("LiveEd")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

        self.drawings = []
        self.pen_properties = {
            "color": (255, 0, 0),
            "size": 10
        }
        self.pen_state = 0
        self.drawing_state = False
        self.pen_location = (0, 0)
        self.query_image_coord = (0, 0)
        self.query_image = ''
        self.get_image_flag = False

    def get_image(self):
        # Audio
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
        print("recording...")
        # frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
        print("finished recording")
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        raud = sr.AudioFile(r'D:\LiveED\LiveEd_2\recorded_audio.wav')
        with raud as source:
            raudio = r.record(source)
            word = r.recognize_google(raudio)
            _search_params = {
                'q': word,
                'num': 1,
                'searchType': 'image'
            }
            if os.path.exists(r"D:\LiveED\LiveEd_2\pics"):
                shutil.rmtree(r'D:\LiveED\LiveEd_2\pics')
            gis.search(search_params=_search_params, path_to_dir=r'D:\LiveED\LiveEd_2\pics')

            pic = os.listdir(r'D:\LiveED\LiveEd_2\pics')[0]
            global picfname
            picfname = os.path.join('D:\LiveED\LiveEd_2\pics', pic)

            query_img = cv2.imread(picfname)
            query_img = cv2.resize(query_img, (128, 128))
            query_images['images'].append(query_img)
            query_images['coords'].append(1)
            print("Your word: " + word)
        buffer = 1
        render_image = True
        self.query_image = picfname

    def onClose(self):
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        print("[INFO] closing...")
        self.stopEvent.set()
        self.vs.release()
        self.root.quit()

    def penLoop(self):

        while True:

            client, addr = s.accept()

            while True:

                content = client.recv(32)
                arduinoData = content.decode('ascii').strip()

                if len(content) == 0:
                    break

                else:
                    self.pen_state = arduinoData

            print("Closing connection")
            client.close()

    def videoLoop(self):
        try:

            while not self.stopEvent.is_set():
                _, self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=800)

                self.frame = cv2.flip(self.frame, 1)

                self.pen_location = self.get_pen_location(self.frame)

                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                # image = cv2.flip(image, 1)

                if self.pen_state == '1':

                    print('elfaks')

                    if self.drawing_state:

                        self.drawings[-1].append(self.pen_location)

                    else:

                        self.drawing_state = True
                        self.drawings.append([])
                        self.drawings[-1].append(self.pen_location)

                else:

                    if self.drawing_state:
                        self.drawing_state = False

                if self.pen_state == '2':

                    if (self.get_image_flag == False):
                        self.get_image_flag = True
                        self.query_image_coord = self.pen_location
                        self.query_image = ''
                        self.thread3.start()

                if (self.get_image_flag):

                    if self.query_image != '':
                        self.get_image_flag = False

                image = self.process_image(image)

                tkinter_image = Image.fromarray(image)
                tkinter_image = ImageTk.PhotoImage(tkinter_image)

                # if the panel is None, we need to initialize it
                if self.panel is None:
                    self.panel = Label(image=tkinter_image)
                    self.panel.image = tkinter_image
                    self.panel.pack(side="left", padx=10, pady=10)
                    self.panel2 = Frame(self.root, height="1080", width="300", bg="red")
                    self.panel2.pack(side="left", padx=10, pady=10)
                    Label(self.panel2, text='Sir, I dont understand why you use Tkinter', borderwidth=1).pack(
                        side="top")
                    Label(self.panel2, text="lol2", borderwidth=1).pack(side="top")
                # otherwise, simply update the panel
                else:
                    self.panel.configure(image=tkinter_image)
                    self.panel.image = tkinter_image

                print(self.pen_state)

        except RuntimeError:
            print("[INFO] caught a RuntimeError")

    def process_image(self, image):

        for drawing in self.drawings:

            for i in range(len(drawing) - 1):
                cv2.line(image, drawing[i], drawing[i + 1], (255, 0, 0), 2)

        if self.query_image != '':
            print(self.query_image)
            q_img = cv2.imread(self.query_image)
            q_img = cv2.resize(q_img, (150, 150))

            image[self.query_image_coord[1]:self.query_image_coord[1] + 150,
            self.query_image_coord[0]:self.query_image_coord[0] + 150] = q_img

        cv2.circle(image, self.pen_location, 2, (0, 255, 0), -1)

        return image

    def get_pen_location(self, img):

        kernel_size = 5
        kernel1 = np.ones((kernel_size, kernel_size), np.float32) / kernel_size / kernel_size

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower_1 = np.array([0, 120, 130], dtype=np.uint8)
        upper_1 = np.array([10, 200, 255], dtype=np.uint8)

        lower_2 = np.array([170, 120, 130], dtype=np.uint8)
        upper_2 = np.array([180, 200, 255], dtype=np.uint8)

        mask_1 = cv2.inRange(hsv, lower_1, upper_1)
        mask_2 = cv2.inRange(hsv, lower_2, upper_2)

        mask = mask_1 + mask_2

        res = cv2.bitwise_and(hsv, hsv, mask=mask)
        res = cv2.erode(res, kernel1, iterations=1)
        res = cv2.dilate(res, kernel1, iterations=1)

        rgb = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)

        gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

        gray = cv2.GaussianBlur(gray, (11, 11), 0)
        ret, gray = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

        white_coords = np.argwhere(mask == 255)

        if white_coords.shape == (0, 2):
            topmost_last = (360, 512)
        else:
            topmost_last = np.average(white_coords, axis=0)
            topmost_last = topmost_last.astype(np.int)
            topmost_last[0], topmost_last[1] = topmost_last[1], topmost_last[0]
            topmost_last = tuple(topmost_last)

        return topmost_last


if __name__ == "__main__":
    vs = cv2.VideoCapture(0)
    pba = videofeed(vs, r"D:/")

    pba.root.mainloop()

    # while(1):
    #
    #     _, img = vs.read()
    #
    #     kernel_size = 5
    #     kernel1 = np.ones((kernel_size, kernel_size), np.float32) / kernel_size / kernel_size
    #
    #     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #
    #     lower_1 = np.array([0, 120, 130], dtype=np.uint8)
    #     upper_1 = np.array([10, 200, 255], dtype=np.uint8)
    #
    #     lower_2 = np.array([170, 120, 130], dtype=np.uint8)
    #     upper_2 = np.array([180, 200, 255], dtype=np.uint8)
    #
    #     mask_1 = cv2.inRange(hsv, lower_1, upper_1)
    #     mask_2 = cv2.inRange(hsv, lower_2, upper_2)
    #
    #     mask = mask_1 + mask_2
    #
    #     res = cv2.bitwise_and(hsv, hsv, mask=mask)
    #     res = cv2.erode(res, kernel1, iterations=1)
    #     res = cv2.dilate(res, kernel1, iterations=1)
    #
    #     rgb = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)
    #
    #     gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
    #
    #     gray = cv2.GaussianBlur(gray, (11, 11), 0)
    #     ret, gray = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    #
    #
    #
    #     white_coords = np.argwhere(mask == 255)
    #
    #     if white_coords.shape == (0, 2):
    #         topmost_last = (360, 512)
    #     else:
    #         topmost_last = np.average(white_coords, axis=0)
    #         topmost_last = topmost_last.astype(np.int)
    #         topmost_last[0], topmost_last[1] = topmost_last[1], topmost_last[0]
    #         topmost_last = tuple(topmost_last)
    #
    #     cv2.circle(img, topmost_last, 2, (0, 255, 0), -1)
    #
    #     cv2.imshow('Gray', mask)
    #     cv2.imshow('Img', img)
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break


