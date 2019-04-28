from tkinter import Label, Tk, Frame
from ttkthemes import themed_tk as tk
import threading
import cv2
from PIL import Image
from PIL import ImageTk
import imutils
import socket

s = socket.socket()

s.bind(('192.168.43.115', 8090))
s.listen(0)



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

    def getData(self):
        while True:

            client, addr = s.accept()

            while True:
                content = client.recv(32)
                arduinoData = content.decode('ascii').strip()

                if len(content) == 0:
                    break

                else:
                    return arduinoData

            print("Closing connection")
            client.close()

    def videoLoop(self):
        try:

            while not self.stopEvent.is_set():
                _, self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=1420)

                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = cv2.flip(image, 1)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                # if the panel is None, we need to initialize it
                if self.panel is None:
                    self.panel = Label(image=image)
                    self.panel.image = image
                    self.panel.pack(side="left", padx=10, pady=10)
                    self.panel2 = Frame(self.root, height="1080", width="500", bg="red")
                    self.panel2.pack(side="left", padx=10, pady=10)
                    Label(self.panel2, text='Sir, I dont understand why you use Tkinter', borderwidth=1).pack(
                        side="top")
                    Label(self.panel2, text=self.getData(), borderwidth=1).pack(side="top")
                # otherwise, simply update the panel
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image

        except RuntimeError:
            print("[INFO] caught a RuntimeError")


vs = cv2.VideoCapture(0)

pba = videofeed(vs, r"D:/")

# comments shit


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
