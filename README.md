# LiveED: Smart Teacher's App  
This app allows teachers and illustrators to air-draw or air-write and have their writings be shown on screen in real time. This project was done for AngelHack in 2019. The app uses computer vision to identify a pen tip, and speech recognition to get assests from the web while the teacher is teaching. This allows for a more immersive and visual learning experience for the students. There is also a deep learning based approach which has a better accuracy.  

# Usage  
## Dependencies
Following dependencies are required: 
1. OpenCV based approach
```
SpeechRecognition
pyaudio
OpenCV
GoogleImagesSearch
Numpy
Pillow
```
2. Deep Learning based approach  
All of the above, and:  
```
Tensorflow
```

## Training  
The OpenCV method doesn't require any training.  
The deep learning based approach requires training and can be done by running the cnn.py file via `python cnn.py`.  
Once the training is complete, there should be a directory named `Pen-CNN.model` under `Deep_learning_approach`. Use  
`python predictor_image.py`  

## Inference  
Simpy use `python videowindow.py` to run the application. You can calibrate the pen's color for better accuracy. Currently you have to update the HSV values in the code for the above, we will add utilities to specify these colors in the future.  


To run inference on an image. The default image is currently specified as `Pen473.jpg`. We will add utilities to specify your own images in the future. Till then, either rename the image you want to predict to `Pen473.jpg` and place it withing the `Deep_learning_approach` directory, else, change the path in the source code of `predictor_image.py`. 

