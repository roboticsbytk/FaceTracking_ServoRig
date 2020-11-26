/* Written by Roboticsbytk. (roboticsbytk.blogspot.com)
This code serves to read in the data from the Serial Port and processes it further. 
2 Servo's range of motion has been defined and the data is mapped onto the servos.
1 Servo is for Panning and the other is for tilting
Date=26/11/2020

This code was inspired mostly by the project written by Harsh Dethe 
link: https://create.arduino.cc/projecthub/WolfxPac/face-tracking-using-arduino-b35b6b
*/

#include <Servo.h>

Servo myservo;  // create servo object for tilting
Servo myservo2;  // create servo object for panning
//x and y will store the xy coordinates sent by the Python code
int x; 
int y;
//prevX and prevY will store the previous iteration's xy coordinates
int prevX;
int prevY;
//The initial positions for the servos are set below
int pos = 140;    //pos refers to the position for the tilt servo 
int pos2 = 60;//pos2 refers to the position for the pan servo 
void setup() {
  myservo.attach(6);  // attaches the servo on pin 6 
  myservo2.attach(9);  // attaches the servo on pin 9 
  Serial.begin(38400); //Baud rate set to 38400

  //writes the initial position values to the servos
  myservo.write(pos);
  myservo2.write(pos2); 
}

void loop() {
  while (Serial.available() > 0) { //only starts loop if Serial Port isnt empty

    if (Serial.read() == 'X') //THe encoded data comes in the form of  X _ _ Y _ _ Z
    {
      x = Serial.parseInt(); //we store the integers between X and Y, in the form of an INTEGER
          
      if (Serial.read() == 'Y')//Afterwards, we store the integers between Y and Z, in the form of an INTEGER
      {
        y = Serial.parseInt();
        Pos(); // we then start the function pos() to carry out mapping of the integer values
      }
    }   
  }
}

//The function pos() serves to map the values we got from the python code to
// a value that lies between the range of positions we want the servo to sweep through
//These individual values may vary depending on the size of your image, namely-> fromLow, fromHigh
//Or the way you have positioned your servos -> toLow, toHigh

//The tuned values will differ for each servo
void Pos()
{
  if (prevX != x || prevY != y) //CHecks to see if the x and y coordinates have changed
  {
    //pos2 receives width and stores for the PAN servo
    pos2 = map(x, 40, 244, 30,80 );
       //pos2 receives height and stores for the Tilt servo
    pos = map(y, 128, 48, 140, 170);

    //Making sure that the values don't go beyond the ranges
    pos2  = max(pos2, 30);
    pos2  = min(pos2, 80);
    
    pos  = max(pos, 140);
    pos = min(pos, 170);

    //sets the current xy positions to prevX and prevY
    prevX=x;
    prevY=y;
    //Writes to Servps
   myservo.write(pos);                     
   myservo2.write(pos2);
  
  }
}
