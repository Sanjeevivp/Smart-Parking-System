#include <Servo.h>

// ====== Servo Gate Section ======
Servo gateServo;
int entryIR = 9;       // IR sensor for gate (entry)
int servoPin = 8;      // Servo signal pin

// ====== Smart Parking System (5 Slots) ======
// IR Sensor pins for slots
int irSensor1 = 2;
int irSensor2 = 5;
int irSensor3 = 6;
int irSensor4 = 7;
int irSensor5 = A5; // Using A5 as digital pin (for 5th slot)

// LED pairs (Red = occupied, Green = empty)
int redLed1 = A2;
int greenLed1 = A3;

int redLed2 = A0;
int greenLed2 = A1;

int redLed3 = 12;
int greenLed3 = 13; // onboard LED for slot 3

int redLed4 = 10;
int greenLed4 = 11;

int redLed5 = 3;
int greenLed5 = 4;


// ====== Setup ======
void setup() {
  Serial.begin(9600);
  delay(2000);

  // Servo setup
  gateServo.attach(servoPin);
  gateServo.write(0); // start closed

  pinMode(entryIR, INPUT);

  // IR sensors for slots
  pinMode(irSensor1, INPUT);
  pinMode(irSensor2, INPUT);
  pinMode(irSensor3, INPUT);
  pinMode(irSensor4, INPUT);
  pinMode(irSensor5, INPUT);

  // LEDs for each slot
  pinMode(redLed1, OUTPUT);
  pinMode(greenLed1, OUTPUT);

  pinMode(redLed2, OUTPUT);
  pinMode(greenLed2, OUTPUT);

  pinMode(redLed3, OUTPUT);
  pinMode(greenLed3, OUTPUT);

  pinMode(redLed4, OUTPUT);
  pinMode(greenLed4, OUTPUT);

  pinMode(redLed5, OUTPUT);
  pinMode(greenLed5, OUTPUT);

  Serial.println("Smart Parking System + Servo Gate Ready...");
}

// ====== Loop ======
void loop() {
  // === Gate control ===
  int entryValue = digitalRead(entryIR);

  if (entryValue == LOW) { // Car detected at entry
    gateServo.write(90);  // Open gate
    Serial.println("Entry detected - Gate Open");
    delay(2000);           // keep open 3 sec
    gateServo.write(0);    // Close gate
  } 

  // === Parking Slots ===
  int s1 = digitalRead(irSensor1);
  int s2 = digitalRead(irSensor2);
  int s3 = digitalRead(irSensor3);
  int s4 = digitalRead(irSensor4);
  int s5 = digitalRead(irSensor5);

  // Slot 1
  if (s1 == LOW) {
    digitalWrite(redLed1, HIGH);
    digitalWrite(greenLed1, LOW);
  } else {
    digitalWrite(redLed1, LOW);
    digitalWrite(greenLed1, HIGH);
  }

  // Slot 2
  if (s2 == LOW) {
    digitalWrite(redLed2, HIGH);
    digitalWrite(greenLed2, LOW);
  } else {
    digitalWrite(redLed2, LOW);
    digitalWrite(greenLed2, HIGH);
  }

  // Slot 3
  if (s3 == LOW) {
    digitalWrite(redLed3, HIGH);
    digitalWrite(greenLed3, LOW);
  } else {
    digitalWrite(redLed3, LOW);
    digitalWrite(greenLed3, HIGH);
  }

  // Slot 4
  if (s4 == LOW) {
    digitalWrite(redLed4, HIGH);
    digitalWrite(greenLed4, LOW);
  } else {
    digitalWrite(redLed4, LOW);
    digitalWrite(greenLed4, HIGH);
  }

  // Slot 5
  if (s5 == LOW) {
    digitalWrite(redLed5, HIGH);
    digitalWrite(greenLed5, LOW);
  } else {
    digitalWrite(redLed5, LOW);
    digitalWrite(greenLed5, HIGH);
  }

  // Print status to Serial Monitor
  Serial.print("Slots: ");
  Serial.print(s1); Serial.print(" ");
  Serial.print(s2); Serial.print(" ");
  Serial.print(s3); Serial.print(" ");
  Serial.print(s4); Serial.print(" ");
  Serial.println(s5);

  delay(1000);
}
