int enablePin = 9;
int motorPin1 = 11;
int motorPin2 = 10;

int trig1 = 4;
int echo1 = 5;
int trig2 = 6;
int echo2 = 7;
int trig3 = 8;
int echo3 = 12;


int LF_1 = A0;
int LF_2 = A1;
int LF_3 = A2;
int LF_4 = A3;
int LF_5 = A4;


float calculateDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH);
  float distance = duration * 0.034 / 2;
  return distance;
}

void setup() {
  // Set pin modes
  pinMode(enablePin, OUTPUT);
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  
  pinMode(trig1, OUTPUT); 
  pinMode(trig2, OUTPUT);
  pinMode(trig3, OUTPUT);
  
  pinMode(echo1, INPUT);
  pinMode(echo2, INPUT);
  pinMode(echo3, INPUT);

  pinMode(LF_1, INPUT);
  pinMode(LF_2, INPUT);
  pinMode(LF_3, INPUT);
  pinMode(LF_4, INPUT);
  pinMode(LF_5, INPUT);

  // Start with the motor stopped
  digitalWrite(enablePin, LOW);
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, LOW);

  // Start serial communication
  Serial.begin(9600);
}


void loop() {
  
  float distance2 = round(calculateDistance(trig2, echo2));

  // Stop the motor if the distance is less than 15
  if (distance2 < 15) {
    digitalWrite(enablePin, LOW);
    digitalWrite(motorPin1, LOW);
    digitalWrite(motorPin2, LOW);
    Serial.print("stop");

  }
  else {
    // Read line follower values
    int lf1 = digitalRead(LF_1);
    int lf2 = digitalRead(LF_2);
    int lf3 = digitalRead(LF_3);
    int lf4 = digitalRead(LF_4);
    int lf5 = digitalRead(LF_5);

    // Determine motor speed based on line follower readings
    int motorSpeed = 0;
    if (lf3 == HIGH) {
      motorSpeed = 220;  // Middle sensor detects line, full speed
      Serial.print("mid");
    }
    else if (lf2 == HIGH) {
      motorSpeed = 180;  // Left  sensor detects line, slower speed
      Serial.print("left");
    }
    else if (lf1 == HIGH) {
      motorSpeed = 0;    // Leftmost  sensor detects line, stop motor
      Serial.print("left left");
    }
    else if (lf4 == HIGH){
      motorSpeed = 220;    // right sensor detects line, stop motor
      Serial.print("right");
    }
    else if (lf5 == HIGH){
      motorSpeed = 220;    // rightmost sensor detects line, stop motor
      Serial.print("right right");
    }
    
    Serial.println();

    // Control the motor using the determined speed
    analogWrite(enablePin, motorSpeed);
    digitalWrite(motorPin1, HIGH);
    digitalWrite(motorPin2, LOW);
  }

  // Print the distance to the serial monitor
  

  delay(500); // Delay between readings
}