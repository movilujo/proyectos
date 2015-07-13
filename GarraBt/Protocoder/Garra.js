/*
*	
*	Description ........ Controlar por bluetooth una garra robótica
*	by ................. Jose Luis Villarejo
*   Fecha .............. Julio-2015
*
*/

ui.screenMode("immersive");
ui.toolbar.title("Garra_v5");
ui.toolbar.bgColor(201, 155, 51, 255);
ui.toolbar.show(true);
ui.screenOrientation("landscape");
ui.allowScroll(false);

var margin = 10;
var w = ui.screenWidth - 2*margin;
var h = 200;
var y = h + margin;
var x = 10 + margin;

var entero;
var max = 0;
var progress = 255;

var btStatus = true;
var btCliente;


var btnCnx = ui.addButton("Conectar BT", 10, 25);
btnCnx.background("#CC3300");
var btnDCnx = ui.addButton("Desconectar", 280, 25);
btnDCnx.background("#00CC00");
ui.alpha(btnDCnx, 0);

/* Etiquetas Rapido - lento - Rapido */

var vRapido = ui.addText("Rapido",x, h-45, 100, 75);
var vLento = ui.addText("Lento",w/2, h-45, 100, 75);
var vRapido2 = ui.addText("Rapido",w-100, h-45, 100, 75);
var vCerrar = ui.addText("Cerrar", x, h+75, 100, 75);
var vParar = ui.addText("Parar",w/2, h+75, 100, 75);
var vAbrir = ui.addText("Abrir", w-75, h+75, 100, 75);

var txt = ui.addText("", 10, 350, ui.screenWidth, -1);
var miSli;

miSli = ui.addSlider(x, y, w, h, max, progress);
miSli.setValue(128);
txt.text( Math.round(miSli.getValue()));
            
function envio(dato) { 
    if (btStatus === true) { 
       btCliente.send(dato + "\n"); 
       console.log(dato); 
   }
}

miSli.onChange(function(val) { 
    txt.text(val);
    if (btStatus === true) { 
        entero = Math.round(val); 
        console.log(entero);
        envio(entero);
    }
}); 

btnCnx.onClick(function() {
    btCliente = network.bluetooth.connectSerial(function(status) {
        console.log("Conectado " + status);
        miSli.setValue(128);
        if (status){
            ui.toast("Conectado");
            btStatus = status;
            console.log("btStatus = " +btStatus);
            ui.alpha(btnCnx, 0);
            ui.alpha(btnDCnx, 255);

        }
    });
    
    btCliente.onNewData(function(data) {
        parseIncomming(data); // "translate" data
        //Print Data in screen
        txt.text(data);
    });
    
});

btnDCnx.onClick(function() { // Creamos el botón de conectar
    miSli.setValue(128);
    envio(String.fromCharCode(128));
    btCliente.disconnect();
    btStatus= false;
    ui.alpha(btnCnx, 255);
    ui.alpha(btnDCnx, 0);
});
