#include <Arduino.h>
// Define GPIO pins
const int gpioPins[5] = {5, 6, 7, 8, 10};

void setup() {
  // Initialize Serial communication over USB
  Serial.begin(115200);
  while (!Serial); // Wait for the Serial connection
  
  // Set GPIO pins as output
  for (int i = 0; i < 5; i++) {
    pinMode(gpioPins[i], OUTPUT);
    digitalWrite(gpioPins[i], LOW); // Turn off initially
  }

  Serial.println("ESP32-C3 GPIO Controller Ready");
  Serial.println("Use commands like 'on0', 'off0' to control GPIOs 0-9.");
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read the command
    command.trim(); // Remove any trailing newline or spaces

    if (command.startsWith("on")) {
      int pinIndex = command.substring(2).toInt(); // Extract the pin number
      if (pinIndex >= 0 && pinIndex < 5) {
        digitalWrite(gpioPins[pinIndex], HIGH);
        Serial.print("Turned ON GPIO ");
        Serial.println(gpioPins[pinIndex]);
      } else {
        Serial.println("Invalid pin number.");
      }
    } else if (command.startsWith("off")) {
      int pinIndex = command.substring(3).toInt(); // Extract the pin number
      if (pinIndex >= 0 && pinIndex < 5) {
        digitalWrite(gpioPins[pinIndex], LOW);
        Serial.print("Turned OFF GPIO ");
        Serial.println(gpioPins[pinIndex]);
      } else {
        Serial.println("Invalid pin number.");
      }
    } else {
      Serial.println("Unknown command. Use 'onX' or 'offX'.");
    }
  }
}
