/*
 *  Author: Jose Luis Villarejo Muñoz
 *  Date  : Febrero 2015
 *  
 *  Programa para el control de un sistema Pan-Tilt que recibe los datos de los
 *  angulos desde un programa externo a traves del puerto serie.
 *
 */


#include <Servo.h>  


//Servos
Servo servoTilt;
Servo servoPan;

int pinTilt = 2;
int pinPan = 3;

//Variables para los angulos
int angTilt = 90;
int angPan = 90;

//Variable para recoger lo enviado por el puerto Serial
String recibido;

void setup(){
  
  servoTilt.attach(pinTilt);  //El servo Tilt en el pin digital 2.
  servoPan.attach(pinPan);   //El servo Pan en el pin digital 3.

//inicializamos servos a 90 grados
  servoTilt.write(angTilt);  
  servoPan.write(angPan);     
  
  Serial.begin(57600);  //Set up a serial connection for 57600 bps.
}

void loop()
{
  recibido = leerSerial();
  angTilt = getValores(recibido, 0);
  angPan = getValores(recibido, 1);
  Serial.print(angTilt);
  Serial.print(":");
  Serial.println(angPan);
  servoTilt.write(angTilt);  
  servoPan.write(angPan);     
}

//---------------------------------------------------//
// Funcion para obtener el mensaje enviado por el    //
// puerto serie                                      //
//---------------------------------------------------//
String leerSerial (){
  
 String dato;
 
 while(!Serial.available()) {}
  // leemos el puerto serial
  while (Serial.available())
  {
    if (Serial.available() > 0)
    {
      delay(5);
      char c = Serial.read();  //Obtenemos un bit del puerto serial
      dato += c; //lo incorporamos al mensaje
    }
  }

/*
  if (dato.length() > 0)
  {
    Serial.print("Arduino received: ");  
    Serial.println(dato); //see what was received
  }
*/
  return dato;
}

//---------------------------------------------------//
// Funcion que obtiene el valor de los angulos para  //
// el servo Tilt (1 valor) y para el servo Pan (2 valor) //                                      //
//---------------------------------------------------//

int getValores(String dato, int tipo){
  String subCadena;
  int posSeparador;
  
  posSeparador = dato.indexOf(':');
  
  if (tipo == 0) {  //obtenemos el valor Tilt
     subCadena = dato.substring(0, posSeparador);
  }
  else {
    subCadena = dato.substring(posSeparador+1);
  }
  
  return subCadena.toInt();
}
