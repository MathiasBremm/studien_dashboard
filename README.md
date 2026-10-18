# Studien-Dashboard

> **Kurs:** DLBDSOOFPP01 – Objektorientierte und funktionale Programmierung mit Python  
> **Studiengang:** B.Sc. Cyber Security, IU Internationale Hochschule  

Ein prototypisches, webbasiertes Dashboard zur Überwachung des eigenen Studienfortschritts. Die Anwendung visualisiert zentrale Studienmetriken (Gesamtschnitt, Notentendenz, ECTS-Soll/Ist-Tempo) und ermöglicht die interaktive Pflege des tabellarischen Notenspiegels mit persistenter Speicherung in einer JSON-Datei.

---

## Schnellstart & Installation

Das Projekt benötigt lediglich **Python ab Version 3.10** (empfohlen: Python 3.11–3.14).

### 1. Repository vorbereiten (optional: venv)

Es wird empfohlen, eine isolierte virtuelle Python-Umgebung zu verwenden:

```bash
# Virtuelle Umgebung erstellen
python -m venv .venv

# Virtuelle Umgebung aktivieren
# Linux / macOS:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Windows (cmd):
.venv\Scripts\activate.bat
```

### 2. Abhängigkeiten installieren

Das Dashboard benötigt lediglich `streamlit` und `pandas`:

```bash
pip install -r requirements.txt
```

*(Alternativ direkt: `pip install streamlit pandas`)*

### 3. Dashboard starten

Die Anwendung wird über Streamlit gestartet:

```bash
streamlit run dashboard_app.py
```

Das Dashboard öffnet sich anschließend automatisch im Browser unter **`http://localhost:8501`**.

---

## Projektstruktur & Schichtenarchitektur

Die Anwendung folgt einer sauberen Schichtenarchitektur unter Berücksichtigung der **SOLID-Prinzipien** (u. a. *Single Responsibility Principle* und *Dependency Inversion Principle*):

```text
POC_Python_Objektorientierte_Programmierung/
├── dashboard_app.py              # Application Root (Composition Root, Programmstart)
├── requirements.txt              # Externe Abhängigkeiten (streamlit, pandas)
├── studium_data.json             # Lokale Datenpersistenz (JSON)
│
├── domain/                       # Reines Domänenmodell (Fachobjekte als Dataclasses)
│   ├── studiengang.py            # Studiengang-Entität (Aggregat-Root)
│   ├── semester.py               # Semester-Entität
│   ├── modul.py                  # Modul-Entität
│   ├── pruefungsleistung.py      # Prüfungsleistung (Bestehenslogik / Single Source of Truth)
│   └── modul_status.py           # Enum für Bearbeitungsstatus
│
├── service/                      # Fachliche Geschäfts- und Rechenlogik
│   └── noten_service.py          # Notenschnitt, Notentrend, ECTS-Tempo, Zeitfortschritt
│
├── repository/                   # Persistenzschicht (kapselt Dateizugriff)
│   ├── i_modul_repository.py     # Abstraktes Repository-Interface (DIP)
│   └── json_modul_repository.py  # Konkrete JSON-Implementierung
│
├── controller/                   # Steuerungsschicht
│   └── dashboard_controller.py   # Koordination zwischen UI, Service und Repository
│
├── dto/                          # Datentransferobjekte (Entkopplung der Schichten)
│   ├── dashboard_daten_dto.py    # Aufbereitete Daten für die Anzeige
│   └── modul_eintrag_dto.py      # Tabellenzeilen-DTO für Datenaustausch mit der View
│
├── mapper/                       # Objekt-Transformation
│   └── modul_mapper.py           # Wandelt DTO-Einträge in Domänenobjekte um
│
└── view/                         # Präsentationsschicht (reine UI)
    └── dashboard_view.py         # Streamlit-Oberfläche (Metriken, Grafiken, Data Editor)
```

---

## Kernfunktionen des Dashboards

1. **Header-Bereich:**
   * Anzeige der Studentendaten, des Studiengangs und des Notenziels (2,0 oder besser).
   * Tagesaktuelle Berechnung des aktuellen Semesters und der verstrichenen Zeit in Prozent basierend auf dem `studienbeginn`.
2. **Zielbereich Noten:**
   * **Notendurchschnitt:** ECTS-gewichteter Gesamtschnitt aller bestandenen Module.
   * **Notentendenz:** Durchschnitt der letzten drei absolvierten Modulprüfungen inkl. Trend-Delta zur Vorperiode.
3. **Zielbereich Studiendauer & ECTS:**
   * Fortschrittsbalken über alle absolvierten ECTS (z. B. 90 / 180 ECTS).
   * Vergleich des zeitbasierten Soll-Tempos mit dem tatsächlich erreichten Ist-Tempo (ECTS/Semester).
4. **Interaktive Modulübersicht & Prüfungen:**
   * Tabellarischer Notenspiegel aller Module (`st.data_editor`).
   * Bearbeiten von Noten, Versuchen, Abgabe- und Prüfungsdaten direkt in der Weboberfläche.
   * Button **„Änderungen speichern“**: Persistiert geänderte oder neu hinzugefügte Module direkt in `studium_data.json` und aktualisiert alle Kennzahlen sofort.
