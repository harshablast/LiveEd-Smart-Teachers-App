from tkinter import Label, Tk, Frame
from ttkthemes import themed_tk as tk
import threading
import cv2
from PIL import Image
from PIL import ImageTk
import imutils

class videofeed:
    def __init__(self,vs, outputPath):
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
        self.thread.start()
        self.root.wm_title("LiveEd")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def onClose(self):
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        print("[INFO] closing...")
        self.stopEvent.set()
        self.vs.release()
        self.root.quit()


    def videoLoop(self):
        # DISCLAIMER:
        # I'm not a GUI developer, nor do I even pretend to be. This
        # try/except statement is a pretty ugly hack to get around
        # a RunTime error that Tkinter throws due to threading
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                # grab the frame from the video stream and resize it to
                # have a maximum width of 300 pixels
                _, self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=1420)

                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                # if the panel is not None, we need to initialize it
                if self.panel is None:
                    self.panel = Label(image=image)
                    self.panel.image = image
                    self.panel.pack(side="left", padx=10, pady=10)
                    self.panel2 = Frame(height="1080", width="500")
                    self.panel2.pack(side="left", padx=10, pady=10)
                # otherwise, simply update the panel
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image

        except RuntimeError:
            print("[INFO] caught a RuntimeError")



vs = cv2.VideoCapture(0)

pba = videofeed(vs, r"D:/")
pba.root.mainloop()

# root = tk.ThemedTk()
# root.get_themes()
# root.set_theme("radiance")
#
# #video
# videoframe = Frame(root, height=1080, width=1353, bg="white")
#
#
# #chat
# chatframe = Frame(root, height = 1080, width=567,bg="gray")
#
#
# #packing
# videoframe.pack(side=LEFT)
# chatframe.pack(side=LEFT)
#
# root.mainloop()