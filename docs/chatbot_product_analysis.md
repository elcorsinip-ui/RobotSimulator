# BOTTERO CHATBOT / GLASS ASSIST AI - PRODUCT ANALYSIS
**Documento di riferimento per future analisi di Product Management**  
**Fonte:** Google Drive `\workspace\Chatbot\` e sottocartelle  
**Data analisi:** 2026-07-05  
**Analista:** Hermes Agent  

---

## 📁 STRUTTURA CARTELLA COMPLETA

```
Workspace/
├── Chatbot/                          (ID: 1uTB1axGjan3hE1fSNC7NwMQGPiw6RMfj)
│   ├── 01.Specifiche/                (ID: 1LFcnhVFFf1oDDjc3GZh_31DxDYaef8DJ)
│   │   ├── Documenti Tecnici/        (ID: 1Tcrk16n24pX5wH0bZdcpd0FAb4PYVVFq) — VUOTA
│   │   ├── Documenti di Progetto/    (ID: 1Wqdjz33YB4E5taXeyFh1KiFrt1AA-ohU)
│   │   │   ├── Analisi Brevettuale/  (ID: 1hZ04f_0KOgocozLZQ8a3Yha6YLEPKbAZ) — VUOTA
│   │   │   ├── Analisi Rischi/       (ID: 1QG_xWmbwfrLOvIx0j5--ioeG3NjtRxW0) — VUOTA
│   │   │   ├── Apertura Studio/      (ID: 1PZjH_znD04W1lT_yR6A9N_9bEChxR4Vd)
│   │   │   │   └── Sviluppo prodotto Glass Assist AI_0.0.0.1.xlsx
│   │   │   ├── Avanzamento Studio/   (ID: 1c_DE-NrhZ7PqwnfqghmDpmd7G6pBvE4x)
│   │   │   │   ├── Validazione/      (ID: 10zNNsxuLxBF9u1r40aoALwa0z8OQPjwu) — VUOTA
│   │   │   │   ├── Design Review/    (ID: 1rFlhW9nP31vSD5ZxPVoKUqv1V2y8qNcL) — VUOTA
│   │   │   │   └── Pianificazione Progetto/ (ID: 1X0VawGqMFzBpH1qCuhWTUeYJhL7yaQjb) — VUOTA
│   │   │   └── Specifica dei Requisiti/ (ID: 1waP3Wn407VAfPqfFkU5JJjLmwA-J3kGa)
│   │   │       ├── Bottero_Glass-AssistAI_DesignReview_60min_EN_v0.0.0.2.pptx
│   │   │       ├── Sviluppo prodotto Glass Assist AI_0.0.0.1.xlsx (DUPLICATO)
│   │   │       ├── MOD_PS~2.DOC
│   │   │       ├── Glass_Assist_AI_Gantt.xlsx
│   │   │       ├── Glass Assistant_Architecture_R02.pdf
│   │   │       ├── Glass Assistant_Architecture_R02.drawio
│   │   │       ├── Bottero_GlassAssist_Workflow_Flowchart.pptx
│   │   │       └── ApiExample.c#.txt
│   │   └── Vari/                     (ID: 1eAMVODUdGtAcSOWrXu8NpG_ZwnaaRrnk) — VUOTA
│   ├── 02.Commesse/                  (ID: 1nh_phBy-YmKQRQZD3C6QLrE-YHV-uf-g) — VUOTA
│   └── 03.AppuntiVari/               (ID: 1GG0qsKDOlAud--oBgSAvvDcs9snbDe8V) — VUOTA
├── EasyRock/                         (Cartella gemella - materiale prodotto EASYROCK)
├── Invert/                           (Feature servo invert anti-collision)
└── 01.Readme.txt                     ("Prima istanza workspace per BetterClaw")
```

---

## 📄 ANALISI DETTAGLIATA PER FILE

### 1. Sviluppo prodotto Glass Assist AI_0.0.0.1.xlsx (Preventivo Costi)
**Path:** `Chatbot/01.Specifiche/Documenti di Progetto/Apertura Studio/` + `Specifica dei Requisiti/` (duplicato)

#### Foglio: XA-SCHEDA PREV COSTI PROTOTIPO
| Centro Costo | Descrizione | Ore Assegnate | Note |
|---|---|---|---|
| 714 ELT. | Uff. R&D Elettrico Vetro Cavo | 240h | Progetto elettrico |
| 714 S/W | Uff. R&D Software Vetro Cavo | **720h** | **Core development** |
| 611 | Uff. Documentazione Vetro Cavo | 90h | Manuali |
| 912 | Assistenza tecnica Vetro Cavo | 72h | Testing/validazione |
| **TOTALE ORE LAVORO** | | **~1.122h** | Escluse voci a 0 |

#### Costi Aggiuntivi (Foglio RAZIONALE)
| Voce | Costo Base | Costo +150% | Note |
|---|---|---|---|
| Materiale su R&D | €25.000 | €37.500 | Hardware server, switch, etc. |
| Costi di trasferta | €3.500 | €5.250 | 2gg sopraluogo + 2gg install + 3gg finetuning |
| Fusioni | €0 | €0 | N.A. |
| Brevettuale | €0 | €0 | N.A. |
| Spedizione | €0 | €0 | N.A. |

#### Calcolo Gran Total
```
Gran Total = SUM(C14:I32)*57 + SUM(B39:B43)
          = 1.122h * €57/h + (€37.500 + €5.250)
          = €63.954 + €42.750
          = **€106.704**
