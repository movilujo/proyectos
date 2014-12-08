/*
 * IRremote: IRrecvDump - dump details of IR codes with IRrecv
 * An IR detector/demodulator must be connected to the input RECV_PIN.
 * Version 0.1 July, 2009
 * Copyright 2009 Ken Shirriff
 * http://arcfn.com
 */

#include <IRremote.h>

int RECV_PIN = 11;

IRrecv irrecv(RECV_PIN);

decode_results results;

void setup()
{
  Serial.begin(9600);
  irrecv.enableIRIn(); // Start the receiver
}

// Dumps out the decode_results structure.
// Call this after IRrecv::decode()
// void * to work around compiler issue
//void dump(void *v) {
//  decode_results *results = (decode_results *)v
void dump(decode_results *results) {
  int count = results->rawlen;
  if (results->decode_type == UNKNOWN) {
    Serial.print("Unknown encoding: ");
  } 
  else if (results->decode_type == NEC) {
    Serial.print("Decoded NEC: ");
  } 
  else if (results->decode_type == SONY) {
    Serial.print("Decoded SONY: ");
  } 
  else if (results->decode_type == RC5) {
    Serial.print("Decoded RC5: ");
  } 
  else if (results->decode_type == RC6) {
    Serial.print("Decoded RC6: ");
  }
  else if (results->decode_type == PANASONIC) {
    Serial.print("Decoded PANASONIC: ");
  }
  else if (results->decode_type == JVC) {
    Serial.print("Decoded JVC: ");
  }
  else if (results->decode_type == SAMSUNG) {
    Serial.print("Decoded SAMSUNG: ");
  }
  int val1 = results->value;
  Serial.print(val1, HEX);
  Serial.print(" (");
  int valbits = results->bits;
  Serial.print(valbits, DEC);
  Serial.println(" bits)");
  Serial.print("Raw (");
  Serial.print(count, DEC);
  Serial.print("): ");

  for (int i = 0; i < count; i++) {
    if ((i % 2) == 1) {
      int valen = results->rawbuf[i]*USECPERTICK;
      Serial.print(valen, DEC);

    } 
    else {
      int negvalen =-(int)results->rawbuf[i]*USECPERTICK;
      Serial.print(negvalen, DEC);
    }
    Serial.print(", ");
  }
  Serial.println("");
}

void loop() {
  if (irrecv.decode(&results)) {
    int hexen = results.value;
    Serial.println(hexen, HEX);
    dump(&results);
    irrecv.resume(); // Receive the next value
  }
}
