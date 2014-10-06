/*
* Author: Jose Luis Villarejo Muñoz
* Date : Octubre 2014
*
* Programa para uso de un sensor de ultrasonidos BAT en una simulación de un radar
* que se visualiza en un dispositivo móvil, enviando los datos del sensor mediante bluetooth.
*
*/

#include <NewPing.h>
#include <Servo.h>

#define PINSERVO 10
#define PINTIGGER 13
#define PINECO 12
#define MAXDISTANCIA 200

//----- ANGULOLIMITE indica el desde y el hasta del rastreo. En este caso -80º..80º
#define ANGULOLIMITE 80

//----- ANGULOSALTO es el incremento que aplicamos para mover el servo
#define ANGULOSALTO 1

Servo miServo;

//Aquí hemos utilizado la libreria NewPing por comodidad y rapidez
//   http://playground.arduino.cc/Code/NewPing

NewPing ultraS(PINTIGGER, PINECO, MAXDISTANCIA);

int angulo = 0;
int distancia = 0;
int dir = 1;

void setup()
{
  miServo.attach(PINSERVO); 
// Inicializamos el bluetooth. Como estoy utilizando una placa ZUM-Uno de bq lo inicializo a 19200 bps
// que el que marca el fabricante.
  Serial.begin(19200);
}

void loop()
{
  delay(25);
  
//Con la siguiente operación normalizamos el valor que enviamos al servo, ya que la variable angulo
//alberga valores entre -ANGULOLIMITE y +ANGULOLIMITE (-80 y 80 en este caso) y al servo hemos mandarle
//valores entre 0..180.
  miServo.write(angulo + ANGULOLIMITE);
  
  distancia = ultraS.ping_cm();
 
  Serial.print(angulo,DEC);
  Serial.print(",");
  Serial.println(distancia,DEC);
 
 // Si la variable angulo ha llegado a uno de sus limites, cambiamos de dirección
  if (angulo >= ANGULOLIMITE || angulo <= -ANGULOLIMITE)
  {
     dir = -dir;
  } 
  
  angulo += (dir * ANGULOSALTO);
}



