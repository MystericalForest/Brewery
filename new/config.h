#ifndef CONFIG_H
#define CONFIG_H

// Heater pins
#define HEATER1_PIN 48
#define HEATER2_PIN 50
#define HEATER3_PIN 52
#define LED1_PIN 25
#define LED2_PIN 26
#define LED3_PIN 27

// MAX31865 pins
#define SENSOR_CS1 2
#define SENSOR_CS2 3
#define SENSOR_CS3 33
#define SENSOR_CS4 38
#define MAX31865_CLK 6
#define MAX31865_SDO 5
#define MAX31865_SDI 4

// Time-window & sampling
#define TIME_WINDOW_MS 10000
#define SAMPLE_RATE_MS 1000

// Serial
#define SERIAL_BAUD 115200

// Default setpoints
#define SETPOINT1 60.0
#define SETPOINT2 65.0
#define SETPOINT3 70.0

// Alarms
#define ALARM1 90.0
#define ALARM2 95.0
#define ALARM3 100.0

// Warnings
#define WARNING1 55.0
#define WARNING2 60.0
#define WARNING3 65.0

// Safety
#define MAX_TEMP 120.0

// Control parameters
#define P_GAIN 5.0
#define LED_BLINK_MS 200

// Relay pins (active LOW)
#define RELAY1_PIN 40
#define RELAY2_PIN 42
#define RELAY3_PIN 44
#define RELAY4_PIN 46

// Relay LED pins
#define RELAY_LED1_PIN 39
#define RELAY_LED2_PIN 41
#define RELAY_LED3_PIN 43
#define RELAY_LED4_PIN 45

// Button pins (INPUT_PULLUP)
#define BUTTON1_PIN 47
#define BUTTON2_PIN 49
#define BUTTON3_PIN 51
#define BUTTON4_PIN 53

// Debounce
#define DEBOUNCE_MS 50

#endif
