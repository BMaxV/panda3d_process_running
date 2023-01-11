import os
import subprocess

import panda3d
from direct.gui import DirectGuiGlobals as DGG
from panda3d.core import LVector3
from panda_interface_glue import panda_interface_glue
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectButton import DirectButton

print(panda3d.__file__)

def create_button(text,position,scale,function, arguments,text_may_change=0,frame_size=(-4.5,4.5,-0.75,0.75)):
    
    position = LVector3(*position)
    button = DirectButton(text=text,
                    pos=position,
                    scale=scale,
                    frameSize=frame_size,
                    textMayChange=text_may_change)
                    
    position[0]+=0.1
    
    button.setPos(*position)
    
    if function!=None and arguments!=None:
        arguments=list(arguments)
        button.bind(DGG.B1PRESS,function,arguments)
        
    return button

class MyContainer:
    def __init__(self):
        # this is my path on my machine, find out where you put your 
        # samples and insert that path here.
        self.sample_dir = "my_path_to/panda3d/samples"
        self.b = ShowBase()
        self.build_screen()
        self.my_process = None
        
    def build_screen(self):
        my_samples = os.listdir(self.sample_dir)
        
        y = 0
        scale  = 0.05
        x = -0.5
        for s in my_samples:
            p = (x,0,y)
            b = create_button(s,p,scale,self.run_sample,(s,))
            y -= 0.1
    
    def respawn(self):
        self.b = ShowBase()
        self.build_screen()
        self.my_process = None
        
    def run_sample(self,path,*args):
        self.b.destroy() # destroy the old showbase
        self.b = None
        
        # to run a different process, you may need to be in the correct
        # working directory
        
        os.chdir(self.sample_dir+"/"+path) # this could be done better and cross platform
        
        # and it needs to be called somewhat like so
        # think of it as "python main.py".split(" ")
        self.my_process = subprocess.call(["python3","main.py"])
        
if __name__=="__main__":
    M = MyContainer()
    
    #this waits, regular waiting doesn't work for some reason.
    while M.my_process == None or M.my_process == 0:
        if M.my_process == 0:
            M.respawn()
        M.b.taskMgr.step()
