package processing.test.arduradarv2;

import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import android.bluetooth.BluetoothAdapter; 
import android.bluetooth.BluetoothDevice; 
import android.bluetooth.BluetoothSocket; 
import android.content.Context; 
import android.content.Intent; 
import android.content.IntentFilter; 
import java.util.UUID; 
import android.os.Handler; 
import android.os.Message; 
import java.util.ArrayList; 
import java.io.IOException; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.lang.reflect.Method; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class arduRadarV2 extends PApplet {

/*
* Author: Jose Luis Villarejo Mu\u00f1oz
* Date : Octubre 2014
*
* Este programa ha sido copiado de 
*        http://www.sistemasorp.es/2011/08/13/android-processing-bluetooth/
* y modificado levemente para poder utilizar la clase Radar de forma que pueda ser 
* como el simulador de un Radar.
* 
* El programa conecta mediante bluetooth con arduino en el que se ejecuta un programa que utiliza un sensor
* de Ultrasonidos para detectar objetos y utiliza la informaci\u00f3n recibida para visalizarla en un 
* dispositivo m\u00f3vil.
*
*/

















private static final int REQUEST_ENABLE_BT = 3;
ArrayList dispositivos;
BluetoothAdapter adaptador;
BluetoothDevice dispositivo;
BluetoothSocket socket;
boolean registrado = false;
PFont f1;
PFont f2;
int estado;
String error;
byte valor;

int MAX_DISTANCE = 200;
int angulo = -80;
int dir = 0;
int distancia;
String comPortString;

// Tipos de mensajes usados por Handler
public static final int ESCRIBE_MSG = 1;
public static final int LEE_MSG = 2;

Radar miRadar;
getSendDatos RecibeBT=null;
//-------------------------------------------------------------------
// Procedimientos Processing estandar
//-------------------------------------------------------------------
public void setup()
{
  orientation(LANDSCAPE);
  miRadar = new Radar(displayHeight, displayWidth);
  f1 = loadFont("ArialMT-20.vlw");
  f2 = loadFont("ArialMT-15.vlw");
  stroke(255);  
}

public void draw()
{
  switch(estado)
  {
    case 0:
      listaDispositivos("BUSCANDO DISPOSITIVOS", color(255, 0, 0));
      break;
    case 1:
      listaDispositivos("ELIJA DISPOSITIVO", color(0, 255, 0));
      break;
    case 2:
      conectaDispositivo();
      break;
    case 3:
      muestraDatos();
      break;
    case 4:
      muestraError();
      break;
  }  
}

//----------------------------------------------------------------------------------
// Procedimientos control de flujo de Android y referentes a la conexi\u00f3n Bluetooth
//----------------------------------------------------------------------------------
public void onStart()
{
  super.onStart();
//  println("onStart");
  adaptador = BluetoothAdapter.getDefaultAdapter();
  if (adaptador != null)
  {
    if (!adaptador.isEnabled())
    {
        Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
        startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);
    }
    else
    {
      empieza();
    }
  }
}

//--------------------------------------------------------
public void onStop()
{
//  println("onStop");
  if(socket != null)
  {
    try
    {
      socket.close();
    }
    catch(IOException ex)
    {
      println(ex);
    }
  }
  super.onStop();
}

//--------------------------------------------------------
public void onActivityResult (int requestCode, int resultCode, Intent data)
{
//  println("onActivityResult");
  if(resultCode == RESULT_OK)
  {
    empieza();
  }
  else
  {
    estado = 4;
    error = "No se ha activado el bluetooth";
  }
}

//--------------------------------------------------------
public void mouseReleased()
{
  switch(estado)
  {
    case 0:
      break;
    case 1:
      compruebaEleccion();
      break;
  }
}


//--------------------------------------------------------
// The Handler obtiene los datos desde le Socket
private final Handler mHandler = new Handler() 
{
   @Override
   public void handleMessage(Message msg) {
    switch (msg.what) {
     case ESCRIBE_MSG:
        //No usado en este caso
        break;
     case LEE_MSG:
        //Obtiene los datos desde el msg.obj
        String strRecibido = null;
        byte[] datRecibidos = (byte[]) msg.obj;
        // construct a string from the valid bytes in the buffer
        strRecibido = new String(datRecibidos, 0, msg.arg1);
        if (strRecibido != null) {
            strRecibido=trim(strRecibido);
            String[] values = split(strRecibido, ',');
            try {
                 angulo = PApplet.parseInt(map(Integer.parseInt(values[0]), 0, 160, -80, 80));
                 distancia = PApplet.parseInt(map(Integer.parseInt(values[1]), 1, MAX_DISTANCE, 1, miRadar.radio));
                 println(angulo + ", "+distancia);
            } catch (Exception e) {}
        }
        break;
    }
   }
};

//----------------------------------------------------------------------
// Procedimientos referentes a la conexi\u00f3n Bluetooth
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
//  Obtenemos un listado de los dispositivos bluetooth que tenemos emparejados.
// Para que funcione este programa, el bluetooth que usemos en la parte Arduino debe estar
// emparejado previamente a nuestro dispositivo.
//-----------------------------------------------------------------------

public void empieza()
{
    dispositivos = new ArrayList();
    for (BluetoothDevice dispositivo : adaptador.getBondedDevices())
    {
        dispositivos.add(dispositivo);
    }
    estado = 1;
}


//-----------------------------------------------------------------------
//  Mostramos en pantalla el listado de los dispositivos bluetooth que tenemos emparejados.
//-----------------------------------------------------------------------

