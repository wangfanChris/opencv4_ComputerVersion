import sys
sys.path.append('/home/wangfan/Desktop/test')

import cv2
import filters
from managers import WindowManger, CaptureManager

class Cameo(object):
    def __init__(self):
        self._windowManager = WindowManger('Cameo', self.onKeypress)
        self._captureManager = CaptureManager(cv2.VideoCapture(0), self._windowManager, True)
        self._curveFilter = filters.FindEdgesFilter()

    def run(self):
        """Run the main loop"""
        self._windowManager.createWindow()
        while self._windowManager.isWindwoCreated:
            self._captureManager.enterFrame()

            frame = self._captureManager.frame
            if frame is not None:
                # TODO : filter the frame (chapter 3)
                filters.strokeEdges(frame,frame)
                self._curveFilter.apply(frame, frame)
            
            self._captureManager.exitFrame()
            self._windowManager.processEvents()

    def onKeypress(self, keycode):
        """ Handle a keypress 
        space-> Take a screenshot
        tab-> Start/Stop recording a screencast.
        escape ->quit
        """
        if keycode == 32: #space
            self._captureManager.writeImage('screenshot.png')
        elif keycode == 9: #tab
            if not self._captureManager.isWritingVideo:
                self._captureManager.startWritingVideo('screencast.avi')
            else :
                self._captureManager.stopWritingVideo()
        elif keycode == 27: # esc
            self._windowManager.destroyWindow()
                
#if __name__ == "__main__":
Cameo().run()




