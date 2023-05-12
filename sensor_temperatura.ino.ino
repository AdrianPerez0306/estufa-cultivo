#include <ArduinoUniqueID.h>
int temp; //lo q voy a recibir del valor valor entre 0 y 1023 
int pin=0; // donde conecte el sensor pin A0
char option; //para guardar lo que recibí de python
void setup() {
  Serial.begin(57600);
}
void loop() {

    if (Serial.available()) {
        option= Serial.read();
        if (option == '1'){           //Cadda vez que reciba de python un "1" voy arduino va a leer un dato 
            temp= analogRead(pin);  // acá le digo que lea lo que recibe del pin A0 
            Serial.println(temp);   //imprimo lo que leí
            delay(10);             // espero 
        }
        else{
          if(option =='2'){
            	for (size_t i = 0; i < UniqueIDsize; i++){          //imprime el SN 
		            if (UniqueID[i] < 0x10)
			          Serial.print("0");
		            Serial.print(UniqueID[i], HEX);
		            //Serial.print(" "); genera espacios cada dos cifras
	            }
	          Serial.println();
          }else{
            if(option =='3'){
              temp= analogRead(pin);
              Serial.println(temp);
              Serial.println("HANDSHAKING");
            }

          }
        }
    }

}

