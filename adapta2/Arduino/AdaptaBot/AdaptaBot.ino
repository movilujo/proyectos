/*
 *  Author: Jose Luis Villarejo Muñoz
 *  Date  : Enero 2014
 *  
 *  Programa de prueba de una interfaz entre Android y Arduino para crear
 *  una plataforma para juguetes adaptados para su uso con niños con
 *  problemas de movilidad.
 *
 */
#include <SoftwareSerial.h>
#include <Servo.h>

#define RxD 10
#define TxD 11
#define RST 5 // Encendido del Modulo

#define LED 13

int servoPinR = 7;    // pin motor derecho
int servoPinL = 4;   // pin motor izquierdo

SoftwareSerial BTSerial(RxD, TxD);
byte pinEstado = 0;

Servo servoR;
Servo servoL;

void setup()
{
  servoR.attach(servoPinR);
  servoL.attach(servoPinL);
  
  // Estado inicial
  pinMode(RST, OUTPUT);
  digitalWrite(LED, HIGH);
  digitalWrite(LED, LOW);
  digitalWrite(RST, LOW);
   
  // Encendemos el modulo.
  digitalWrite(RST, HIGH);
  delay(500);
  
  // Configuracion del puerto serie por software
  // para comunicar con el modulo HC-05
//  BTSerial.begin(9600);
  BTSerial.flush();
  delay(500);
  BTSerial.begin(38400);
  
  // Configuramos el puerto serie de Arduino para Debug
  Serial.begin(9600);
  Serial.println("Ready");


}

void loop()
{
  // Esperamos ha recibir datos.
  if (BTSerial.available()){
    
    // La funcion read() devuelve un caracter 
    char command = BTSerial.read();
    BTSerial.flush();
    
    // Comprobamos el comando recibido y mostramos la acción que se debe hacer
    switch (command) {
      case 'A': 
          Serial.println("1: ON");
          advance();
          break;
      case '0':
          Serial.println("Parar/OFF");
          halt();
          break;
      case '1':
          Serial.println("4b-1: Avanza");
          advance();
          break;
      case '2':
          Serial.println("4b-2: Gira a la Derecha");
          turnR();
          break;
      case '3':
          Serial.println("4b-3: Retrocede");
          move_back();
          break;
       case '4':
          Serial.println("4b-4: Gira a la Izquierda");
          turnL();
          break;     
    }
    
  }
}

/////////////////////////////////////////////////
//////////  Movimientos
/////////////////////////////////////////////////

// avanzar
void advance()
{
  servoR.write(180);
  servoL.write(0);
}

// retroceder
void move_back()
{
  servoR.write(0);
  servoL.write(180);
}

// girar a la derecha
void turnR()
{
  servoR.write(90);
  servoL.write(0);
}

// girar a la izquierda
void turnL()
{
  servoR.write(180);
  servoL.write(90);
}

// parar
void halt()
{
  servoR.write(90);
  servoL.write(90);
}



