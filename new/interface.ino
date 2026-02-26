#include <Adafruit_MAX31865.h>
#include <ArduinoJson.h>
#include "config.h"

// MAX31865 sensors array
Adafruit_MAX31865* sensors[4];

#define RREF 4300.0
#define RNOMINAL 1000.0
#define SENSOR_ERROR -999.0

// State variables
float temperatures[4] = {0, 0, 0, 0};
float setpoints[3] = {SETPOINT1, SETPOINT2, SETPOINT3};
float alarmLimits[3] = {ALARM1, ALARM2, ALARM3};
float warningLimits[3] = {WARNING1, WARNING2, WARNING3};
float outputPercent[3] = {0, 0, 0};
bool heaterEnabled[3] = {true, true, true};
bool forceOn[3] = {false, false, false};
bool warnings[3] = {false, false, false};
bool alarms[3] = {false, false, false};
bool heaterState[3] = {false, false, false};
uint8_t sensorFaults[4] = {0, 0, 0, 0};

unsigned long lastSample = 0;
unsigned long windowStart[3] = {0, 0, 0};

const int heaterPins[3] = {HEATER1_PIN, HEATER2_PIN, HEATER3_PIN};
const int ledPins[3] = {LED1_PIN, LED2_PIN, LED3_PIN};

// Relay state
const int relayPins[4] = {RELAY1_PIN, RELAY2_PIN, RELAY3_PIN, RELAY4_PIN};
const int relayLedPins[4] = {RELAY_LED1_PIN, RELAY_LED2_PIN, RELAY_LED3_PIN, RELAY_LED4_PIN};
const int buttonPins[4] = {BUTTON1_PIN, BUTTON2_PIN, BUTTON3_PIN, BUTTON4_PIN};
bool relayState[4] = {false, false, false, false};
bool lastButtonState[4] = {HIGH, HIGH, HIGH, HIGH};
unsigned long lastDebounce[4] = {0, 0, 0, 0};

void setup() {
  Serial.begin(SERIAL_BAUD);
  
  // Initialize sensor array
  const int sensorCS[4] = {SENSOR_CS1, SENSOR_CS2, SENSOR_CS3, SENSOR_CS4};
  for (int i = 0; i < 4; i++) {
    sensors[i] = new Adafruit_MAX31865(sensorCS[i], MAX31865_SDI, MAX31865_SDO, MAX31865_CLK);
    sensors[i]->begin(MAX31865_3WIRE);
  }
  
  // Initialize heater pins
  for (int i = 0; i < 3; i++) {
    pinMode(heaterPins[i], OUTPUT);
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(heaterPins[i], LOW);
    digitalWrite(ledPins[i], LOW);
  }
  
  // Initialize relays and buttons
  for (int i = 0; i < 4; i++) {
    pinMode(relayPins[i], OUTPUT);
    pinMode(relayLedPins[i], OUTPUT);
    pinMode(buttonPins[i], INPUT_PULLUP);
    digitalWrite(relayPins[i], HIGH); // OFF (active LOW)
    digitalWrite(relayLedPins[i], LOW);
  }
}

void loop() {
  unsigned long now = millis();
  
  // Sample temperatures
  if (now - lastSample >= SAMPLE_RATE_MS) {
    lastSample = now;
    readTemperatures();
    updateControl();
  }
  
  // Time-window control
  controlHeaters(now);
  
  // Handle relay buttons
  handleButtons();
  
  // Handle JSON commands
  if (Serial.available()) {
    handleCommand();
  }
}

void readTemperatures() {
  for (int i = 0; i < 4; i++) {
    uint16_t rtd = sensors[i]->readRTD();
    uint8_t fault = sensors[i]->readFault();
    sensorFaults[i] = fault;
    
    if (fault) {
      temperatures[i] = SENSOR_ERROR;
      sensors[i]->clearFault();
    } else {
      temperatures[i] = sensors[i]->temperature(RNOMINAL, RREF);
    }
  }
}

