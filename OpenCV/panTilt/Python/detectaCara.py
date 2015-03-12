__author__ = 'Jose Luis V'

from cv2 import *
namedWindow("webcam")
vc = VideoCapture(0);

# establecemos las dimensiones de la imagen
vc.set(3, 640)
vc.set(4, 480)

# Cargamos el fichero con las especificaciones para identificar caras (de frente en este caso)
detector = CascadeClassifier("haarcascade_frontalface_alt.xml");

while True:
    ret, frame = vc.read()

# Obtenemos las caras detectadas
    caras = detector.detectMultiScale(
        frame,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv.CV_HAAR_SCALE_IMAGE
    )

    for (x, y, w, h) in caras:
        rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    imshow("webcam",frame)
    if waitKey(50) >= 0:
        break
vc.release()
