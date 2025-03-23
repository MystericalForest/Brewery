#include <ArduinoJson.h>

const bool demo = true; // ret til false få at få indløste temperaturer

class Relay {
private:
  bool value;
  uint8_t relayPin; 

public:
  Relay(int RelayPin) {
    relayPin = RelayPin;
    
    // Sætter udgangspinnen som output
    pinMode(relayPin, OUTPUT);  
  }
  
  // Tænder for relæet
  void relayOn() {
    value = true;
    digitalWrite(relayPin, HIGH);
  }
  
  // Slukker for relæet
  void relayOff() {
    value = false;
    digitalWrite(relayPin, LOW);
  }
  
  // Henter den nuværende setpoint
  float getValue() {
    return value;
  }

  JsonDocument getJSON() {
  
      JsonDocument data;
      data["relay"]=value;

      return data;
  }
};

class Thermostat {
private:
  float setPoint;     // Den ønskede temperatur (setpoint)
  int outputPin;      // Den digitale udgang (f.eks. pin til relæ eller varmekilde)
  float tolerance;    // Hvor tæt temperaturen skal være på setpointet, før varmen slår til/fra
  float temperature;
  uint8_t termometerPin; 
  
public:
  // Konstruktor
  Thermostat(int OutputPin, uint8_t TermometerPin, float initialSetPoint, float toleranceValue) {
    outputPin = OutputPin;
    setPoint = initialSetPoint;
    tolerance = toleranceValue;
    temperature = initialSetPoint;
    termometerPin = TermometerPin;
    
    // Sætter udgangspinnen som output
    pinMode(outputPin, OUTPUT);
  }
  
  // Sætter setpoint (ønsket temperatur)
  void setSetPoint(float newSetPoint) {
    setPoint = newSetPoint;
  }
  
  // Henter den nuværende setpoint
  float getSetPoint() {
    return setPoint;
  }

  JsonDocument getJSON() {
  
      JsonDocument data;
      data["temperature"]=temperature;
      data["setPoint"]=setPoint;
      data["heating"]=digitalRead(outputPin);  

      return data;
  }
  
  float getTemperature() {
    if (demo) {
      if (digitalRead(outputPin)) {
        temperature += random(1,2);
      } else  {
        temperature -= random(1,2);
      }
    } else {
      // Her kan du tilføje kode til at læse en temperatur fra en sensor
      // For eksempel, hvis du bruger en analog temperaturmåler:
      int sensorValue = analogRead(termometerPin);  // Læs sensorværdi
      float voltage = sensorValue * (5.0 / 1023.0);  // Omregn til spænding
      temperature = (voltage - 0.5) * 100;  // Omregn spænding til temperatur (for LM35 f.eks.)
    }
    return temperature;
  }
  
  // Henter den nuværende temperaturmåling og styrer varmen
  void controlTemperature() {
    float currentTemp=getTemperature();
    // Tjekker om temperaturen er under setpoint minus tolerance
    if (currentTemp < (setPoint - tolerance)) {
      // Hvis temperaturen er lavere end ønsket, tænder vi varmen
      digitalWrite(outputPin, HIGH);
    }
    // Tjekker om temperaturen er over setpoint plus tolerance
    else if (currentTemp > (setPoint + tolerance)) {
      // Hvis temperaturen er højere end ønsket, slukker vi varmen
      digitalWrite(outputPin, LOW);
    }
  }
};

Thermostat thermostat1(11, A0, 62.0, 0.5);
Thermostat thermostat2(9, A1, 52.0, 0.5); 
Thermostat thermostat3(7, A2, 22.0, 0.5);  // Pin 7, setpoint 22 grader, tolerance 0.5 grader

Relay relay1(4);
Relay relay2(5);
Relay relay3(6);
Relay relay4(7);

// Generally, you should use "unsigned long" for variables that hold time
// The value will quickly become too large for an int to store
unsigned long previousMillis = 0;        // will store last time LED was updated

// constants won't change:
const long interval = 5000;           // interval at which to blink (milliseconds)

