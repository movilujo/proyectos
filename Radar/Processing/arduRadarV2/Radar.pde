/*
* Author: Jose Luis Villarejo Muñoz
* Date : Octubre 2014
*
* Este clase ha sido copiada de 
*               https://github.com/pepijnkoopman/ArduinoRadar/blob/master/radar_client.pde
* y convenientemente adaptada para utilizarse para realizar la comunicación por Bluetooth.
*
*/

//----------------------------------------------------------------------
//              Clase Radar
//----------------------------------------------------------------------

class Radar
{
 int SIDE_LENGTH;
 int ANGLE_BOUNDS = 80;
 int ANGLE_STEP = 2;
 int HISTORY_SIZE = 10;
 int POINTS_HISTORY_SIZE = 100;
 
 int radio;
 float x;
 float y;
 float leftAnguloRad;
 float rightAnguloRad;
 float[] historyX, historyY;
 Punto[] puntos;
 int centroX;
 int centroY;
 
 //************************************************* 
 //Constructor
 //*************************************************
 Radar (int alto, int ancho)
 {
    SIDE_LENGTH = (alto-100) * 2; 
    radio = SIDE_LENGTH / 2;
    centroX = ancho / 2;
    centroY = alto;
    leftAnguloRad = radians(-ANGLE_BOUNDS) - HALF_PI;
    rightAnguloRad = radians(ANGLE_BOUNDS) - HALF_PI;
    historyX = new float[HISTORY_SIZE];
    historyY = new float[HISTORY_SIZE];
    puntos = new Punto[POINTS_HISTORY_SIZE];
 }
 
 //************************************************* 
 //Método para dibujar el fondo del radar
 //*************************************************
 void dibRadar() 
 {
    stroke(100);  //color de las lineas
    noFill();
    strokeWeight(2); //ancho de las líneas
   
    //dibujamos los semicirculos como referencias de la distacia
    for (int i = 0; i <= (SIDE_LENGTH / 100); i++) {
       arc(centroX, centroY, 100 * i, 100 * i, leftAnguloRad, rightAnguloRad);
    }

    //dibujamos lineas como referencia del angulo
    for (int i = 0; i <= (ANGLE_BOUNDS*2/20); i++) {
        float angulo = -ANGLE_BOUNDS + i * 20;
        float radAngulo = radians(angulo);
        line(centroX, centroY, centroX + radio*sin(radAngulo), centroY - radio*cos(radAngulo));
    }
    
 }
    
 //******************************************************* 
 //Método para dibujar las líneas que simulan el rastreo
 //*******************************************************
 void dibRastreo(int angle) {
   float radian = radians(angle);
   x = radio * sin(radian);
   y = radio * cos(radian);
   float px = centroX + x;
   float py = centroY - y;
   historyX[0] = px;
   historyY[0] = py;
   strokeWeight(2);
   for (int i=0;i<HISTORY_SIZE;i++) {
       stroke(50, 190, 50, 255 - (25*i));
       line(centroX, centroY, historyX[i], historyY[i]);
   }
   shiftHistoryArray();
 }
  
 //******************************************************* 
 //Método para dibujar los objetos que se detectan
 //*******************************************************
 void dibEncontrados(int angle, int distance) {
   
   if (distance > 0) {
      float radian = radians(angle);
      x = distance * sin(radian);
      y = distance * cos(radian);
      int px = (int)(centroX + x);
      int py = (int)(centroY - y);
      puntos[0] = new Punto(px, py);
   }
   else {
      puntos[0] = new Punto(0, 0);
   }
   for (int i=0;i<POINTS_HISTORY_SIZE;i++) {
       Punto punto = puntos[i];
       if (punto != null) {
          int x = punto.x;
          int y = punto.y;
          if (x==0 && y==0) continue;
          int colorAlfa = (int)map(i, 0, POINTS_HISTORY_SIZE, 50, 0);
          int size = (int)map(i, 0, POINTS_HISTORY_SIZE, 30, 5);
          fill(190, 40, 40, colorAlfa);
          noStroke();
          ellipse(x, y, size, size);
       }
   }
   shiftPointsArray();
 }
 
  void shiftHistoryArray() {
   for (int i = HISTORY_SIZE; i > 1; i--) {
       historyX[i-1] = historyX[i-2];
       historyY[i-1] = historyY[i-2];
   }
 }

 void shiftPointsArray() {
   for (int i = POINTS_HISTORY_SIZE; i > 1; i--) {
       Punto oldPoint = puntos[i-2];
       if (oldPoint != null) {
          Punto punto = new Punto(oldPoint.x, oldPoint.y);
          puntos[i-1] = punto;
       }
   }
 }
 
}

//----------------------------------------------------------------------
//              Clase Punto
//----------------------------------------------------------------------
 class Punto {
   int x, y;
   Punto(int xPos, int yPos) {
     x = xPos;
     y = yPos;
   }
 
   int getX() {
     return x;
   }

   int getY() {
     return y;
   }
 }

