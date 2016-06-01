#include <Servo.h>
Servo rlrotate; 
Servo udrotate; 
Servo mouth;  //Объявление имен серво   
int power = 23;
int redR = A0; //0
int greenR = A1; //1
int blueR = A2;
int redL = A3; 
int greenL = A4; 
int blueL = A5;

void setup(){
  //Подключение серво:
  rlrotate.attach(10);
  udrotate.attach(12);
  mouth.attach(11);
  mouth.write(55);
  rlrotate.write(90);
  udrotate.write(90);
  
  delay(1000);
  Serial.begin(115200);
  
  pinMode(redR, OUTPUT);
  pinMode(greenR, OUTPUT);
  pinMode(blueR, OUTPUT);
  
  pinMode(power, OUTPUT);
  pinMode(redL, OUTPUT);
  pinMode(greenL, OUTPUT);
  pinMode(blueL, OUTPUT);
  
  
  analogWrite(redR, 255);
  analogWrite(greenR, 0);
  analogWrite(blueR, 0);
  
  analogWrite(redL, 0);
  analogWrite(greenL, 0);
  analogWrite(blueL, 0);
  
  

}

void loop(){
  
  if(Serial.available()){
    
    String line = readlinePort();
    switch(line[0]){
      case 'S':{
        int indexD = line.indexOf('D');
        int indexBolshe = line.indexOf('>');
        int pinNamber = line.substring(indexD+1, indexBolshe).toInt();
        int sercoPos = line.substring(indexBolshe+1).toInt();
        switch(pinNamber){
          case 11:
              mouth.write(sercoPos);
              break;
          case 10:
              rlrotate.write(sercoPos);
              break;
          case 12:
              udrotate.write(sercoPos);
              break;
                   
        break;
        }
      } 
      
      case 'L':{
        int indexD = line.indexOf('D');
        int indexBolshe = line.indexOf('>');
        int pinNamber = line.substring(indexD+1, indexBolshe).toInt();
        int value = line.substring(indexBolshe+1).toInt();
        value = map(value, 0, 255, 0, 1023);
        switch(pinNamber){
          case 1:
             analogWrite(redL, value);
             break;
          case 2:
             analogWrite(greenL, value);
             break;
          case 3:
             analogWrite(blueL, value);
             break;
        }
        break;
      }
      
      case 'R':{
        int indexD = line.indexOf('D');
        int indexBolshe = line.indexOf('>');
        int pinNamber = line.substring(indexD+1, indexBolshe).toInt();
        int value = line.substring(indexBolshe+1).toInt();
        value = map(value, 0, 255, 0, 1023);
        switch(pinNamber){
          case 1:
             analogWrite(redR, value);
             break;
          case 2:
             analogWrite(greenR, value);
             break;
          case 3:
             analogWrite(blueR, value);
             break;
        }
        break;
      }
      case 'P':{
        int value = line.substring(1).toInt();
        //Serial.println(value);
        switch(value){
          case 1:
             digitalWrite(power, HIGH);
             break;
          case 0:
             digitalWrite(power, LOW);
             break;
         
        }
        break;
      }
     
    }
   
  }
  /**
  if(Serial.overflow()){
        Serial.end();
        delay(15);
        Serial.begin(115200);
  }**/
}

String readlinePort(){
  String command_pi = "";
  while (1){
    if(Serial.available( )){
      char buf = Serial.read();
      if(buf != '\n'){
        command_pi += buf;
      }else{
        return command_pi;
      }  
    }
  }
}