public void listaDispositivos(String texto, int c)
{
//  println("listaDispositivos");
  background(0);
  textFont(f1);
  fill(c);
  text(texto,0, 20);
  if(dispositivos != null)
  {
    for(int indice = 0; indice < dispositivos.size(); indice++)
    {
      BluetoothDevice dispositivo = (BluetoothDevice) dispositivos.get(indice);
      fill(255,255,0);
      int posicion = 50 + (indice * 55);
      if(dispositivo.getName() != null)
      {
        text(dispositivo.getName(),0, posicion);
      }
      fill(180,180,255);
      text(dispositivo.getAddress(),0, posicion + 20);
      fill(255);
      line(0, posicion + 30, 319, posicion + 30);
    }
  }
}

//-----------------------------------------------------------------------
//  Obtenemos el dispositivo que se ha seleccionado en pantalla
//-----------------------------------------------------------------------
public void compruebaEleccion()
{
  println("compruebaEleccion");
  int elegido = (mouseY - 50) / 55;
  if(elegido < dispositivos.size())   
  {     
    dispositivo = (BluetoothDevice) dispositivos.get(elegido);     
    println(dispositivo.getName());     
    estado = 2;   
  } 
} 

//-----------------------------------------------------------------------
//  Establecemos una conexi\u00f3n con el dispositivo seleccionado
//-----------------------------------------------------------------------
public void conectaDispositivo() 
{   
  println("conectaDispositivo");
    
  try   
  {     
    socket = dispositivo.createRfcommSocketToServiceRecord(UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"));
    socket.connect();
        
//    ins = socket.getInputStream();     
//    ons = socket.getOutputStream();
    RecibeBT = new getSendDatos(socket);
    new Thread(RecibeBT).start();
    estado = 3;   

//    println("conectado");
  }   
  catch(Exception ex)   
  {     
    estado = 4;     
    error = ex.toString();     
    println(error);   
  }
 
}

//**********************************************************************
// Procedimientos operacionales
//**********************************************************************


//---------------------------------------------------------------------------------
//  Dibujamos y mostramos en la pantalla del dispositivo m\u00f3vil los datos obtenidos
//----------------------------------------------------------------------------------
public void muestraDatos()
{
//  println("muestraDatos: " + miRadar.centerX);
  background(0, 0, 0);
  miRadar.dibRadar();
  miRadar.dibRastreo(angulo); 
  miRadar.dibEncontrados(angulo, distancia);  
}

//---------------------------------------------------------------------------------
//  Procedimiento para mostrar un error
//----------------------------------------------------------------------------------
public void muestraError()
{
  background(255, 0, 0);
  fill(255, 255, 0);
  textFont(f2);
  textAlign(CENTER);
  translate(width / 2, height / 2);
  rotate(3 * PI / 2);
  text(error, 0, 0);
}

/*
* Author: Jose Luis Villarejo Mu\u00f1oz
* Date : Octubre 2014
*
* Este clase ha sido copiada de 
*               https://github.com/pepijnkoopman/ArduinoRadar/blob/master/radar_client.pde
* y convenientemente adaptada para utilizarse para realizar la comunicaci\u00f3n por Bluetooth.
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
 //M\u00e9todo para dibujar el fondo del radar
 //*************************************************
 public void dibRadar() 
 {
    stroke(100);  //color de las lineas
    noFill();
    strokeWeight(2); //ancho de las l\u00edneas
   
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
 //M\u00e9todo para dibujar las l\u00edneas que simulan el rastreo
 //*******************************************************
 public void dibRastreo(int angle) {
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
 //M\u00e9todo para dibujar los objetos que se detectan
 //*******************************************************
 public void dibEncontrados(int angle, int distance) {
   
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
 
  public void shiftHistoryArray() {
   for (int i = HISTORY_SIZE; i > 1; i--) {
       historyX[i-1] = historyX[i-2];
       historyY[i-1] = historyY[i-2];
   }
 }

 public void shiftPointsArray() {
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
 
   public int getX() {
     return x;
   }

   public int getY() {
     return y;
   }
 }

/*
* Author: Jose Luis Villarejo Mu\u00f1oz
* Date : Octubre 2014
*
* Con esta clase creamos un Thread mediante el cual leemos los datos recibidos
* desde el dispositivo externo, en este caso Arduino.
*/

private class getSendDatos implements Runnable {
  private InputStream ins;
  private OutputStream ons;
  private BluetoothSocket DataSocket;
  
  public getSendDatos(BluetoothSocket socket) {
      DataSocket = socket;
      try {
            ins = DataSocket.getInputStream();
            ons = DataSocket.getOutputStream();
      } 
      catch (Exception e) { 
      }
  }

  public void run() {
      byte[] buffer = new byte[1024]; // buffer para almacenar el string
      int bytes; // N\u00ba de bytes leidos

      // Escuchamos en el InputStream
      while (true) {
            try {
                // leemos
                bytes = ins.read(buffer);
                // enviamos lo leido al interfaz de usuario
                mHandler.obtainMessage(LEE_MSG, bytes, -1, buffer)
                .sendToTarget();
            } 
            catch (Exception ex) {
                break;
            }
      }
  }

  /* procedimiento para finalizar la conexi\u00f3n */
  public void cancel() {
      try {
           DataSocket.close();
      } 
      catch (Exception ex) { 
      }
  }
}
  

}
