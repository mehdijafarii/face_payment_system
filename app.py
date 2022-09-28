import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import time
import datetime as dt
import argparse
from tkinter import messagebox
import os

from f_recognition import compare_faces

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.ok=False

        # open video source (by default this will try to open the computer webcam)
        self.vid = VideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_snapshot=tk.Button(window, text="Snapshot", command=self.snapshot)
        self.btn_snapshot.pack(side=tk.LEFT)

        # quit button
        self.btn_quit=tk.Button(window, text='QUIT', command=quit)
        self.btn_quit.pack(side=tk.LEFT)

        # The entery widget
        self.user_input=tk.Entry(window, width=20)
        self.user_input.pack(side=tk.RIGHT)

        self.price_lable = tk.Label(window, text="Amount: ")
        self.price_lable.pack(side=tk.RIGHT)

        self.id_input=tk.Entry(window, width=5)
        self.id_input.pack(side=tk.RIGHT)

        self.id_lable = tk.Label(window, text="ID: ")
        self.id_lable.pack(side=tk.RIGHT)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay=12
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret,frame=self.vid.get_frame()
        # * check if the user did put anything.
        if self.user_input.index("end") != 0 and self.id_input.index("end") != 0:
            input_money = self.user_input.get()
            if ret:
                buyer_tp=self.id_input.get()
                
                cv2.imwrite("temp-"+buyer_tp+".jpg",cv2.cvtColor(frame,cv2.COLOR_RGB2BGR))
                compare_faces(buyer_tp, input_money)
                # This line will delete the image.
                os.remove("temp-"+buyer_tp+".jpg")
        else:
            # * This line will through an error to user face.
            messagebox.showerror("Error",'Please add the "ID" or "Amount" .')
       
    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if self.ok:
            self.vid.out.write(cv2.cvtColor(frame,cv2.COLOR_RGB2BGR))

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
        self.window.after(self.delay,self.update)


class VideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Command Line Parser
        args=CommandLineParser().args
        #create videowriter
        # 1. Video Type
        VIDEO_TYPE = {
            'avi': cv2.VideoWriter_fourcc(*'XVID'),
            #'mp4': cv2.VideoWriter_fourcc(*'H264'),
            'mp4': cv2.VideoWriter_fourcc(*'XVID'),
        }
        self.fourcc=VIDEO_TYPE[args.type[0]]
        # 2. Video Dimension
        STD_DIMENSIONS =  {
            '480p': (640, 480),
            '720p': (1280, 720),
            '1080p': (1920, 1080),
            '4k': (3840, 2160),
        }
        res=STD_DIMENSIONS[args.res[0]]
        print(args.name,self.fourcc,res)
        self.out = cv2.VideoWriter(args.name[0]+'.'+args.type[0],self.fourcc,10,res)
        #set video sourec width and height
        self.vid.set(3,res[0])
        self.vid.set(4,res[1])
        # Get video source width and height
        self.width,self.height=res
    # To get frames
    def get_frame(self):
        ret = False
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))                
            else:
                return (ret, None)    
        else:
            return (ret, None)
    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
            self.out.release()
            cv2.destroyAllWindows()


class CommandLineParser:
    
    def __init__(self):
        # Create object of the Argument Parser
        parser=argparse.ArgumentParser(description='Script to record videos')
        # Create a group for requirement 
        # for now no required arguments 
        # required_arguments=parser.add_argument_group('Required command line arguments')
        # Only values is supporting for the tag --type. So nargs will be '1' to get
        parser.add_argument('--type', nargs=1, default=['avi'], type=str, help='Type of the video output: for now we have only AVI & MP4')
        # Only one values are going to accept for the tag --res. So nargs will be '1'
        parser.add_argument('--res', nargs=1, default=['480p'], type=str, help='Resolution of the video output: for now we have 480p, 720p, 1080p & 4k')
        # Only one values are going to accept for the tag --name. So nargs will be '1'
        parser.add_argument('--name', nargs=1, default=['output'], type=str, help='Enter Output video title/name')
        # Parse the arguments and get all the values in the form of namespace.
        # Here args is of namespace and values will be accessed through tag names
        self.args = parser.parse_args()


def main():
    # Create a window and pass it to the Application object
    App(tk.Tk(),'Video Recorder')

main()

# test 