void updateControl() {
  for (int i = 0; i < 3; i++) {
    // Skip if sensor error
    if (temperatures[i] == SENSOR_ERROR) {
      heaterEnabled[i] = false;
      outputPercent[i] = 0;
      warnings[i] = false;
      alarms[i] = true;
      continue;
    }
    
    // Check warnings and alarms
    warnings[i] = temperatures[i] >= warningLimits[i];
    alarms[i] = temperatures[i] >= alarmLimits[i];
    
    // Safety: disable on alarm or over-temp
    if (alarms[i] || temperatures[i] >= MAX_TEMP) {
      heaterEnabled[i] = false;
      forceOn[i] = false;
    }
    
    // Calculate output
    if (!heaterEnabled[i]) {
      outputPercent[i] = 0;
    } else if (forceOn[i]) {
      outputPercent[i] = 100;
    } else {
      float error = setpoints[i] - temperatures[i];
      outputPercent[i] = constrain(error * P_GAIN, 0, 100);
    }
  }
}

void controlHeaters(unsigned long now) {
  for (int i = 0; i < 3; i++) {
    // Reset window
    if (now - windowStart[i] >= TIME_WINDOW_MS) {
      windowStart[i] = now;
    }
    
    // Calculate on-time
    unsigned long onTime = (TIME_WINDOW_MS * outputPercent[i]) / 100;
    bool shouldBeOn = (now - windowStart[i]) < onTime;
    
    // Apply state
    if (heaterEnabled[i] && shouldBeOn) {
      digitalWrite(heaterPins[i], HIGH);
      heaterState[i] = true;
    } else {
      digitalWrite(heaterPins[i], LOW);
      heaterState[i] = false;
    }
    
    // LED control
    if (!heaterEnabled[i]) {
      digitalWrite(ledPins[i], LOW);
    } else if (forceOn[i]) {
      digitalWrite(ledPins[i], HIGH);
    } else if (alarms[i]) {
      digitalWrite(ledPins[i], (millis() / LED_BLINK_MS) % 2);
    } else {
      digitalWrite(ledPins[i], heaterState[i]);
    }
  }
}

void handleButtons() {
  unsigned long now = millis();
  for (int i = 0; i < 4; i++) {
    bool reading = digitalRead(buttonPins[i]);
    
    if (reading != lastButtonState[i]) {
      lastDebounce[i] = now;
      lastButtonState[i] = reading;
    }
    
    if ((now - lastDebounce[i]) > DEBOUNCE_MS) {
      if (reading == LOW) {
        relayState[i] = !relayState[i];
        digitalWrite(relayPins[i], relayState[i] ? LOW : HIGH);
        digitalWrite(relayLedPins[i], relayState[i] ? HIGH : LOW);
        lastDebounce[i] = now + 1000; // Prevent rapid re-trigger
      }
    }
  }
}

