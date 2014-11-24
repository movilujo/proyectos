/*
*	
*	Description: Experimento para controlar un Printbot con el Acelerometro del móvil
*	by ........ Jose Luis Villarejo
*   date ...... Octubre - 2014
*
*/

// Start and Connect Bluetooth
network.startBluetooth();

network.connectBluetoothSerialByMac("XX:XX:XX:XX:XX:XX", function(data) {
    console.log(data);
});


ui.setFullscreen();

// forzamos modo Portrait 
ui.setScreenMode('portrait');

var rX = 0, rY = 0;
var Envio;
var accelerometer   = ui.addText("", 20, 20, 600, 100);

  sensors.startAccelerometer(function(x, y, z){ 
    rX = parseInt(x);
    rY = parseInt(y);
    
    if (Math.abs(rX) == Math.abs(rY)){
        Envio = 'S';   //Stop
    }
    else if (Math.abs(rX) > Math.abs(rY)){
            if (rX > 0){
               Envio = 'L'; //Izquierda
            }
            else {
                 Envio = 'R'; //Derecha
            }
        }
        else {
             if (rY > 0){
                Envio = 'D'; //Atras
             }
             else {
                Envio = 'U'; //Adelante
             }
         
        }
    
    accelerometer.setText("Posición: " + rX + ", " + rY + ", Envio: " + Envio );
    network.sendBluetoothSerial(Envio);
  });
