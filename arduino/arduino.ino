#include <Servo.h>
Servo omoplate; 
Servo shoulder; 
Servo rotate;  //Объявление имен серво   
Servo biceps;
Servo palm;
Servo finger1;
Servo finger2;
Servo finger3;
Servo finger4;
Servo finger5;


void setup(){
  //Подключение серво:
  omoplate.attach(11);
  omoplate.write(20);
  delay(1000);
  shoulder.attach(10);
  shoulder.write(30);
  delay(1500);
  rotate.attach(9);
  rotate.write(90);
  delay(1000);
  biceps.attach(8);
  biceps.write(5);
  delay(1000);
  palm.attach(7);
  finger1.attach(2);
  finger2.attach(3);
  finger3.attach(4);
  finger4.attach(5);
  finger5.attach(6);
  delay(1);
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
              omoplate.write(servoPos);
              break;
          case 10:
              shoulder.write(servoPos);
              break;
          case 9:
              rotate.write(servoPos);
              break;
          case 8:
              biceps.write(servoPos);
              break;
          case 7:
              palm.write(servoPos);
              break;
             
          case 2:
              finger1.write(servoPos);
              break;
          case 3:
              finger2.write(servoPos);
              break;
          case 4:
              finger3.write(servoPos);
              break;
          case 5:
              finger4.write(servoPos);
              break;
          case 6:
              finger5.write(servoPos);
              break;
         
        break;
        }
      } 
      case 'R':{
        Serial.end();
        delay(15);
        Serial.begin(115200);
        break;
      }
     
    }
   
  }
  
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