void handleCommand() {
  String input = Serial.readStringUntil('\n');
  input.trim();
  
  StaticJsonDocument<512> doc;
  DeserializationError error = deserializeJson(doc, input);
  
  if (error) {
    sendError(0, "JSON parse error");
    return;
  }
  
  int id = doc["id"] | 0;
  const char* cmd = doc["cmd"];
  
  if (strcmp(cmd, "get_status") == 0) {
    sendStatus(id);
  } else if (strcmp(cmd, "set_setpoint") == 0) {
    int zone = doc["zone"] | 1;
    float value = doc["value"] | 0;
    if (zone >= 1 && zone <= 3) {
      setpoints[zone - 1] = value;
      sendStatus(id);
    } else {
      sendError(id, "Invalid zone");
    }
  } else if (strcmp(cmd, "set_output_percent") == 0) {
    int zone = doc["zone"] | 1;
    float value = doc["value"] | 0;
    if (zone >= 1 && zone <= 3) {
      outputPercent[zone - 1] = constrain(value, 0, 100);
      sendStatus(id);
    } else {
      sendError(id, "Invalid zone");
    }
  } else if (strcmp(cmd, "set_alarm") == 0) {
    int zone = doc["zone"] | 1;
    float value = doc["value"] | 0;
    if (zone >= 1 && zone <= 3) {
      alarmLimits[zone - 1] = value;
      sendStatus(id);
    } else {
      sendError(id, "Invalid zone");
    }
  } else if (strcmp(cmd, "set_warning") == 0) {
    int zone = doc["zone"] | 1;
    float value = doc["value"] | 0;
    if (zone >= 1 && zone <= 3) {
      warningLimits[zone - 1] = value;
      sendStatus(id);
    } else {
      sendError(id, "Invalid zone");
    }
  } else if (strcmp(cmd, "enable_heater") == 0) {
    int zone = doc["zone"] | 1;
    bool enable = doc["enable"] | false;
    if (zone >= 1 && zone <= 3) {
      heaterEnabled[zone - 1] = enable;
      sendStatus(id);
    } else {
      sendError(id, "Invalid zone");
    }
  } else if (strcmp(cmd, "force_heater_on") == 0) {
    int zone = doc["zone"] | 1;
    bool enable = doc["enable"] | false;
    if (zone >= 1 && zone <= 3) {
      forceOn[zone - 1] = enable;
      sendStatus(id);
    } else {
      sendError(id, "Invalid zone");
    }
  } else if (strcmp(cmd, "get_temperature") == 0) {
    sendStatus(id);
  } else if (strcmp(cmd, "emergency_stop") == 0) {
    for (int i = 0; i < 3; i++) {
      heaterEnabled[i] = false;
      forceOn[i] = false;
      digitalWrite(heaterPins[i], LOW);
    }
    sendStatus(id);
  } else if (strcmp(cmd, "ping") == 0) {
    sendStatus(id);
  } else if (strcmp(cmd, "set_relay") == 0) {
    int relay = doc["relay"] | 1;
    bool state = doc["state"] | false;
    if (relay >= 1 && relay <= 4) {
      relayState[relay - 1] = state;
      digitalWrite(relayPins[relay - 1], state ? LOW : HIGH);
      digitalWrite(relayLedPins[relay - 1], state ? HIGH : LOW);
      sendStatus(id);
    } else {
      sendError(id, "Invalid relay");
    }
  } else {
    sendError(id, "Unknown command");
  }
}

void sendStatus(int id) {
  StaticJsonDocument<768> doc;
  doc["id"] = id;
  doc["status"] = "ok";
  
  JsonObject data = doc.createNestedObject("data");
  
  JsonArray temps = data.createNestedArray("temperatures");
  for (int i = 0; i < 4; i++) temps.add(temperatures[i]);
  
  JsonArray sp = data.createNestedArray("setpoints");
  for (int i = 0; i < 3; i++) sp.add(setpoints[i]);
  
  JsonArray out = data.createNestedArray("outputs_percent");
  for (int i = 0; i < 3; i++) out.add(outputPercent[i]);
  
  JsonArray hs = data.createNestedArray("heater_state");
  for (int i = 0; i < 3; i++) hs.add(heaterState[i]);
  
  JsonArray fo = data.createNestedArray("force_on");
  for (int i = 0; i < 3; i++) fo.add(forceOn[i]);
  
  JsonArray en = data.createNestedArray("enabled");
  for (int i = 0; i < 3; i++) en.add(heaterEnabled[i]);
  
  JsonArray warn = data.createNestedArray("warnings");
  for (int i = 0; i < 3; i++) warn.add(warnings[i]);
  
  JsonArray alrm = data.createNestedArray("alarms");
  for (int i = 0; i < 3; i++) alrm.add(alarms[i]);
  
  JsonArray relays = data.createNestedArray("relays");
  for (int i = 0; i < 4; i++) relays.add(relayState[i]);
  
  JsonArray faults = data.createNestedArray("sensor_faults");
  for (int i = 0; i < 4; i++) faults.add(sensorFaults[i]);
  
  serializeJson(doc, Serial);
  Serial.println();
}

void sendError(int id, const char* message) {
  StaticJsonDocument<256> doc;
  doc["id"] = id;
  doc["status"] = "error";
  doc["message"] = message;
  serializeJson(doc, Serial);
  Serial.println();
}
