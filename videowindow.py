from tkinter import Label, Tk, Frame
# from ttkthemes import themed_tk as tk
import threading
import cv2
from PIL import Image
from PIL import ImageTk
import imutils
import socket

# s = socket.socket()

#s.bind('192.168.43.212', 8090))
#s.listen(0)



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
        self.thread2 = threading.Thread(target=self.penLoop, args = ())
        self.thread.start()
        self.thread2.start()
        self.root.wm_title("LiveEd")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

        self.drawings = []
        self.pen_properties = {
            color: (255, 0, 0)
            size: 10
        }
        self.pen_state = 0
        self.drawing_state = False
        self.pen_location = (0, 0)

        self.query_images = []

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

                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = cv2.flip(image, 1)

                self.pen_location = get_pen_location(image)

                if self.pen_state == 1:

                    if self.drawing_state:

                        drawings[-1].append(pen_location)

                    else:

                        drawings.append([])
                        drawings[-1].append(pen_location)

                else:

                    if self.drawing_state:

                        self.drawing_state = False



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

        except RuntimeError:
            print("[INFO] caught a RuntimeError")

    def process_image(self, image):

        blank_image = np.zeros(h_img, w_img, 3, dtype = np.uint8)

        for drawing in drawings:




if __name__ == "__main__":

    vs = cv2.VideoCapture(0)
    pba = videofeed(vs, r"D:/")

    pba.root.mainloop()