void setup() {
  // Initialiserer seriell kommunikation
  Serial.begin(9600);
  while (!Serial) {
    ; // Vent på, at serielporten er tilgængelig
  }
  succesMessage("Arduino er klar til at modtage JSON data.");
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  // Tjek om der er indkommende data
  if (Serial.available() > 0) {
    // Læs dataen
    String input = Serial.readStringUntil('\n');

    // Opret en JSON-dokumentbuffer
    JsonDocument doc;

    // Parse JSON-dataen
    DeserializationError error = deserializeJson(doc, input);

    if (error) {
      // Hvis der er en fejl i at parse JSON
      errorMessage("Fejl i at parse JSON!");
      return;
    }

    // Læs værdierne fra JSON-dokumentet
    const char* action = doc["action"];
    int value = doc["value"];

    // Reagér baseret på den modtagne JSON
    if (strcmp(action, "set_led") == 0) {
      set_led(value); 
    } else if (strcmp(action, "get_data") == 0) {
      get_data(value);
    } else if (strcmp(action, "get_temperature") == 0) {
      get_temperature(value);
    } else if (strcmp(action, "setpoint_1") == 0) {
      setpoint_1(value);
    } else if (strcmp(action, "setpoint_3") == 0) {
      setpoint_2(value);
    } else if (strcmp(action, "setpoint_3") == 0) {
      setpoint_3(value);
    }
    else {
      // Hvis action ikke er genkendt
      errorMessage("Ugyldig action.");
    }
  }
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    // save the last time you blinked the LED
    previousMillis = currentMillis;
    thermostat1.controlTemperature();
    thermostat2.controlTemperature();
    thermostat3.controlTemperature();
  }  
}

void errorMessage(String message) {
      sendMessage("Error", message);
}

void succesMessage(String message) {
      sendMessage("Succes", message);
}

void sendMessage(String status, String message) {
    JsonDocument response;
    response["status"] = status;
    response["message"] = message;

    sendJson(response);
}

void sendJson(JsonDocument json) {
    String output;
    serializeJson(json, output);
    Serial.println(output);
}

// {"action": "set_led", "value": 1}
void set_led(int value) {
      // Hvis action er "set_led", tænd/sluk for en LED baseret på value
      if (value == 1) {
        digitalWrite(LED_BUILTIN, HIGH);  // Tænd LED
      } else {
        digitalWrite(LED_BUILTIN, LOW);   // Sluk LED
      }
      
      // Send et JSON-svar tilbage
      JsonDocument response;
      response["status"] = "success";
      response["action"] = "set_led";
      response["value"] = value;
      
      sendJson(response);
}

// {"action": "get_temperature", "value": 1}
void get_data(int value) {
      // Send et JSON-svar tilbage
      JsonDocument response;
      response["status"] = "success";
      response["action"] = "get_data";
      if (value == 1) {
        response["Termostat1"] = thermostat1.getJSON();
      } else if (value == 2) {
        response["Termostat2"] = thermostat2.getJSON();
      } else if (value == 3) {
        response["Termostat3"] = thermostat3.getJSON();
      } else {
        response["Termostat1"] = thermostat1.getJSON();
        response["Termostat2"] = thermostat2.getJSON();
        response["Termostat3"] = thermostat3.getJSON();
        response["Relay1"] = relay1.getJSON();
        response["Relay2"] = relay2.getJSON();
        response["Relay3"] = relay3.getJSON();
        response["Relay4"] = relay4.getJSON();
      }
      
      sendJson(response);
}

// {"action": "get_temperature", "value": 1}
void get_temperature(int value) {
      // Send et JSON-svar tilbage
      JsonDocument response;
      response["status"] = "success";
      response["action"] = "get_temperature";
      if (value == 1) {
        response["Termostat1"] = thermostat1.getJSON();
      } else if (value == 2) {
        response["Termostat2"] = thermostat2.getJSON();
      } else if (value == 3) {
        response["Termostat3"] = thermostat3.getJSON();
      } else {
        response["Termostat1"] = thermostat1.getJSON();
        response["Termostat2"] = thermostat2.getJSON();
        response["Termostat3"] = thermostat3.getJSON();
      }
      
      sendJson(response);
}

// {"action": "setpoint_1", "value": 55}
void setpoint_1(int value) {
      thermostat1.setSetPoint(value);
      
      // Send et JSON-svar tilbage
      JsonDocument response;
      response["status"] = "success";
      response["action"] = "setpoint_1";
      response["value"] = value;
      
      sendJson(response);
}

// {"action": "setpoint_2", "value": 65}
void setpoint_2(int value) {
      thermostat2.setSetPoint(value);
      
      // Send et JSON-svar tilbage
      JsonDocument response;
      response["status"] = "success";
      response["action"] = "setpoint_2";
      response["value"] = value;
      
      sendJson(response);
}

// {"action": "setpoint_3", "value": 58}
void setpoint_3(int value) {
      thermostat3.setSetPoint(value);
      
      // Send et JSON-svar tilbage
      JsonDocument response;
      response["status"] = "success";
      response["action"] = "setpoint_3";
      response["value"] = value;
      
      sendJson(response);
}
