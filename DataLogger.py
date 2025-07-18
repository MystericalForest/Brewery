from datetime import datetime, timedelta

class DataLogger:
    """
    Klasse til at logge termostat-data over tid.
    Gemmer temperatur, setpoint og andre parametre med tidsstempler.
    """
    def __init__(self):
        self.log = []  # Gemmer data i hukommelsen som en liste af dicts

    def log_data(self, data):
        """
        Logger nye data med tidsstempel.
        Logger kun hvis der er gået mindst 1 minut siden sidste log,
        eller hvis vigtige parametre har ændret sig.
        
        Args:
            data: Termostat data objekt
        """
        last_entry = self.get_last_entry()

        if last_entry is None:
            # Første log-indgang
            self.log.append({
                'timestamp': datetime.now(),
                'temperatur': data.temperatur,
                'setpoint': data.setpoint,
                'manual': data.manual,
                'heating': data.heating,
                'power': data.power
            })
        else:
            # Log hvis der er gået mindst 1 minut eller hvis vigtige parametre har ændret sig
            if (datetime.now() - last_entry["timestamp"] > timedelta(minutes=1)): 
                changed_data = (last_entry["setpoint"] != data.setpoint or 
                               last_entry["heating"] != data.heating or 
                               last_entry["manual"] != data.manual)
                
                # Log ændringer i parametre med sidste tidsstempel
                if changed_data:
                    self.log.append({
                        'timestamp': last_entry["timestamp"],
                        'temperatur': last_entry["temperatur"],
                        'setpoint': data.setpoint,
                        'manual': data.manual,
                        'heating': data.heating,
                        'power': last_entry["power"]
                    })

                # Log aktuelle værdier med nyt tidsstempel
                self.log.append({
                    'timestamp': datetime.now(),
                    'temperatur': data.temperatur,
                    'setpoint': data.setpoint,
                    'manual': data.manual,
                    'heating': data.heating,
                    'power': data.power
                })

    def get_log(self):
        """Returnerer hele loggen"""
        return self.log

    def get_last_entry(self):
        """Returnerer seneste log-indgang eller None hvis loggen er tom"""
        if len(self.log) == 0:
            return None
        return self.log[-1]