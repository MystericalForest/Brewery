# JSON API Dokumentation
## Arduino Mega 3-Zone Varmecontroller

### Kommunikation
- **Baudrate:** 115200
- **Format:** JSON per linje, afsluttet med `\n`
- **Request:** Send JSON kommando
- **Response:** JSON svar med alle systemdata

---

## Standard Response Format

Alle succesfulde kommandoer returnerer:

```json
{
  "id": 1,
  "status": "ok",
  "data": {
    "temperatures": [23.4, 45.1, 50.0, 22.8],
    "setpoints": [60.0, 65.0, 70.0],
    "outputs_percent": [30.5, 50.0, 0.0],
    "heater_state": [true, true, false],
    "force_on": [false, false, false],
    "enabled": [true, true, false],
    "warnings": [false, false, false],
    "alarms": [false, false, false],
    "relays": [true, false, true, false],
    "sensor_faults": [0, 0, 0, 0]
  }
}
```

### Data Felter
| Felt | Type | Beskrivelse |
|------|------|-------------|
| `temperatures` | array[4] | Temperaturer fra 4 sensorer (°C). `-999.0` = sensor fejl |
| `setpoints` | array[3] | Setpoints for 3 varmezoner (°C) |
| `outputs_percent` | array[3] | Output procent 0-100% for hver zone |
| `heater_state` | array[3] | Aktuel heater tilstand (true=ON, false=OFF) |
| `force_on` | array[3] | Force ON status (true=100% output) |
| `enabled` | array[3] | Heater enabled status |
| `warnings` | array[3] | Advarsel aktiv (temp ≥ warning limit) |
| `alarms` | array[3] | Alarm aktiv (temp ≥ alarm limit) |
| `relays` | array[4] | Relæ tilstande (true=ON, false=OFF) |
| `sensor_faults` | array[4] | MAX31865 fejlkoder (0=OK, se fejlkode tabel) |

### Error Response
```json
{
  "id": 1,
  "status": "error",
  "message": "Invalid zone"
}
```

### MAX31865 Sensor Fejlkoder

Fejlkoder returneres i `sensor_faults` array (bit-flags):

| Bit | Hex  |   Fejl                             |  Beskrivelse            |
|-----|------|------------------------------------|-------------------------|
|  0  | 0x00 | OK                                 | Ingen fejl              |
|  7  | 0x80 | RTD High Threshold                 | RTD modstand for høj    |
|  6  | 0x40 | RTD Low Threshold                  | RTD modstand for lav    |
|  5  | 0x20 | REFIN- > 0.85 x Bias               | REFIN- spænding fejl    |
|  4  | 0x10 | REFIN- < 0.85 x Bias (FORCE- open) | REFIN- for lav          |
|  3  | 0x08 | RTDIN- < 0.85 x Bias (FORCE- open) | RTDIN- åben forbindelse |
|  2  | 0x04 | Overvoltage/undervoltage fault     | Spændingsfejl           |

**Eksempel:**
- `0` = Ingen fejl
- `8` (0x08) = RTDIN- åben forbindelse (sensor ikke tilsluttet)
- `132` (0x84) = RTD Low Threshold + Overvoltage fault

---

## Kommandoer

### 1. ping
Test forbindelse til enheden.

**Request:**
```json
{"id": 1, "cmd": "ping"}
```

**Response:** Standard response med alle data

---

### 2. get_status
Hent komplet systemstatus.

**Request:**
```json
{"id": 2, "cmd": "get_status"}
```

**Response:** Standard response med alle data

---

### 3. get_temperature
Hent temperaturer (alias for get_status).

**Request:**
```json
{"id": 3, "cmd": "get_temperature"}
```

**Response:** Standard response med alle data

---

### 4. set_setpoint
Sæt setpoint for en varmezone.

**Request:**
```json
{"id": 4, "cmd": "set_setpoint", "zone": 1, "value": 65.0}
```

**Parametre:**
- `zone`: 1-3 (varmezone nummer)
- `value`: Temperatur i °C

**Response:** Standard response med opdateret setpoint

---

### 5. set_output_percent
Manuel override af output procent.

**Request:**
```json
{"id": 5, "cmd": "set_output_percent", "zone": 2, "value": 75.0}
```

**Parametre:**
- `zone`: 1-3
- `value`: 0-100 (procent)

