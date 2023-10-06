## DATA MODEL

### Fields explaination:

- "labelId" : id de la localisation courante
- "cycleId" : id du cycle courant (un cycle toutes les 4s)
- "activityDecoded" : activité temporelle détectée sur le cycle courant.
- "bandwidthKHz" : la largeur de bande en kHz
- "freqRadioKHz" : la fréquence en kHz
- "coord" : la position latitude/longitude de la localisation courante
- "type" : le type de localisation (avions, bateaux, émetteurs fixes, véhicules terrestres, non identifiés)
- "is_master" : booléen, true si la localisation est la localisation maitre du réseau 
- "links" : liste des id des localisations qui communiquent avec la localisation courante
- "trajectory" : objet contenant les prédictions en coordonnées de T+1 à T+5


### Exemple de localisation:

```json
{
    "labelId": 1,
    "cycleId": 1,
    "activityDecoded": "1111111111111111111111111111111111111111111111111111111111111111",
    "bandwidthKHz": 2.783,
    "freqRadioKHz": 2790.7960000000003,
    "coord": {
      "lon": -3.2593666666666667,
      "lat": 48.58455,
      "alt": 0
    },
    "type": "avions",
    "is_master": true,
    "links": [3 ,4 ,5 ],
    "trajectory": {
      "coordT1": {
        "lon": -3.2593666666666667,
        "lat": 48.58455,
        "alt": 0
      },
      "coordT2": {
          "lon": -3.2593666666666667,
          "lat": 48.58455,
          "alt": 0
      },
      "coordT3": {
          "lon": -3.2593666666666667,
          "lat": 48.58455,
          "alt": 0
      },
      "coordT4": {
          "lon": -3.2593666666666667,
          "lat": 48.58455,
          "alt": 0
      },
      "coordT5": {
          "lon": -3.2593666666666667,
          "lat": 48.58455,
          "alt": 0
      }
    }
}
```

