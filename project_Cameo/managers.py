import cv2
import numpy
import time

class CaptureManager(object):
    def __init__(self, capture, previewWindowManage = None,
                        shouldMirrorPreview = False):
        self.previewWindowManage = previewWindowManage
        self.shouldMirrorPreview = shouldMirrorPreview
        self._capture = capture
        self._channel = 0
        self._enteredFrame = False
        self._frame = None
        self._imageFileName = None
        
        self._videoFileName = None
        self._videoEncoding = None
        self._videoWriter = None

        self._startTime = None
        self._framesElapsed = 0
        self._fpsEstimate = None

    @property
    def channel(self) :
        return self._channel
    
    @channel.setter
    def channel(self, value) :
        if self._channel != value:
            self._channel = value
            self._frame = None

    @property
    def frame(self) :
        if self._enteredFrame and self._frame is None:
            _, self._frame = self._capture.retrieve()
        return self._frame

    @property
    def isWritingImage(self):
        return self._imageFileName is not None

    @property
    def isWritingVideo(self):
        return self._videoFileName is not None

    """
    #decorator 解释器：
    @decorator 
    def func():
        xxx

    相当于
    func = decorator(func)

    结构体里面的@property相当于生成了一个getter
    @.setter相当于生成了一个setter
    """

    def enterFrame(self) :
        """ Capture the next frame"""

        #But first , check that any previous frame was exited.
        assert not self._enteredFrame, \
            'previous enterFrame() had no matching exitFrame'

        if self._capture is not None:
            self._enteredFrame = self._capture.grab()

    def exitFrame(self) :
        """ Draw to the window, Write to files. Release the frame """
        
        # check whether any grabbed frame is retrievable
        # The getter may retrieve and cache the frame
        if self.frame is None:
            self._enteredFrame = False
            return 

            # update the FPS estimate and related variables.
        if self._framesElapsed == 0:
            self._startTime = time.time()
        else :
            timeElapsed = time.time() - self._startTime
            self._fpsEstimate = self._framesElapsed / timeElapsed
        self._framesElapsed += 1

        #draw to the window, if any.
        if self.previewWindowManage is not None:
            if self.shouldMirrorPreview:
                mirroredFrame = numpy.fliplr(self._frame).copy()        # fliplr()将数组在行变换上翻转，列保持不便
                self.previewWindowManage.show(mirroredFrame)
            else:
                self.previewWindowManage.show(self._frame)

        #wirte to the image file , if any
        if self.isWritingImage:
            cv2.imwrite(self._imageFileName, self._frame)
            self._imageFileName = None

        # write to the video file, if any
        self._writeVideoFrame()

        #Release the frame
        self._frame = None
        self._enteredFrame = False

    def writeImage(self, filename):
        """write the next exited frame to an image file."""
        self._imageFileName = filename

    def startWritingVideo(self, filename, encoding = cv2.VideoWriter_fourcc('I', '4', '2', '0')):
        """Start writing exited frames to a video file."""
        self._videoFileName = filename
        self._videoEncoding = encoding

    def stopWritingVideo(self):
        """ Stop writing exited frames to a video file."""
        self._videoFileName = None
        self._videoEncoding = None
        self._videoWriter = None

    def _writeVideoFrame(self) :
        if not self.isWritingVideo:
            return

        if self._videoWriter is None:
            fps = self._capture.get(cv2.CAP_PROP_FPS)
            if fps == 0:
                #the captures fps is unknown so use a estimate
                if self._framesElapsed < 20:
                    #wait until more frames elapse so thart the estimate is more stable
                    return
                else :
                    fps = self._fpsEstimate
            size = (int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                        int (self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self._videoWriter = cv2.VideoWriter(
                self._videoFileName, self._videoEncoding, fps, size)
        self._videoWriter.write(self._frame)


class WindowManger(object):

    def __init__(self, windowName, keypressCallback = None) :
        self.keypressCallback = keypressCallback
        self._windowName = windowName
        self._isWindwoCreated= False

    @property
    def isWindwoCreated(self):
        return self._isWindwoCreated

    def createWindow(self) :
        cv2.namedWindow(self._windowName)
        self._isWindwoCreated = True
    
    def show(self, frame):
        cv2.imshow(self._windowName, frame)

    def destroyWindow(self):
        cv2.destroyWindow(self._windowName)
        self._isWindwoCreated = False

    def processEvents(self):
        keycode = cv2.waitKey(1)

        if self.keypressCallback is not None and keycode != -1:
            #Discard any non-ASCII info encoded by GTK
            keycode &= 0xFF
            self.keypressCallback(keycode)
    