**Response:** Standard response med opdateret output

**Note:** Overskriver automatisk regulering indtil ændret igen

---

### 6. set_alarm
Sæt alarmgrænse for en zone.

**Request:**
```json
{"id": 6, "cmd": "set_alarm", "zone": 1, "value": 95.0}
```

**Parametre:**
- `zone`: 1-3
- `value`: Temperatur i °C

**Response:** Standard response

**Note:** Ved alarm slukkes heater automatisk

---

### 7. set_warning
Sæt advarselsgrænse for en zone.

**Request:**
```json
{"id": 7, "cmd": "set_warning", "zone": 1, "value": 55.0}
```

**Parametre:**
- `zone`: 1-3
- `value`: Temperatur i °C

**Response:** Standard response

---

### 8. enable_heater
Enable/disable en varmezone.

**Request:**
```json
{"id": 8, "cmd": "enable_heater", "zone": 2, "enable": true}
```

**Parametre:**
- `zone`: 1-3
- `enable`: `true` eller `false`

**Response:** Standard response

**Note:** Disabled heater = 0% output, LED slukket

---

### 9. force_heater_on
Tving heater til 100% output.

**Request:**
```json
{"id": 9, "cmd": "force_heater_on", "zone": 1, "enable": true}
```

**Parametre:**
- `zone`: 1-3
- `enable`: `true` (100% ON) eller `false` (normal regulering)

**Response:** Standard response

**Note:** LED lyser konstant ved force ON

---

### 10. set_relay
Styr relæ ON/OFF.

**Request:**
```json
{"id": 10, "cmd": "set_relay", "relay": 1, "state": true}
```

**Parametre:**
- `relay`: 1-4 (relæ nummer)
- `state`: `true` (ON) eller `false` (OFF)

**Response:** Standard response med opdateret relæ status

**Note:** Relæer kan også styres manuelt med knapper

---

### 11. emergency_stop
Sluk alle varmelegemer øjeblikkeligt.

**Request:**
```json
{"id": 11, "cmd": "emergency_stop"}
```

**Response:** Standard response med alle heaters disabled

**Note:** Sætter alle heaters til disabled og force_on til false

---

## Eksempler

### Opstart sekvens
```json
{"id": 1, "cmd": "ping"}
{"id": 2, "cmd": "get_status"}
{"id": 3, "cmd": "set_setpoint", "zone": 1, "value": 60.0}
{"id": 4, "cmd": "set_setpoint", "zone": 2, "value": 65.0}
{"id": 5, "cmd": "set_setpoint", "zone": 3, "value": 70.0}
```

### Overvågning
```json
{"id": 100, "cmd": "get_status"}
```
Send periodisk (f.eks. hvert sekund) for at overvåge systemet.

### Nødsituation
```json
{"id": 999, "cmd": "emergency_stop"}
```

---

## Safety Features

1. **Sensor fejl:** Heater slukkes automatisk hvis sensor returnerer `-999.0`
2. **Alarm:** Heater slukkes automatisk ved alarm (temp ≥ alarm limit)
3. **Max temp:** Heater slukkes ved temp ≥ 120°C (MAX_TEMP)
4. **Boot safe:** Alle SSR er LOW ved opstart
5. **Disabled heater:** Kan ikke tændes før enabled igen

---

## LED Status

| Tilstand | LED Adfærd |
|----------|------------|
| Heater disabled | OFF |
| Normal regulering | Blinker med heater state |
| Force ON 100% | Konstant ON |
| Alarm | Hurtig blink (200ms) |

---

## Hardware Mapping

### Varmezoner
- Zone 1: Sensor 1 → Heater 1 (pin 48) → LED (pin 25)
- Zone 2: Sensor 2 → Heater 2 (pin 50) → LED (pin 26)
- Zone 3: Sensor 3 → Heater 3 (pin 52) → LED (pin 27)
- Sensor 4: Reference/reserve

### Relæer
- Relæ 1: Pin 40 → LED pin 39 → Knap pin 47
- Relæ 2: Pin 42 → LED pin 41 → Knap pin 49
- Relæ 3: Pin 44 → LED pin 43 → Knap pin 51
- Relæ 4: Pin 46 → LED pin 45 → Knap pin 53

**Note:** Relæer er aktive ved LOW signal