```
**Nota:** "Costi e spese Glassform.ai escluse" — il chatbot si interfaccia a Glassform.ai ma non ne sviluppa il core.

#### Foglio RAZIONALE - Dettaglio Risorse
| Attività | Persone | Settimane | Ore Totali | Note |
|---|---|---|---|---|
| Progettazione Elettrica | 1 | 4 | | 240h | Configurabile: soluzione minima / PC pulpito / rete wireless |
| **Progettazione Software** | **1** | **12** | **720h** | Escluso sviluppo Glassform.ai. Incluso: pubblicazione allarmi/eventi gamma prodotto + preparazione oggetto interfaccia chatbot verso HTH, SCMU300, ELP400, Stacker |
| Montaggio/Testing SW (MVP1) | 1 | 1 | 40h | Validazione comm cliente finale, 1 sett lab R&D |
| Montaggio/Testing SW (MVP2) | 1 | 1.2 | 48h | Validazione AT, 6 sett 1gg/settimana |
| Documentazione | 1 | 1.5 | 60h | Manuale operatore basico con Glassform.ai |

---

### 2. Glass_Assist_AI_Gantt.xlsx (Project Plan)
**Path:** `Chatbot/01.Specifiche/Documenti di Progetto/Specifica dei Requisiti/`

#### Timeline Progetto
| Metrica | Valore |
|---|---|
| **Inizio** | 02/09/2024 |
| **Fine** | 23/10/2026 |
| **Durata** | 649 giorni (~21 mesi) |
| **% Completamento (al 11/04/2026)** | **58%** |
| **Proprietario** | Paolo Corsini |

#### Work Breakdown Structure (Task Principali)
| ID | Task | Inizio | Fine | Durata | Ore | Stato | Note |
|---|---|---|---|---|---|---|---|
| 44 | **GLASS-ASSIST AI** (Root) | 30/03/2026 | 23/10/2026 | 150gg | 1.569h | 0% | Backlog |
| 44.1 | MVP1 Kickoff | 22/04/2026 | 22/04/2026 | 0gg | — | Milestone | Sì |
| 44.2 | Interviews with champions | 07/04/2026 | 28/04/2026 | 16gg | 141h | Backlog | |
| 44.3 | Definition MVP use cases | 04/05/2026 | 08/05/2026 | 5gg | 42h | Backlog | |
| 44.4 | **Dataset preparation** | 30/03/2026 | 30/04/2026 | 24gg | 213h | Backlog | Macchina IS; HTH; Stacker; Swabbing Robot |
| 44.5 | Material supply (server, switch) | 18/05/2026 | 10/07/2026 | 40gg | 357h | Backlog | Per customer e AT |
| 44.6 | Product HW design | 20/04/2026 | 15/05/2026 | 20gg | 177h | Backlog | MVP1, MVP2, Product |
| 44.7 | **MVP2 Deployment + Validation** | 13/07/2026 | 30/09/2026 | 58gg | 519h | Backlog | Customer service area, triage workflow |
| 44.8 | Final product positioning | 01/09/2026 | 11/09/2026 | 9gg | 78h | Backlog | |
| 44.9 | **Glasstec Show** | 19/10/2026 | 23/10/2026 | 5gg | 42h | Backlog | Deadline fissa evento |
| 44.10 | MVP1 Installation | — | — | — | — | Backlog | Sotto "GLASSTEC 2024" |
| 44.11 | Glassform.ai SW development | — | — | — | — | Backlog | Sotto "GLASSTEC 2024" |
| 44.12 | Glassform.ai procedure doc | — | — | — | — | Backlog | Sotto "GLASSTEC 2024" |

#### Path Critico
`Dataset Prep (44.4)` → `HW Supply (44.5)` → `MVP2 Deployment (44.7)` → `Product Positioning (44.8)` → `Glasstec (44.9)`
- **MVP2 Deployment (58gg, 519h)** = task più lungo e rischioso
- **Glasstec 2026 (19-23 Ott)** = hard deadline non negoziabile

---

### 3. Glass Assistant_Architecture_R02.drawio/.pdf (System Architecture)
**Path:** `Chatbot/01.Specifiche/Documenti di Progetto/Specifica dei Requisiti/`

#### Componenti di Rete (3 Reti Separate)
| Rete | Colore | Componenti Chiave | Protocollo |
|---|---|---|---|
| **Factory Network** | 🟢 Verde | Switch/Firewall (52070100228799), Ethernet CAT6, 24Vdc wiring | Ethernet/Modbus TCP |
| **Automation Network** | 🔵 Blu | PLC, Inverter, Safety I/O, Encoder, RMC2 Controller, SPV400 UI, BRO700 UI | Profinet, IO-Link |
| **AI Network** | 🟠 Arancione | **SERVER 1**, FIELD UI, CONTROL ROOM UI, BOTTERO ROBOT L11, HTH L11, IS MACHINERY L11, STACKER L1 | Ethernet + NAT/Firewall |

#### Nodi Principali (con IP)
| Nodo | IP Factory | IP Automation | IP AI Network | Ruolo |
|---|---|---|---|---|
| **SERVER 1** | — | — | Centralizzato | AI/Chatbot Server |
| **FIELD UI** | — | — | Edge | Interfaccia operatore campo |
| **CONTROL ROOM UI** | — | — | Centralizzata | Supervisione |
| **BOTTERO ROBOT L11** | — | SPV400 UI, BRO700 UI | AI Network Card | Robot swabbing |
| **HTH L11** (SIEMENS/SCMU200/300) | — | — | 192.168.216.211 | Hot End |
| **IS MACHINERY L11** | — | — | — | Macchina formatura IS |
| **STACKER L1** | — | — | — | Impilatore |
| **HOT END L1X** | — | — | — | Forno aggiuntivo |

#### Network Translation / NAT
- **Supervisor Network Switch + NAT/Firewall**: `192.168.216.170 ⟷ 10.x.y.z`
- **AI Network Specific Card** su ogni nodo per segregazione traffico ML/inference
- **MODBUS TCP** per integrazione dati processo

#### Architettura Logica
```
[FACTORY NETWORK] ──NAT/FW── [SUPERVISOR NETWORK] ──AI NETWORK── [AI SERVER + EDGE UI]
       │                              │                         │
  Machine I/O                    PLC/Safety              Chatbot/Inference
  Modbus TCP                     Profinet                Model Serving
