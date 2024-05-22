int VRx1 = A0; // X-axis pin for joystick 1
int VRy1 = A1; // Y-axis pin for joystick 1
int SW1 = 2;   // Button pin for joystick 1

int VRx2 = A2; // X-axis pin for joystick 2
int VRy2 = A3; // Y-axis pin for joystick 2
int SW2 = 3;   // Button pin for joystick 2

void setup() {
  Serial.begin(9600);
  pinMode(SW1, INPUT_PULLUP);
  pinMode(SW2, INPUT_PULLUP);
}

void loop() {
  // Read values from joystick 1
  int xValue1 = analogRead(VRx1);
  int yValue1 = analogRead(VRy1);
  int buttonState1 = digitalRead(SW1);

  // Read values from joystick 2
  int xValue2 = analogRead(VRx2);
  int yValue2 = analogRead(VRy2);
  int buttonState2 = digitalRead(SW2);

  // Map joystick 1 x-value
  int mappedX1;
  if (xValue1 < 499) {
    mappedX1 = -1;
  } else if (xValue1 > 501) {
    mappedX1 = 1;
  } else {
    mappedX1 = 0;
  }

  // Map joystick 1 y-value
  int mappedY1;
  if (yValue1 < 509) {
    mappedY1 = -1;
  } else if (yValue1 > 514) {
    mappedY1 = 1;
  } else {
    mappedY1 = 0;
  }

  // Map joystick 2 x-value
  int mappedX2;
  if (xValue2 < 499) {
    mappedX2 = 1;
  } else if (xValue2 > 502) {
    mappedX2 = -1;
  } else {
    mappedX2 = 0;
  }

  // Map joystick 2 y-value
  int mappedY2;
  if (yValue2 < 509) {
    mappedY2 = 1;
  } else if (yValue2 > 514) {
    mappedY2 = -1;
  } else {
    mappedY2 = 0;
  }

  // Send mapped values and button states over serial
  Serial.print(mappedX1);
  Serial.print(",");
  Serial.print(mappedY1);
  Serial.print(",");
  Serial.print(buttonState1);
  Serial.print(",");

  Serial.print(mappedX2);
  Serial.print(",");
  Serial.print(mappedY2);
  Serial.print(",");
  Serial.println(buttonState2);

  delay(100); // Adjust delay as needed
}
