import cv2
from tensorflow.keras.models import load_model
import numpy as np

model = load_model("Pen-CNN.model")

img_array = cv2.imread('Pen473.jpg', cv2.IMREAD_GRAYSCALE)
img_array = cv2.resize(img_array,(100,100))
X = np.array(img_array).reshape(-1, 100, 100, 1)
X = X.astype(np.float32)
X = X/255.0

prediction = model.predict(X)
print(prediction)
    
img_array = cv2.circle(img_array,(int(prediction[0][0]*100),int(prediction[0][1]*100)), 5, (0,0,255), -1)
#img_array = cv2.resize(img_array,(480,640))
cv2.imshow("output",img_array)
cv2.waitKey(0)