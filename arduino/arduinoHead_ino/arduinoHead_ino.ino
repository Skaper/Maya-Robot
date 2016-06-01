#include <Servo.h>
Servo rlrotate; 
Servo udrotate; 
Servo mouth;  //Объявление имен серво   


void setup(){
  //Подключение серво:
  rlrotate.attach(10);
  udrotate.attach(12);
  mouth.attach(11);
  mouth.write(0);
  rlrotate.write(90);
  udrotate.write(90);
  
  delay(1000);
  Serial.begin(115200);
  

}

void loop(){
  
  if(Serial.available()){
    
    String line = readlinePort();
    switch(line[0]){
      case 'S':{
        int indexD = line.indexOf('D');
        int indexBolshe = line.indexOf('>');
        int pinNamber = line.substring(indexD+1, indexBolshe).toInt();
        int servoPos = line.substring(indexBolshe+1).toInt();
        switch(pinNamber){
          case 11:
              mouth.write(servoPos);
              break;
          case 10:
              rlrotate.write(servoPos);
              break;
          case 12:
              udrotate.write(servoPos);
              break;
                   
        break;
        }
      } 
      case 'R':{
        Serial.end();
        delay(25);
        Serial.begin(115200);
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
