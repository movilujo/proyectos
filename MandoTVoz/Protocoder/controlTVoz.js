/*
*
* Description: Experimento para controlar una televisión con voz
* by ........ Jose Luis Villarejo
* date ...... Diciembre - 2014
*
*/
// Start and Connect Bluetooth
network.startBluetooth();
network.connectBluetoothSerialByMac("98:D3:31:20:1A:75", function(data) {
console.log(data);
});
ui.setScreenMode("fullscreen");
ui.setBackgroundColor(100, 100, 100);

var oido   = ui.addText("", 20, 20, 100, 300);
var envio;

var btn = ui.addImageButton(250, 450, 250, 250, "VoztoBT.png", function(){
    media.startVoiceRecognition(function(text) {

          console.log(text);

          switch(text) {
            case "on":
                envio = "W";
                break;
            case "1":
                envio = "1";
                break;
            case "2":
                envio = "2";
                break;
            case "3":
                envio = "3";
                break;
            case "4":
                envio = "4";
                break;
            case "5":
                envio = "5";
                break;
            case "6":
                envio = "6";
                break;
            case "7":
                envio = "7";
                break;
            case "8":
                envio = "8";
                break;
            case "9":
                envio = "9";
                break;
            case "0":
                envio = "0";
                break;
            case "sube":
                envio = "P";
                break;
            case "baja":
                envio = "D";
                break;
            case "mas":
                envio = "M";
                break;
            case "menos":
                envio = "-";
                break;
          }
          
          oido.setText("Oido: " + text + " envío: " + envio);
          network.sendBluetoothSerial(envio);
      });
 });