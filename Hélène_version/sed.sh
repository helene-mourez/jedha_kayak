#!/bin/bash

# Calcul des dates
today=$(date +%Y-%m-%d) récupère la date du jour au format AAAA-MM-JJ
checkout=$(date -d "+1 day" +%Y-%m-%d)

# Mise à jour des dates dans le fichier Python
sed -i -E "s/checkin=[0-9]{4}-[0-9]{2}-[0-9]{2}/checkin=${today}/" kayak_playwright_anti_detection_tempo.py
sed -i -E "s/checkout=[0-9]{4}-[0-9]{2}-[0-9]{2}/checkout=${checkout}/" kayak_playwright_anti_detection_tempo.py

# Lancement du script Playwright
python kayak_playwright_anti_detection_tempo.py