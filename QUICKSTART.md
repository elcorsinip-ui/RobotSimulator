# 📍 DOVE TROVI IL PROGRAMMA E COME LANCIARLO

## Posizione

Il programma si trova nella cartella:

```
/root/RobotSimulator/
```

## Come lanciare l'applicazione

### Metodo 1: Streamlit Web UI (raccomandato)

```bash
cd /root/RobotSimulator
streamlit run app.py
```

Dopo aver lanciato il comando, apri il browser all'indirizzo:
```
http://localhost:8501
```

### Metodo 2: Script Python da terminale

Se vuoi usare il motore di calcolo senza UI:

```bash
cd /root/RobotSimulator
python3 -c "
from robotsimulator import VERSION, PROJECT_NAME
from robotsimulator.models import MouldGeometry, ObstacleEnvelope, RobotParameters, SwabbingParameters
from robotsimulator.trajectory import generate_trajectory

print(f'{PROJECT_NAME} v{VERSION}')
# ... tuo codice di calcolo ...
"
```

## Cosa vedrai all'avvio dell'app

Quando lanci `streamlit run app.py`, l'interfaccia mostrerà:

1. **Header** con:
   - Nome: "RobotSimulator"
   - Versione: v0.3.3 — 2026-06-28
   - License: Proprietary — Bottero Group S.p.A.

2. **Disclaimer di sicurezza** (in un expander "⚠️ SAFETY DISCLAIMER — Read before use")
   - Clicca per espandere e leggere tutti gli avvertimenti legali

3. **Sidebar** con:
   - Versione in basso: "v0.3.3 | 2026-06-28"
   - INPUT参数 (mould, lance, robot, swabbing)

4. **Area principale** con:
   - Definizione ostacoli
   - Pulsante "Calculate Trajectory"
   - Plot X-Z della traiettoria
   - Tabella dei punti
   - Bottoni di export (CSV, JSON, Report)

## Struttura dei file

```
RobotSimulator/
├── VERSION                    # File di versione (0.3.3)
├── LICENSE                    # Licenza proprietaria Bottero
├── CHANGELOG.md               # Storico versioni
├── README.md                  # Documentazione con badge GitHub
├── .gitignore                 # Git ignore rules
├── app.py                     ← ENTRY POINT PRINCIPALE (Streamlit)
├── requirements.txt           # Dipendenze Python
├── robotsimulator/            # Pacchetto Python
│   ├── __init__.py            # Export version constants
│   ├── version.py             # Modulo versioning centrale
│   ├── models.py              # Dataclasses
│   ├── geometry.py            # Motore geometrico
│   ├── collision.py           # Collision detection
│   ├── trajectory.py          # Generatore traiettoria
│   ├── velocity.py            # Modulazione velocità
│   ├── valve_timing.py        # Timing valvola
│   ├── export.py              # Export CSV/JSON/MD
│   └── plotting.py            # Plot matplotlib + Plotly
├── tests/                     # Test unitari (68 test)
├── data/                      # Dati di esempio
├── docs/                      # Documentazione
│   ├── architecture.md
│   ├── user_guide.md
│   ├── engineering_notes.md
│   ├── validation_plan.md
│   └── RELEASE.md             ← ISTRUZIONI PER PUBBLICARE SU GITHUB
└── outputs/                   # Output generati
```

## Per pubblicare su GitHub

Leggi il file:
```
/root/RobotSimulator/docs/RELEASE.md
```

Contiene le istruzioni passo-passo per:
- Aggiornare la versione
- Fare commit e tag
- Creare il release su GitHub

## Verifica rapida

Prima di chiudere, verifica che tutto funzioni:

```bash
cd /root/RobotSimulator
python3 -c "from robotsimulator import VERSION; print(f'Versione: {VERSION}')"
# Output: Versione: 0.3.3

pytest tests/ -v --tb=short
# Output: 68 passed
```

---

**Progetto completato e pronto per l'uso.** 🎉