```

---

### 4. Bottero_GlassAssist_Workflow_Flowchart.pptx
**Path:** `Chatbot/01.Specifiche/Documenti di Progetto/Specifica dei Requisiti/`
- **Nota:** File scaricato ma contenuto non estratto (placeholder/vuoto come la Design Review)
- Presumibilmente flowchart: User Query → Intent Classification → Knowledge Retrieval (Glassform.ai + Doc DB) → Response Generation → Action Execution (se integrato)

---

### 5. Bottero_Glass-AssistAI_DesignReview_60min_EN_v0.0.0.2.pptx
**Path:** `Chatbot/01.Specifiche/Documenti di Progetto/Specifica dei Requisiti/`
- **10 slide vuote** (solo rettangoli placeholder)
- Template per Design Review 60 min — da popolare

---

### 6. ApiExample.c#.txt
**Path:** `Chatbot/01.Specifiche/Documenti di Progetto/Specifica dei Requisiti/`
- Esempio codice C# per chiamate API (probabilmente verso Glassform.ai o PLC)

---

### 7. MOD_PS~2.DOC
**Path:** `Chatbot/01.Specifiche/Documenti di Progetto/Specifica dei Requisiti/`
- Documento Word legacy (formato .DOC) — specifica prodotto/modello standard Bottero
- Non letto (richiede conversione)

---

## 🔗 COLLEGAMENTI CON ALTRI PROGETTI (Cartelle Gemelle)

### EasyRock/ (Cartella parallela — Prodotto Robotico Svasticazione Pallet)
**Rilevanza per Chatbot:** Il chatbot **EASY Assistant** (launch 2027) è citato nel roadmap EasyRock come *category-defining feature*. Stesso target cliente (Heineken, beverage/FMCG).

| Documento EasyRock | Insight per Chatbot |
|---|---|
| Executive Summary | Chatbot "EASY Assistant" 2027: voice-first, AR guidance, predictive alerts, training tracking |
| Strategy Report | Adaptive capabilities roadmap 2025-2030 (pallet/film/content) — il chatbot deve supportare questa evoluzione |
| Risk Matrix | **Risk COMM-1**: Customer dependency Heineken (340 linee) — chatbot deve ridurre training time 1 sett → 1 giorno |
| Presentation Script | Demo: Operatore: "Cosa devo fare?" → EASY: "Allarme X. Procedura: 1. Verifica Y... Video AR?" |

### Invert/ (Feature Servo Invert Anti-Collision)
**Rilevanza:** Caso d'uso reale di **diagnostica predittiva** (corrente + posizione) che il chatbot dovrà esporre/guidare.
- Feature implementata su SMC700 rel. 3.21 SP4
- GUI web parametrizzazione (role-based: Specialist/2705)
- Warning manuale/ciclo su soglie corrente/posizione
- Test live su linee L51/L61 (maggio 2026)

---

## 💰 ROI ANALYSIS (Basato su Dati Disponibili)

### Investment (CAPEX + OPEX 2024-2026)
| Voce | Importo | Note |
|---|---|---|
| Sviluppo Software (720h × €57/h) | €41.040 | Core chatbot |
| Sviluppo Elettrico (240h × €57/h) | €13.680 | HW integration |
| Documentazione (90h × €57/h) | €5.130 | Manuali |
| Assistenza Tecnica (72h × €57/h) | €4.104 | Testing |
| Materiale HW (Server, Switch) | €37.500 | +150% markup |
| Trasferte | €5.250 | +150% markup |
| **TOTALE INVESTIMENTO** | **€106.704** | Escluso Glassform.ai core |

### Benefici Attesi (da EasyRock Strategy + Invert Test)
| KPI | Baseline | Target | Valore Annuo Stimato |
|---|---|---|---|
| Training time operatori | 1 settimana | **1 giorno** | -85% onboarding cost |
| Troubleshooting resolution | Baseline | **-50% tempo** | Meno fermi linea |
| Manual access | Cartaceo/PDF | **100% voice** | Efficienza + sicurezza |
| First-call resolution (service) | ~60% | **>80%** | Meno trasferte service |
| OEE customer (Heineken) | 70% | **90%+** | €50M+ revenue opportunity (EasyRock doc) |

### Payback Estimation (Rough)
- **Investimento:** ~€107K
- **Risparmio training/anno** (assumendo 50 operatori × 4gg risparmiati × €300/gg): **€60K/anno**
- **Risparmio service/anno** (meno trasferte, risoluzione remota): **€30-50K/anno**
- **Payback:** **~12-18 mesi**
- **Break-even allineato a EasyRock Year 3** (2027 chatbot launch)

---

## 🎯 PRODUCT POSITIONING & MARKET

### Target Market
| Segmento | Cliente Pilota | Potenziale |
|---|---|---|
| **Primary** | Heineken (~170 plant, 340 linee) | High — già pilota EasyRock |
| **Secondary** | AB InBev, Coca-Cola, Pepsi, Craft breweries | Medium — diversificazione rischio |
| **Terziario** | FMCG packaging automation | Medium — stesso dominio |

### Competitive Landscape
| Competitor | Prodotto | Gap vs Glass Assist AI |
|---|---|---|
| **MSK Covertech** | Unwrapper rigido, ~700-800 unità | No AI, no chatbot, no adaptive |
| **Atlanta Stretch (Sipario)** | Hot cutting | Emissioni, no AI |
| **Glassform.ai (Partner)** | AI platform vetro | **Non è chatbot** — noi siamo *interface layer* |

### Unique Value Proposition (da EasyRock 2030 Vision)
> **"Infinite Adaptability, Zero-Friction Intelligence"**
1. **Self-adapting** — Qualsiasi pallet/film/contenuto (via Glassform.ai)
2. **Conversational** — Controllo linguaggio naturale ("Ask EASY")
3. **Zero-emission** — Taglio meccanico (legacy EasyRock)
4. **Predictive** — Zero-touch maintenance (via Invert feature)
5. **Human-augmented** — Collaborativo, non sostituivo

### Chatbot Specific Differentiators
- **Domain-specific**: Addestrato su doc Bottero (IS, HTH, Stacker, Swabbing Robot, Invert)
- **Multi-system integration**: HTH, SCMU300, ELP400, Stacker, SPV400, SMC700
- **Action-oriented**: Non solo Q&A — *trigger azioni* (reset allarmi, avvio procedure, AR guidance)
- **Role-based UI**: Specialist/Operator/Manager views (già in Invert GUI)

---

## 🗺️ PRODUCT ROADMAP (Derivato da Gantt + EasyRock)

| Fase | Timeline | Milestone | Deliverable | Success Criteria |
|---|---|---|---|---|
| **MVP1 - Foundation** | Apr-Mag 2026 | Kickoff 22/04 | Dataset validato, HW in lab | 213h dataset prep completate |
| **MVP1 - Core** | Mag-Lug 2026 | HW supply 10/07 | Chatbot base + integrazione HTH/SCMU/Stacker | Demo lab R&D funzionante |
| **MVP2 - Field Validation** | Lug-Set 2026 | Deployment 13/07 | Chatbot in area AT customer | Triage workflow validato, 519h testing |
| **Product Hardening** | Set 2026 | Positioning 11/09 | Prodotto finale, doc completa | Ready per Glasstec |
| **Launch** | Ott 2026 | **Glasstec 19-23/10** | Demo live, lead generation | ≥10 qualified leads |
| **Post-Launch** | 2027+ | EasyRock Integration | EASY Assistant v1.0 | Voice + AR + Predictive |

### Dipendenze Critiche
1. **Glassform.ai** — Core AI/ML non sviluppato da noi (interfaccia only)
2. **HW Supply** — Server/switch lead time 40gg (rischio fornitura)
3. **Dataset Quality** — Documenti Bottero + Q&A ricorrenti + technical questions
4. **Customer Access** — Heineken pilot site per MVP2 validation

---

## ⚠️ RISK REGISTER (Chatbot Specifico)

| ID | Rischio | Probabilità | Impatto | Mitigazione |
|---|---|---|---|---|
| CHAT-01 | **Glassform.ai API instabile/ritardo** | Alta | Critico | Contract SLA, mock layer per sviluppo parallelo |
| CHAT-02 | **Dataset insufficiente/qualità bassa** | Media | Alto | Interviews champions (44.2), curated Q&A da service |
| CHAT-03 | **HW delivery >40gg** | Media | Alto | Ordine anticipato, fallback cloud (AWS/Azure) |
| CHAT-04 | **Heineken pilot non disponibile per MVP2** | Media | Critico | Backup: lab R&D simulation + altro customer (AB InBev?) |
| CHAT-05 | **Integrazione PLC legacy (SPV400, SMC700) complessa** | Alta | Medio | ApiExample.c# già esiste, usare come base |
| CHAT-06 | **Glasstec deadline mancata** | Bassa | Critico | Hard deadline — scope reduction per MVP2 se necessario |
| CHAT-07 | **Adozione operatori bassa (resistenza al cambiamento)** | Media | Medio | Voice-first UX, training 1 giorno, gamification |
| CHAT-08 | **Security/Compliance (GDPR, IEC 62443)** | Media | Alto | AI Network segregata, NAT/FW, data residency EU |

---

## 📋 REQUISITI CHIAVE (Estratti da Documenti)

### Funzionali (Must Have - MVP1)
- [ ] Natural language query understanding (IT/EN)
- [ ] Knowledge base: manuali Bottero, allarmi, procedure, troubleshooting HTH/SCMU/ELP400/Stacker/Swabbing Robot/Invert
- [ ] Integrazione Glassform.ai per allarmi/eventi real-time
- [ ] Interfaccia chat web (Field UI + Control Room UI)
- [ ] Role-based access (Operator / Specialist / Manager)
- [ ] Logging conversazioni per continuous learning

### Funzionali (Should Have - MVP2)
- [ ] **Action execution**: Reset allarme, avvio procedura guidata, parametrizzazione
- [ ] **AR guidance integration** (overlay su smart glasses/tablet)
- [ ] **Predictive alerts** da Invert feature (corrente/posizione)
- [ ] Multi-language (DE, FR, ES per mercato EU)
- [ ] Offline mode (cached knowledge base)

### Funzionali (Nice to Have - Post Launch)
- [ ] Voice-first (speech-to-text + text-to-speech)
- [ ] Training/certification tracking operatori
- [ ] Fleet learning (condivisione anonima pattern cross-plant)
- [ ] Integration con MES/ERP per ticketing automatico

### Non-Funzionali
| Requisito | Target |
|---|---|
| Response time (query semplice) | <2 secondi |
| Response time (query complessa + action) | <5 secondi |
| Uptime | 99.5% (escl. manutenzione pianificata) |
| Data residency | EU (GDPR) |
| Security | IEC 62443 SL2 (allineato EasyRock) |
| Concurrent users | 50+ per plant |
| Scalabilità | 340 linee (Heineken cluster) |

---

## 🔧 TECHNICAL ARCHITECTURE DECISIONS

### Stack Tecnologico (Inferito)
| Layer | Tecnologia | Note |
|---|---|---|
| **Frontend** | Web GUI (React/Vue?) | Field UI + Control Room UI |
| **Backend** | C# / .NET (ApiExample.c#) | Integrazione PLC nativa |
| **AI/ML** | Glassform.ai API + RAG locale | Non sviluppiamo modelli |
| **Inference** | ONNX Runtime / Triton? | Su SERVER 1 (AI Network) |
| **Communication** | REST/gRPC + Modbus TCP | AI Network segregata |
| **Auth** | Role-based (Specialist/Operator) | Già in Invert GUI |
| **Deployment** | On-prem (server cliente) + edge | No cloud dependency per inference |

### Integrazioni PLC/Controller
| Sistema | Protocollo | Dati Scambiati |
|---|---|---|
| **HTH / SCMU300** | Profinet/Ethernet | Allarmi, stati, parametri processo |
| **ELP400** | Profinet | Livello olio, temperatura, allarmi |
| **Stacker** | Profinet | Posizione, allarmi, diagnostica |
| **Swabbing Robot (SPV400)** | Profinet + AI Network | Traiettorie, errori posizione, corrente |
| **Invert (SMC700)** | Profinet + AI Network | Corrente, posizione, warning impatto |
| **Glassform.ai** | HTTPS/API | Modelli ML, predizioni, feature store |

---

## 📊 METRICHE DI SUCCESSO (KPI)

| Categoria | KPI | Target MVP1 | Target MVP2 | Target Launch |
|---|---|---|---|---|
| **Usage** | Daily active users (per plant) | 5 | 15 | 30+ |
| **Usage** | Query/utente/giorno | 3 | 8 | 15 |
| **Quality** | Resolution rate (no escalation) | 60% | 75% | 85% |
| **Quality** | Avg resolution time | 10 min | 5 min | 2 min |
| **Adoption** | Operatori certificati chatbot | 0% | 50% | 80% |
| **Technical** | API latency p95 | <500ms | <300ms | <200ms |
| **Technical** | Uptime | 99% | 99.5% | 99.9% |
| **Business** | Service call reduction | 10% | 30% | 50% |
| **Business** | Training time reduction | 20% | 50% | 85% |

---

## 🎯 NEXT STEPS PER PRODUCT MANAGER

### Immediato (Settimana 1-2)
1. **Finalizzare dataset** — Completare interviste champions (task 44.2), curare Q&A da service reports
2. **Ordinare HW** — Server + switch (lead time 40gg, task 44.5)
3. **Definire Use Cases MVP1** — Workshop 4-8 Mag (task 44.3), prioritizzare top 20 scenari
4. **SLA Glassform.ai** — Formalizzare contratto API, SLA, data sharing agreement

### Breve Termine (Mese 1-2)
5. **Sprint 1: Core RAG** — Indexing documenti, retrieval + generation baseline
6. **Sprint 2: PLC Integration** — ApiExample.c# → connettori HTH/SCMU/Stacker/SPV400/SMC700
7. **Sprint 3: UI/UX** — Field UI (tablet) + Control Room UI (desktop), role-based
8. **Security Review** — IEC 62443 gap analysis, penetration test planning

### Medio Termine (Mese 3-4)
9. **MVP1 Lab Validation** — Demo interna R&D, feedback loop
10. **MVP2 Field Prep** — Configurazione sito Heineken, training super-user
11. **Glasstec Demo Prep** — Script demo 10min, backup offline mode, swag

---

## 📎 ALLEGATI DA RICHIEDERE / VERIFICARE

- [ ] `MOD_PS~2.DOC` — Convertire e leggere (specifica prodotto standard Bottero)
- [ ] `Bottero_GlassAssist_Workflow_Flowchart.pptx` — Estrarre contenuto reale
- [ ] `ApiExample.c#.txt` — Leggere codice completo
- [ ] Verificare se `Glassform.ai` ha API doc / SDK / sandbox
- [ ] Confermare budget approvato (€107K) vs eventuali variazioni
- [ ] Identificare *champions* per interviste (nom, contatti)
- [ ] Definire *Definition of Done* per ogni task Gantt

