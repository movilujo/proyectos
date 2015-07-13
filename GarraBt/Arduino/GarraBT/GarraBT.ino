/* Baudios del Bluetooth*/
#define HC05              38400
#define BQ_ZUM_BT         19200
#define bufferSize 1

char myBuffer[bufferSize];
/* Buffer datos */
int ByteEntrada = 128;

int i = 0;
int nChar = 0;

String cmd;

/* Conexiones del motor CC */
int AIA = 9;  // (pwm) pin 9 connected to pin A-IA 
int AIB = 5;  // (pwm) pin 5 connected to pin A-IB 

/* Valores para enviar al motor */
int valA;
int valB;

void setGarra(int btValor){
//Damos un margen de seguridad dentro del cual el motor se para
  if ((btValor > 120) && (btValor < 140)) {
      stopM();
  }
  else {
      valA = btValor;
      valB = map(btValor, 0, 255, 255, 0);

      analogWrite(AIA, valA);
      analogWrite(AIB, valB);
  }
}

void stopM(){
  
  digitalWrite(AIA, HIGH);
  digitalWrite(AIB, HIGH);
  
}

void setup() {
  Serial.begin(BQ_ZUM_BT);
  Serial.flush();   
  pinMode(AIA, OUTPUT); // set pins to output
  pinMode(AIB, OUTPUT);
//  Serial.begin(9600);

}

void loop() {
  while(Serial.available()>0){
    int ByteEntrada = Serial.parseInt();
    
    if (Serial.read() == '\n'){
      ByteEntrada = constrain(ByteEntrada, 0, 255);
      setGarra(ByteEntrada);
    }    
  }
}  
