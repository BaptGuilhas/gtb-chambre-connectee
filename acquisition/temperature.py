from pathlib import Path
from datetime import datetime
import csv
import time

# --- Configuration ---
PERIODE = 5          # Secondes entre acquisitions
DUREE = 60           # Durée de la session en secondes

CAPTEUR = Path("/sys/bus/w1/devices/28-08225491b425/w1_slave")
FICHIER_CSV = Path("temperatures.csv")


def lire_temperature():
    """Lire la sonde et retourner une température ou NaN."""

    try:
        lignes = CAPTEUR.read_text().splitlines()

        # Vérifier le CRC et la présence de la température
        if len(lignes) < 2 or not lignes[0].endswith("YES"):
            return float("nan")

        if "t=" not in lignes[1]:
            return float("nan")

        valeur = lignes[1].split("t=")[1]
        return int(valeur) / 1000

    except (OSError, ValueError, IndexError):
        # Sonde absente, erreur de lecture ou données incorrectes
        return float("nan")


# --- Préparation du fichier CSV ---
nouveau_fichier = not FICHIER_CSV.exists()

with FICHIER_CSV.open("a", newline="") as fichier:
    writer = csv.writer(fichier)

    if nouveau_fichier:
        writer.writerow(["horodatage", "temperature_c"])

    # --- Acquisition répétée ---
    debut = time.monotonic()
    prochaine_mesure = debut
    fin = debut + DUREE

    while prochaine_mesure < fin:

        # Attendre l'instant prévu pour la mesure
        attente = prochaine_mesure - time.monotonic()
        if attente > 0:
            time.sleep(attente)

        # Acquisition et horodatage
        temperature = lire_temperature()
        horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Enregistrement
        writer.writerow([horodatage, temperature])
        fichier.flush()

        print(f"{horodatage} | {temperature:.3f} °C")

        # Planifier l'acquisition suivante
        prochaine_mesure += PERIODE

print("Session terminée.")
