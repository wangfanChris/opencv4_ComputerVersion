import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('../images/statue_small.jpg')

mask = np.zeros(img.shape[:2],np.uint8)

# 创建以0为背景的前景图和背景图
bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)

#定义参数为(xywh)的前景对象 该对象宽高是原图像宽高+1。为啥子这样弄呢
rect = (100,1,421,378)
cv2.grabCut(img,mask,rect,bgdModel,fgdModel,10,cv2.GC_INIT_WITH_RECT)

# 将mask数组里面 0 2转换为0 值为13的转换为1保存在mask2中
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')

#创建一个白板把我们的mask画出来
white = np.zeros(img.shape[:2],np.uint8) + 63
cv2.imshow("white",white*mask)

img = img*mask2[:,:,np.newaxis]

#绘制matplotlib图像
#(1 row, 2 col) grid for showing the image in the first cell
plt.subplot(121), plt.imshow(img)
plt.title("grabcut"), plt.xticks([]), plt.yticks([])

#(1 row, 2 col) grid for showing the image in the second cell
plt.subplot(122), plt.imshow(cv2.cvtColor(cv2.imread('../images/statue_small.jpg'), cv2.COLOR_BGR2RGB))
plt.title("original"), plt.xticks([]), plt.yticks([])
plt.show()


# Question:grabcut函数里面提供标注功能，在得到结果不合适的情况下可以手动对图像进行分割