//create an array from 3 to 10
int ledPin[]={
  4,5,6,7,8,9,10,11};
int minNum = 0;
int maxNum = 255;
int inByte =0;
int buttonState = 1;
int previousButtonState = 1;
int buttonCount = 0;
int autoCounter = 0;
int autoDelta = 1;
bool goBack = false;
bool pause = false;
bool trigger = false;
String command ="";
String val = "";
String inputString = "";
int previousPot = 0;
#define button 2

void setup() {

    for (int i = 0; i < 9; i++) { 
        pinMode(ledPin[i], OUTPUT); // set pin to output

    } // for loop ends
    
    pinMode(A0,INPUT); // set pin A0 as input
    pinMode(button,INPUT_PULLUP); // set button pin as input with internal pullup resistor
    Serial.begin(9600); // start serial communication
    Serial.print("Enter: \n 1 for Button push/release mode \n 2 for Serial display mode \n 3 for POT value display \n 4 for Programmable mode ");
    attachInterrupt(0,buttonPushed,FALLING);
    
} // setup ends


void loop() {

        //choice is the serial interrupted input
    int choice = Serial.parseInt(); // read the input
    //switch-case statement to determine the choice from 1 to 4
  if(goBack){
        choice = 4;
        }  
  switch(choice){
        case(1):
              Serial.println("\nButton Push/Release Mode is Activated!");
              Serial.println("1-Byte-Display will increment each time button pushed or released!");
              func1();
            
        case(2):
              Serial.println("\nSerial display Mode is Activated!");
              Serial.println("1-Byte-Display will show the number that you send from the Serial port!");
          func2();
            
        case(3):
                Serial.println("\nPOT Value Display Mode is Activated!");
              Serial.println("1-Byte-Display will show the number that you send from the Potentiometer!");
          previousPot = analogRead(A0); 
          func3();
                
        case(4):
                if (goBack == false){
                Serial.println("\nProgrammable Mode is Activated!");
                }
                func4();
        case(5):
                previousPot = analogRead(A0); 
                func5();
                if(trigger){
        choice = 5;
      }
      
      
      
     

    }// swich-case statement ends
      
} // loop ends

void func1(){
    while(1){
        buttonState = digitalRead(button); // read the state of the button
        if (buttonState != previousButtonState){ // if the button state has changed
            buttonCount++; // increment the button count
            Serial.print("Displayed Value is:");
            Serial.println(buttonCount);
            delay(10); // wait for 10 milliseconds
        }
        previousButtonState = buttonState; // update the previous button state
        byteReader(buttonCount); // call the byteReader function
    }
} // func1 ends

void func2(){
    while(1){
        if (Serial.available()) {
            // get incoming decimal number:            
            inByte = Serial.parseInt(); // read the input with the ssetting of no line ending
            if (inByte > 255) { // if the input is greater than the maximum number
                inByte = 255; // set the input to the maximum number
                Serial.println("Crap! I can display at most 255!");
            }
            if (inByte < 0) { // if the input is greater than the maximum number
                inByte = 0; // set the input to the maximum number
                Serial.println("Crap! I can display at least 0!");
            }
            Serial.print("Displayed Value is:");
            Serial.println(inByte);
            
            
        }
      
      byteReader(inByte); // call the byteReader function      
    }
} // func2 ends

void func3(){
    while(1){
        int potRead = analogRead(A0); // read the value of the potentiometer
        if (abs(potRead-previousPot)>2){
        Serial.print("Displayed Value is:");
        Serial.println(potRead/4); // print the value of the potentiometer
        byteReader(potRead/4);  // call the byteReader function
        previousPot = potRead;
        }    
        }
} // func3 ends

void func4(){
    while(!(pause)){
        autoCounter += autoDelta; // increment the autoCounter
        byteReader(autoCounter);  // call the byteReader function
        delay(500); // wait for 500 milliseconds
        if(autoCounter == minNum || autoCounter == maxNum) autoDelta = -autoDelta;  // if the autoCounter is equal to the minimum number or the maximum number, change the autoDelta
        if(autoCounter > maxNum){
        Serial.println("Your display is above maximum value! Display will start from 0");
        autoCounter = 0;
        }
      if(trigger){
      break;}
    }
} // func4 ends

void func5(){
  while(1){
  
   if(Serial.available()){
      command = Serial.readString();
      if(command == "!p:") {
       pause = true;
       Serial.println("Paused");
           }
     if (command == "!c:"){
       pause = false;
       Serial.println("Continued");
     } 
          if (command[1] == 'm' && command[0]=='!' && command[command.length()-1] == ':') {
          val = "";
            if (isDigit(command[4])){
                val +=command[2];
                val +=command[3];
                val +=command[4];
            }
            else{
                val +=command[2];
                val +=command[3];
            }
            maxNum=val.toInt();
          Serial.println("Maximum Number Set as:");
          Serial.println(maxNum);
        }
 }
    int potRead = analogRead(A0);
    if (abs(potRead-previousPot)>2 ){
      maxNum = map(potRead, 0, 1023, 10, 255);
      Serial.println("Maximum Number Set as:");
      Serial.println(maxNum);
      
            previousPot = potRead;  
    }
    buttonState = digitalRead(button);
    if(buttonState == 1){
      trigger = false;
      goBack = true;

      break;
    }
}
}
void  byteReader(byte decimalNum){
    for(int i = 0; i < 8; i++) { // for loop to iterate through the array
        if (bitRead(decimalNum,i)==1){ // if the bit is 1
            digitalWrite(ledPin[i],HIGH); // turn on the led
        }
        else{ // if the bit is 0
            digitalWrite(ledPin[i],LOW); // turn off the led
        }
  } // for loop ends
} // byteReader ends

void buttonPushed(){
       trigger=true;    
}
