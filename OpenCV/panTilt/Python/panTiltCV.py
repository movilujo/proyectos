__author__ = 'Jose Luis Villarejo'

#-- Programa para experimentar con OpenCV en el que se detecta la cara
#-- y mediante el calculo del desplazamiento de la misma a traves de los ejes X e Y
#-- enviamos a Arduino por el puerto Serial los angulos correspondientes para mover un
#-- sistema Pan/Tilt

from cv2 import *
import serial #cargamos la libreria serial
import sys

imgAncho = 640
imgAlto = 480

centroCaraX = 0
centroCaraY = 0
centroPantallaX = (imgAncho/2)
centroPantallaY = (imgAlto/2)
tolerancia = 10
angX = 0
angY = 0
panGrad = 90
tiltGrad = 90

envio = ""

#En la siguiente instrucción está definido para mi puerto Serial, tenéis que cambiarlo
arduino = serial.Serial('/dev/tty.usbserial-FTWVDDX2', 57600)

#Con esta funcion dibujamos los ejes centrales en la imagen
def dibujaEjes(img):
    line(img, (0, imgAlto/2), (imgAncho, imgAlto/2), ( 0, 255, 0), 1, 0)
    line(img, (imgAncho/2, 0), (imgAncho/2, imgAlto), ( 0, 255, 0), 1, 0)

namedWindow("webcam", flags= WINDOW_NORMAL)
resizeWindow("webcam", imgAncho, imgAlto)
vc = VideoCapture(0)


# establecemos las dimensiones de la imagen
vc.set(3, imgAncho)
vc.set(4, imgAlto)

# Leemos un frame desde la camara
ret, frame = vc.read()

# Cargamos el fichero con las especificaciones para identificar caras (de frente en este caso)
detector = CascadeClassifier("haarcascade_frontalface_alt.xml");

while True:
    dibujaEjes(frame)
    gris = cvtColor(frame, COLOR_BGR2GRAY)

    caras = detector.detectMultiScale(
        gris,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv.CV_HAAR_SCALE_IMAGE
    )

    for (x, y, w, h) in caras:
        rectangle(gris, (x, y), (x+w, y+h), (0, 255, 0), 2)

        centroCaraX = x + (w/2)
        centroCaraY = y + (h/2)
        circle(gris,(centroCaraX, centroCaraY), 5, (0, 255, 0), -1)

# El desplazamiento, para hacerlo bien, habria que calcularlo con funciones trigonometricas, pero como
# aproximacion os aseguro que funciona bastante bien
    angX = centroCaraX - centroPantallaX
    angY = centroCaraY - centroPantallaY

# No aseguramos que los valores estén dentro del rango -75, 75
# de esta forma nos aseguramos que los valores que le vamos a
# a los servos están dentro de 15, 165 grados
    if angX < -75:
        angX = -75
    if angX > 75:
        angX = 75
    if angY < -75:
        angY = -75
    if angY > 75:
        angY = 75

# Esto lo hago porque no he encontrado el equivalente en Python a la funcion map() que si tenemos en
# Arduino u otros lenguajes.
    panGrad = 90 + angX
    tiltGrad = 90 + angY

    envio = str(tiltGrad) + ":" + str(panGrad)
    arduino.write(envio)
#    print(envio)

    imshow("webcam",gris)
    ret, frame = vc.read()
    if waitKey(50) >= 0:
        break


vc.release()
destroyAllWindows()
arduino.close()
sys.exit()