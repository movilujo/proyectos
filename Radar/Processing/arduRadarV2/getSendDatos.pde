/*
* Author: Jose Luis Villarejo Muñoz
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
      int bytes; // Nº de bytes leidos

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

  /* procedimiento para finalizar la conexión */
  public void cancel() {
      try {
           DataSocket.close();
      } 
      catch (Exception ex) { 
      }
  }
}
  
