import sys
import os
import subprocess
import time
import datetime
from picamera import PiCamera
from time import sleep
from tkinter import *
from tkinter import ttk
#import tkSnack

# PiCamera #

camera = PiCamera(resolution=(1920, 1080), framerate=30)
#camera.framerate_delta = 0.5
#camera.framerate_range = (0.16666, 30)
camera.rotation = 270
#camera.hflip = True
#camera.vflip = True
#camera.image_denoise


class CamApp(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        
        self.grid(column=0, row=0, sticky=(N, S, E, W))       
        
        self.rotationLabel = StringVar()
        self.rotationLabel.set("Rotation:")        
        self.rotation = IntVar()
        
        self.directory = StringVar()
        self.directory.set("/home/pi/Desktop/")
        
        self.filecount = 1
        self.filename = StringVar()
        #self.ts = time.time()
        #self.st = datetime.datetime.fromtimestamp(self.ts).strftime('%Y-%m-%d_%H-%M-%S')
        self.filename.set("PiCam-%s" % self.filecount)
        
        #Dynamic Range Compression
        self.drcLabel = StringVar()
        self.drcLabel.set("Dynamic Range:")  
        self.drc = camera.drc_strength
        
        #Auto White Balance
        self.awbLabel = StringVar()
        self.awbLabel.set("White Balance:")
        self.awb = camera.awb_mode
        
        #Image Effect
        self.effectLabel = StringVar()
        self.effectLabel.set("Effect:")
        self.effect = camera.image_effect
        
        #Flash Mode
        self.flashLabel = StringVar()
        self.flashLabel.set("Flash:")
        self.flash = camera.flash_mode
        
        #Stabilize
        self.stabilize = IntVar()
        
        #Denoise
        self.denoise = IntVar()
        
        #Output Text
        self.output = StringVar()
        self.output.set("Not Recording")
        #self.output.set(camera.drc_strength)
        
        self.create_widgets()        
        
   
    
    def EscapeStop(self, id):        
        # camera.stop_preview()     
        
        try:
            camera._check_recording_stopped()
        
        except: #is recording
            camera.stop_recording()
            self.output.set("Recording Stopped")            
        
    
    def Record(self):
        self.FilePath = "%s%s.h264" % (self.directory.get(), self.filename.get())        
        try:
            camera._check_recording_stopped()
        
        except: #is recording
            camera.stop_recording()
            self.output.set("Recording Stopped")
            self.OutputText.configure(style="Black.TLabel")
            #self.filecount = self.filecount + 1
            #self.filename.set("PiCam-%s" % self.filecount)
            
        else: #not recording
            camera.start_recording(self.FilePath)
            self.output.set("Recording: %s" % self.FilePath)
            self.OutputText.configure(style="Red.TLabel")
                    

    def Convert(self):
        self.output.set("Converting: %s%s.h264" % (self.directory.get(), self.filename.get()))
        subprocess.call(['MP4Box','-add',"%s%s.h264" % (self.directory.get(), self.filename.get()), "%s%s.mp4" % (self.directory.get(), self.filename.get())])
        
    def Preview(self):
        #camera.preview.fullscreen = False
        camera.start_preview()
        sleep(5)
        camera.stop_preview()
        
    def UpdateRotation(self, event):
        camera.rotation = self.RotationSelect.get()
        self.output.set("Rotation: %s" % str(camera.rotation))
    
    def UpdateDRC(self, event):
        camera.drc_strength = self.DRCSelect.get()
        self.output.set("Dynamic Range Compression: %s" % camera.drc_strength)
        
    def UpdateAWB(self, event):
        camera.awb_mode = self.AWBSelect.get()
        self.output.set("Auto White Balance: %s" % camera.awb_mode)
    
    def UpdateStabilize(self):
        camera.video_stabilization = self.stabilize.get()
        self.output.set("Video Stabilization: %s" % camera.video_stabilization)        
         
    def UpdateDenoise(self):
        camera.video_denoise = self.denoise.get()
        self.output.set("Video Denoise: %s" % camera.video_denoise)
        
    def UpdateEffect(self, event):
        camera.image_effect = self.EffectSelect.get()
        self.output.set("Image Effect: %s" % camera.image_effect)
         
    def UpdateFlash(self, event):
        camera.flash_mode = self.FlashSelect.get()
        self.output.set("Flash Mode: %s" % camera.flash_mode)
        
        
        

    def create_widgets(self):
        top=self.winfo_toplevel()
        top.rowconfigure(0,weight=1)
        top.columnconfigure(0, weight=1)
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)        
        
        #self.rowconfigure(1, weight=1)
        #self.columnconfigure(1, weight=1)
        
        #self.rowconfigure(2, weight=1)
        #self.columnconfigure(2, weight=1)
        
        #self.rowconfigure(3, weight=1)
        #self.columnconfigure(3, weight=1)
        
        #self.rowconfigure(4, weight=1)
        #self.columnconfigure(4, weight=1)
        
        #self.rowconfigure(5, weight=1)
        #self.columnconfigure(5, weight=1)
        
        #self.rowconfigure(6, weight=1)
        #self.columnconfigure(6, weight=1)
        self.OutputStyle = ttk.Style()
        self.OutputStyle.configure("Black.TLabel", background="black", foreground="white")
        self.OutputStyle.configure("Red.TLabel", background="red", foreground="white")
        
        self.OutputText = ttk.Label(self, textvariable=self.output)
        self.OutputText.grid(column=0, row=0, padx=15, pady=15, columnspan=4, sticky="WE")
        self.OutputText.configure(style="Black.TLabel")
        
        self.DirectoryEntry = ttk.Entry(self, width=50, textvariable=self.directory)
        self.DirectoryEntry.grid(column=0, row=1, padx=15, pady=15, columnspan=2, sticky="WE")
        
        self.FileNameEntry = ttk.Entry(self, width=50, textvariable=self.filename)
        self.FileNameEntry.grid(column=2, row=1, padx=15, pady=15, columnspan=2, sticky="WE")
        self.FileNameEntry.focus()
                
        self.RotationLabel = ttk.Label(self, textvariable=self.rotationLabel)
        self.RotationLabel.grid(column=0, row=2, padx=15, pady=15, columnspan=2, sticky="WE")
        self.RotationSelect = ttk.Combobox(self, values=[0,90,180,270], width=20)
        self.RotationSelect.grid(column=1, row=2, padx=15, pady=15)
        self.RotationSelect.bind("<<ComboboxSelected>>", self.UpdateRotation)
        self.RotationSelect.set(camera.rotation)
        
        self.DRCLabel = ttk.Label(self, textvariable=self.drcLabel)
        self.DRCLabel.grid(column=0, row=4, padx=15, pady=15, columnspan=2, sticky="WE")        
        self.DRCSelect = ttk.Combobox(self, values=["off","low","medium","high"],width=20)
        self.DRCSelect.grid(column=1, row=4, padx=15, pady=15)
        self.DRCSelect.bind("<<ComboboxSelected>>", self.UpdateDRC)
        self.DRCSelect.set(camera.drc_strength)
        
        self.AWBLabel = ttk.Label(self, textvariable=self.awbLabel)
        self.AWBLabel.grid(column=2, row=4, padx=15, pady=15, columnspan=1, sticky="WE")
        self.AWBSelect = ttk.Combobox(self, values=["off", "auto", "sunlight", "cloudy", "shade", "tungsten", "fluorescent", "incandescent", "flash", "horizon"],width=20)
        self.AWBSelect.grid(column=3, row=4, padx=15, pady=15)
        self.AWBSelect.bind("<<ComboboxSelected>>", self.UpdateAWB)
        self.AWBSelect.set(camera.awb_mode)
        
        self.FlashLabel = ttk.Label(self, textvariable=self.flashLabel)
        self.FlashLabel.grid(column=0, row=5, padx=15, pady=15, columnspan=1, sticky="WE")
        self.FlashSelect = ttk.Combobox(self, values=["off", "auto", "on", "redeye", "fillin", "torch"],width=20)
        self.FlashSelect.grid(column=1, row=5, padx=15, pady=15)
        self.FlashSelect.bind("<<ComboboxSelected>>", self.UpdateFlash)
        self.FlashSelect.set(camera.flash_mode)
        
        self.EffectLabel = ttk.Label(self, textvariable=self.effectLabel)
        self.EffectLabel.grid(column=2, row=5, padx=15, pady=15, columnspan=1, sticky="WE")
        self.EffectSelect = ttk.Combobox(self, values=["none", "negative", "solarize", "sketch", "denoise", "emboss", "oilpaint", "hatch", "gpen", "pastel", "watercolor", "film", "blur", "saturation", "colorswap", "washedout", "posterise", "colorpoint", "colorbalance", "cartoon", "deinterlace1", "deinterlace2"],width=20)
        self.EffectSelect.grid(column=3, row=5, padx=15, pady=15)
        self.EffectSelect.bind("<<ComboboxSelected>>", self.UpdateEffect)
        self.EffectSelect.set(camera.image_effect)
        
        
        
        self.StabilizeCheck = ttk.Checkbutton(self, text="Stabilize", variable=self.stabilize, onvalue=1, offvalue=0, command=self.UpdateStabilize)
        self.StabilizeCheck.grid(column=2, row=2, padx=15, pady=15)
        
        self.DenoiseCheck = ttk.Checkbutton(self, text="Denoise", variable=self.denoise, onvalue=1, offvalue=0, command=self.UpdateDenoise)
        self.DenoiseCheck.grid(column=3, row=2, padx=15, pady=15)
        #self.StabilizeCheck.bind("<<ComboboxSelected>>", self.UpdateStabilize)
        #self.StabilizeCheck.value(camera.video_stabilization)
        
        self.RecordButton = ttk.Button(self, text="Record", command=self.Record).grid(column=4, row=1, padx=15, pady=15)

        self.PreviewButton = ttk.Button(self, text="Preview", command=self.Preview).grid(column=0, row=6, padx=15, pady=15)
        self.ConvertButton = ttk.Button(self, text="Convert", command=self.Convert).grid(column=2, row=6, padx=15, pady=15)
        self.QuitButton = ttk.Button(self, text="Quit", command=root.destroy).grid(column=4, row=6, padx=15, pady=15)    
        
        top.bind('<Escape>', self.EscapeStop)
        # Camera Settings
        #textvariable=self.rotation
        #self.RotationDropdown = ttk.Listbox(self, height=6)
        
        
    
root = Tk()
root.title("PiCamera")
root.geometry("800x300")

#tkSnack.initializeSnack(root)

app = CamApp(master=root)
app.mainloop()
