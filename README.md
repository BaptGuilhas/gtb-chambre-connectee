# GTB – Chambre connectée

Projet personnel d'apprentissage de la **Gestion Technique du Bâtiment (GTB)**, réalisé à partir d'un Raspberry Pi et de capteurs électroniques.

## Objectifs

Construire progressivement un système permettant de mesurer, surveiller et, à terme, réguler certains paramètres d'une pièce.

La démarche repose sur des expérimentations concrètes : développer un premier système simple, tester son fonctionnement, identifier ses limites et ajouter progressivement de nouvelles fonctionnalités.

## Étape 1 – Acquisition de température

**État : première mesure validée.**

### Matériel

- Raspberry Pi 3 Model B
- Debian 13 (Trixie), 64 bits
- Sonde de température DS18B20
- Résistance de tirage de 4,7 kΩ
- Breadboard et fils de connexion

### Communication

La sonde utilise le protocole **1-Wire** et communique avec le Raspberry Pi sur GPIO4.

### Résultats

- Sonde détectée sous Linux
- Lecture des données depuis `/sys/bus/w1/devices/`
- Contrôle de validité de la mesure par CRC
- Première température mesurée : **21,187 °C**
- Observation de la réponse thermique de la sonde lors du réchauffement à la main et du refroidissement à l'air ambiant

## Prochaines expérimentations

1. Développer un programme Python pour lire la température.
2. Enregistrer des mesures horodatées dans un fichier CSV.
3. Visualiser l'évolution de la température.
4. Étudier la réponse dynamique du capteur.

## Évolutions envisagées

- Supervision des mesures
- Régulation automatique
- Communication entre équipements
- Découverte de protocoles utilisés en GTB, notamment Modbus

Ces fonctionnalités seront développées et documentées progressivement.

## Étape 2 – Acquisition périodique et gestion des défauts

**État : test de 60 secondes réalisé avec succès le 4 novembre 2026.**

Le programme [`acquisition/temperature.py`](acquisition/temperature.py) réalise une acquisition toutes les 5 secondes, avec une durée de session configurable. Il vérifie les données retournées par le pilote 1-Wire, convertit la température en °C et écrit chaque résultat horodaté dans un fichier CSV. En cas d'erreur de lecture ou de mesure invalide, il enregistre `NaN` et poursuit la session.

### Test de déconnexion volontaire

Les données de l'essai sont conservées dans [`mesures/test_deconnexion.csv`](mesures/test_deconnexion.csv).

- **12 acquisitions** sur une session de 60 secondes (instants prévus de 0 à 55 s).
- **10 mesures valides**, 2 mesures invalides (`NaN`).
- **10:11:38 et 10:11:43** : déconnexion volontaire du capteur, mesures invalides.
- **10:11:48** : retour d'une mesure valide après reconnexion.
- **Résultat** : la session n'a pas été interrompue par la déconnexion.

Ce test valide la continuité de l'acquisition face à cette défaillance temporaire. Il ne constitue pas une validation complète de la robustesse du système.

### Exécution sur le Raspberry Pi

Depuis le dossier contenant le script :

```bash
python3 temperature.py
```

Le fichier `temperatures.csv` est créé ou complété dans le dossier courant.

### Limites connues

- Le chemin du capteur est propre à cette sonde et doit être adapté à un autre identifiant 1-Wire.
- Les acquisitions sont planifiées avec `time.monotonic()`, mais une lecture anormalement longue peut entraîner un rattrapage des échéances dépassées.
- L'enregistrement dans un seul CSV ne distingue pas encore les sessions.
- Les tests de fonctionnement prolongé restent à réaliser.
