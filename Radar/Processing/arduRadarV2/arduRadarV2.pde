/*
* Author: Jose Luis Villarejo Muñoz
* Date : Octubre 2014
*
* Este programa ha sido copiado de 
*        http://www.sistemasorp.es/2011/08/13/android-processing-bluetooth/
* y modificado levemente para poder utilizar la clase Radar de forma que pueda ser 
* como el simulador de un Radar.
* 
* El programa conecta mediante bluetooth con arduino en el que se ejecuta un programa que utiliza un sensor
* de Ultrasonidos para detectar objetos y utiliza la información recibida para visalizarla en un 
* dispositivo móvil.
*
*/

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
void setup()
{
  orientation(LANDSCAPE);
  miRadar = new Radar(displayHeight, displayWidth);
  f1 = loadFont("ArialMT-20.vlw");
  f2 = loadFont("ArialMT-15.vlw");
  stroke(255);  
}

void draw()
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
// Procedimientos control de flujo de Android y referentes a la conexión Bluetooth
//----------------------------------------------------------------------------------
void onStart()
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
void onStop()
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
void onActivityResult (int requestCode, int resultCode, Intent data)
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
void mouseReleased()
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
                 angulo = int(map(Integer.parseInt(values[0]), 0, 160, -80, 80));
                 distancia = int(map(Integer.parseInt(values[1]), 1, MAX_DISTANCE, 1, miRadar.radio));
                 println(angulo + ", "+distancia);
            } catch (Exception e) {}
        }
        break;
    }
   }
};

//----------------------------------------------------------------------
// Procedimientos referentes a la conexión Bluetooth
//-----------------------------------------------------------------------

//-----------------------------------------------------------------------
//  Obtenemos un listado de los dispositivos bluetooth que tenemos emparejados.
// Para que funcione este programa, el bluetooth que usemos en la parte Arduino debe estar
// emparejado previamente a nuestro dispositivo.
//-----------------------------------------------------------------------

void empieza()
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

void listaDispositivos(String texto, color c)
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
void compruebaEleccion()
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
//  Establecemos una conexión con el dispositivo seleccionado
//-----------------------------------------------------------------------
void conectaDispositivo() 
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
//  Dibujamos y mostramos en la pantalla del dispositivo móvil los datos obtenidos
//----------------------------------------------------------------------------------
void muestraDatos()
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
void muestraError()
{
  background(255, 0, 0);
  fill(255, 255, 0);
  textFont(f2);
  textAlign(CENTER);
  translate(width / 2, height / 2);
  rotate(3 * PI / 2);
  text(error, 0, 0);
}

