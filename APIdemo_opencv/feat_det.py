import cv2
import sys

# xfeatures2d 在cv3.4以上版本不能用咯，已经被别人纳入专利范围。
def fd(algorithm,hessionThrehold):
    algorithms = {
    "SIFT": cv2.xfeatures2d.SIFT_create(),
    "SURF": cv2.xfeatures2d.SURF_create(float(hessionThrehold) if len(sys.argv) == 4 else 4000),
    "ORB": cv2.ORB_create()
    }
    return algorithms[algorithm]

def feat(imgpath,alg,hessionThrehold=8000):
    img = cv2.imread(imgpath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    fd_alg = fd(alg,hessionThrehold)
    keypoints, descriptor = fd_alg.detectAndCompute(gray,None)

    img = cv2.drawKeypoints(image=img, outImage=img, keypoints = keypoints, flags = 4, color = (51, 163, 236))

    cv2.imshow('keypoints', img)

def nothing(x):
  pass

#python feat_det.py images/varese.jpg SURF 8000
if __name__ == "__main__":
  feat("../images/varese.jpg", "SURF", hessionThrehold=8000) 

  """
  cv2.namedWindow("image")
  cv2.createTrackbar("hessionThrehold", "image", 0, 255, nothing)
  feat(sys.argv[1], sys.argv[2], hessionThrehold=8000) 
  while (True):
    if cv2.waitKey(int(1000 / 12)) & 0xff == ord("q"):
      break
  cv2.destroyAllWindows()

"""








