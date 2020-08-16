#include <SPI.h>
#include <SD.h>
#include <Wire.h>

#define LED 2
#define BUTTON 3
#define HEADER "ax,ay,az,gx,gy,gz,t\n"

#define MPU 0x68

unsigned long time, currentMillis, previousMillis, timestamp;
byte interval = 250;
char output_file[12] = {'E','X','_', '0', '0', '0', '.', 'c', 's', 'v', '\0'};
int results[6];

File file;

void errorBlink();
void generateFile();
void makeHeader();
void buzz();

void setup(){
 	Serial.begin(115200);
	
	if(!SD.begin(10)){
		Serial.println("Initialisation faiLED");
		errorBlink();
	}

	generateFile();
	
	Wire.begin();

 	Wire.beginTransmission(MPU);
 	Wire.write(0x6B);
 	Wire.write(0x00);
 	Wire.endTransmission(true);

 	Wire.beginTransmission(MPU);
 	Wire.write(0x1C);
 	Wire.write(0x11);
 	Wire.endTransmission(true);

 	Wire.beginTransmission(MPU);
 	Wire.write(0x1C);
 	Wire.write(0x10);
 	Wire.endTransmission(true);

 	pinMode(LED, OUTPUT);
	pinMode(BUTTON, INPUT);
}

void generateFile(){	
	while(SD.exists(output_file) == true){		
		if(output_file[5] == '9'){
			output_file[5] = '0';
			if(output_file[4] == '9'){
				output_file[4] = '0';
				if(output_file[3] == '9'){
					output_file[3] = '\0';
				} else {
					output_file[3]++;
				}
			} else {
				output_file[4]++;
			}
		} else {
			output_file[5]++;
		}
	}
}

void makeHeader(){
	file = SD.open(output_file, FILE_WRITE);
	file.write(HEADER);
	file.close();
	
}

void blink(byte dur){
	digitalWrite(LED,HIGH);
	delay(dur);
	digitalWrite(LED,LOW);
}


void errorBlink(){
	for(byte d; d < 200; d += 50){ 
		digitalWrite(LED, HIGH);
		delay(d);
		digitalWrite(LED, LOW);
		delay(200 - d);
	}
}

void buzz(){
	analogWrite(A0, 255);
	delay(100);
	analogWrite(A0, 0);
	delay(50);
	analogWrite(A0, 255);
	delay(250);
	analogWrite(A0, 0);
}

void writeToSD(){
	file = SD.open(output_file, FILE_WRITE);	
	
	for(int i = 0; i < 6; i++){
		file.print(results[i]);
		file.print(",");
	}
	
	file.print(timestamp);
	file.print("\n");

	file.close();
}


void doExp(bool state){
  	long k;
	
	if (state == true){
    		k = time - previousMillis;
    		time = millis();
    		if (k >= 100){
      			previousMillis = time;

      			Wire.beginTransmission(MPU);
      			Wire.write(0x3B);
     			Wire.endTransmission(false);
      			Wire.requestFrom(MPU, 6, true);
	
			results[0] = (Wire.read() << 8 | Wire.read()) / 409.6; 
			results[1] = (Wire.read() << 8 | Wire.read()) / 409.6;
			results[2] = (Wire.read() << 8 | Wire.read()) / 409.6;
			
			Wire.beginTransmission(MPU);
      			Wire.write(0x43);
      			Wire.endTransmission(false);
      			Wire.requestFrom(MPU, 6, true);

			results[3] = (Wire.read() << 8 | Wire.read()) / 32.8;
			results[4] = (Wire.read() << 8 | Wire.read()) / 32.8;
			results[5] = (Wire.read() << 8 | Wire.read()) / 32.8;
		
			writeToSD();	
			
			timestamp += 100;	
			blink(5);
    			
			}else{
		}
	}	
}

void loop(){
	static bool experimentState = false;
	if(digitalRead(BUTTON) == HIGH){
		delay(100);
		generateFile();
		experimentState = !experimentState;
		if(experimentState == true){
			makeHeader();
			buzz();
			timestamp = 0;
		}
	}
	
	doExp(experimentState);	
}
