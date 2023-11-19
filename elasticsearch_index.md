PUT /office-input
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "time": {"type": "date",
        "format": "MM/dd/yyyy HH:ss||MM/d/yyyy HH:ss||MM/dd/yyyy H:ss||M/dd/yyyy HH:ss||MM/d/yyyy H:ss||M/d/yyyy HH:ss||yyyy-MM-dd HH:mm:ss",
        "ignore_malformed": true
      },
      "room": {"type": "keyword"},
      "temperature": {"type": "float"},
      "pir": {"type": "float"},
      "light": {"type": "float"},
      "humidity": {"type": "float"},
      "co2": {"type": "float"}
    }
  }
}