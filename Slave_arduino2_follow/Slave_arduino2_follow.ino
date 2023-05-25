nt enablePin = 9;
int motorPin1 = 10;
int motorPin2 = 11;


void setup() {
  // Set pin modes
  pinMode(enablePin, OUTPUT);
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  
  

  // Start with the motor stopped
  digitalWrite(enablePin, LOW);
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, LOW);

  // Start serial communication
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();

    if (command == 'b') {
      // Stop the motor
      digitalWrite(enablePin, LOW);
    } else if (command == 'a') {
      // Start the motor
      analogWrite(enablePin, 255);
      digitalWrite(motorPin1, HIGH);
      digitalWrite(motorPin2, LOW);
    }
    else if (command == 'c') {
      // Start the motor
      analogWrite(enablePin, 220);
      digitalWrite(motorPin1, HIGH);
      digitalWrite(motorPin2, LOW);
    }
    else if (command == 'd') {
      // Start the motor
      analogWrite(enablePin, 220);
      digitalWrite(motorPin1, HIGH);
      digitalWrite(motorPin2, LOW);
    }
    else if (command == 'e') {
      // Start the motor
      analogWrite(enablePin, 180);
      digitalWrite(motorPin1, HIGH);
      digitalWrite(motorPin2, LOW);
    }
    else if (command == 'f') {
      // Start the motor
      analogWrite(enablePin, 0);
      digitalWrite(motorPin1, HIGH);
      digitalWrite(motorPin2, LOW);
    }
  }
}