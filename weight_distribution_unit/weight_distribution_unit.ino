#include <HX711.h>
#include <SPI.h>
#include <SD.h>

#define TRIG 7
#define ECHO 6
#define PULSE 10

#define CONTROL_PULSE 100

#define LOADCELL_DOUT_PIN 3
#define LOADCELL_SCK_PIN 2

#define HEADER "d,F\n"

void generate_file();
void make_header();
void data_save(float d, float f);

HX711 scale;
File file;
char output_file[12] = {'W','X','_', '0', '0', '0', '.', 'c', 's', 'v', '\0'};

void setup() {
	Serial.begin(38400);
	while(!Serial);
	
	pinMode(TRIG, OUTPUT);
	pinMode(ECHO, INPUT);

	if(!SD.begin(10))
		Serial.println("SD initialization failed!");
	

  	scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);

  	scale.set_scale(1015.f);   
  	scale.tare();
}

void generate_file(){	
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

void make_header(){
	file = SD.open(output_file, FILE_WRITE);
	file.write(HEADER);
	file.close();
	
}

void data_save(float d, float f){
	file = SD.open(output_file, FILE_WRITE);
	file.print(d);
	file.write(",");
	file.print(f);
	file.write("\n");
	file.close();
}

void measure_start(){
	unsigned long ctrl_t = millis();
	unsigned long ctrl_prev = 0;
	unsigned long mtr_t = micros();
	unsigned long mtr_prev = 0;
	static byte mtr_state = LOW;
	float distance, load;

	if(ctrl_t - ctrl_prev >= CONTROL_PULSE){
		ctrl_prev = ctrl_t;
		if(mtr_t - mtr_prev >= PULSE){
			mtr_prev = mtr_t;
			mtr_state = !mtr_state;
			digitalWrite(TRIG, mtr_state);
			if(!mtr_state)
				 distance = 0.034 * pulseIn(ECHO, HIGH) / 2;
			}
			load = scale.get_units(5);
			Serial.println("s = ");
			Serial.print(distance);
			Serial.println("m = ");
			Serial.print(load);
			data_save(distance, load);	
	}
}

void loop(){
	static byte ctrl_state = LOW;
	if(Serial.read() == '\r'){
		ctrl_state = !ctrl_state;
	}

	if(ctrl_state == HIGH){
		generate_file();
		make_header();
		while(ctrl_state == HIGH){
			measure_start();
			if(Serial.read() == '\r'){
				ctrl_state = !ctrl_state;
			}
		}
	}
}
