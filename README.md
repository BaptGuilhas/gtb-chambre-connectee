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