---

## 💡 NOTE STRATEGICHE PER FUTURE ANALISI

1. **Il chatbot NON è un prodotto standalone** — È *interface layer* per Glassform.ai + ecosystem Bottero. Posizionamento: **"Intelligent Operator Assistant per linea vetro cavo"**

2. **Heineken è single point of failure** — 340 linee potenziali ma *un solo cliente pilota*. Roadmap deve includere **diversificazione precoce** (AB InBev, Coca-Cola) entro MVP2.

3. **Glasstec 2026 è hard deadline** — Tutto il progetto ruota attorno a questo evento. Scope MVP2 *deve* essere tagliabile per garantire demo credibile.

4. **Invert feature è "killer app" per chatbot** — Diagnosticare collisioni maschio/braccio via corrente+posizione è *tangible value* immediato. Priorizzare integrazione.

5. **Voice + AR = Differenziazione 2027** — EasyRock doc cita "Training 1 settimana → 1 giorno". Questo è il *north star* per post-launch.

6. **Architettura AI Network segregata** — Già progettata (drawio). Implementarla *correttamente* da giorno 1 evita refactoring security successivo.

7. **Costo Glassform.ai ESCLUSO** — Chiarire *chi paga cosa*. Se Bottero paga licenza Glassform.ai per cliente, modifica unit economics.

---

*Documento generato automaticamente da analisi Google Drive. Aggiornare man mano che emergono nuove info.*
*Per aggiornamenti: rieseguire analisi su cartelle modificate.*