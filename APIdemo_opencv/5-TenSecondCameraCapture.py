import cv2

cameraCapture = cv2.VideoCapture(0)
fps = 30 # an assumption
size = (int(cameraCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cameraCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

#fourcc = cv2.VideoWriter_fourcc(*'XVID')
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
videoWriter = cv2.VideoWriter(
    'MyOutputVid.avi', fourcc, fps, size)

success, frame = cameraCapture.read()
numFramesRemaining = 10 * fps - 1
while numFramesRemaining > 0:
    if frame is not None:
        ret = videoWriter.write(frame)
        cv2.imshow("frame",frame)
    success, frame = cameraCapture.read()
    #numFramesRemaining -= 1
    if cv2.waitKey(int(1000 / 12)) & 0xff == ord("q"):
      break

videoWriter.release()
cameraCapture.release()
cv2.destroyAllWindows()