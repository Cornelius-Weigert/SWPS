# IDOEL 🔍 – Interactive Detection of Outliers in Event Logs

> **"Garbage in, Garbage out."** IDOEL schließt die Lücke zwischen automatischer Ausreißer-Erkennung und menschlichem Domänenwissen im Process Mining.

---

## 📖 Über das Projekt

In der Praxis scheitern Process-Mining-Analysen oft an mangelnder Datenqualität. Herkömmliche Algorithmen zur Ausreißer-Erkennung agieren oft als "Blackbox" und löschen Datenpunkte rein statistisch, ohne den geschäftlichen Kontext zu verstehen.

**IDOEL (Interactive Detection of Outliers in Event Logs)** ist eine interaktive Webanwendung, die einen **Human-in-the-Loop-Ansatz** verfolgt. Sie ermöglicht es Domänenexperten, potenzielle Ausreißer systematisch zu validieren und so die Qualität der Inputdaten für das Process Mining nachhaltig zu steigern.

### Kernfunktionen
* **Interaktiver Upload:** Einfacher Import von Event Logs (CSV/XES).
* **Geführte Detektion:** Automatisierte Identifikation potenzieller Anomalien.
* **Experten-Validierung:** Intuitive UI zur Entscheidung über das Vorhandensein von Ausreißern.
* **Daten-Reparatur:** Export von bereinigten Logs für valide Analyseergebnisse.


## 🚀 Quick Start

### Voraussetzungen
Stelle sicher, dass Python 3.9+ installiert ist.

### Installation
1. Repository klonen:
   ```bash
   git clone [https://github.com/Cornelius-Weigert/SWPS.git](https://github.com/Cornelius-Weigert/IDOEL.git)
   cd IDOEL

2. Abhängigkeiten installieren:
   ```bash
   pip install pm4py pandas streamlit

3. Anwendung starten
Starte die Streamlit-App mit folgendem Befehl:
    ```bash
    streamlit run Dashboard.py


## 🛠 Technologie-Stack

* **Backend:** Python
* **Frontend:** [Streamlit](https://streamlit.io/) (Web-Framework)
* **Datenverarbeitung:** Pandas, PM4Py (Process Mining for Python)

## 🧬 Workflow in IDOEL

1. **Input:** Hochladen des Event Logs.
2. **Highlighting:** Markierung von Traces/Events mit hoher Ausreißer-Wahrscheinlichkeit.
3. **Human Decision:** Der Experte nutzt Schieberegler oder Buttons, um Ausreißer zu bestätigen oder als "validen Sonderfall" zu markieren.
4. **Output:** Download des optimierten Event Logs.
