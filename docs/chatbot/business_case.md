# BOTTERO CHATBOT - BUSINESS CASE FINANZIARIO & PREVISIONE VOLUMI 2027+
**Basato su:** `chatbot_potential_partners_analysis.md` + stime fatturato gruppi + hit rate 10%  
**Obiettivo:** Calcolo OPEX/CAPEX, ROI 24-36 mesi, piano finanziario pluriennale  
**Data:** 2026-07-07  

---

## 1. ASSUNZIONI CHIAVE & METODOLOGIA

### 1.1 Hit Rate & Conversione
| Parametro | Valore | Fonte/Note |
|-----------|--------|------------|
| **Hit Rate (win rate)** | **10%** | Assunto conservativo su pipeline qualificata |
| **Pipeline Target Primario** | 87 clienti | Da analisi DW (Corporate + Predisposizione) |
| **Pipeline Target Secondario** | 41 clienti | Da analisi DW (Predisposizione, no Corporate) |
| **Conversion Rate Lead → Pilot** | 30% | Industry standard B2B enterprise |
| **Conversion Rate Pilot → Rollout** | 70% | Basato su reference EasyRock/Invert |
| **Avg Time to Close (Pilot)** | 6 mesi | Da Glasstec 2026 → Pilot Q1 2027 |
| **Avg Time Pilot → Rollout** | 12 mesi | Validazione + procurement + deployment |

### 1.2 Modello di Pricing (Per Sito/Anno)
| Componente | Prezzo Listino | Note |
|------------|----------------|------|
| **Licenza Chatbot Base** | € 45.000 / sito / anno | Include: RAG, PLC connectors, Web UI, Role-based access |
| **Modulo Action Execution** | € 15.000 / sito / anno | Reset allarmi, procedure guidate, parametrizzazione |
| **Modulo AR Guidance** | € 20.000 / sito / anno | Overlay smart glasses/tablet, video procedure |
| **Modulo Predictive Alerts** | € 10.000 / sito / anno | Integrazione Invert (corrente/posizione), SPV400 |
| **Supporto & Manutenzione (20%)** | Incluso nel canone | SLA 9/5, aggiornamenti, knowledge base sync |
| **Professional Services (Setup)** | € 35.000 / sito (one-off) | Installazione, configurazione, training, go-live |
| **Hardware Edge (Server + Switch)** | € 18.000 / sito (CAPEX) | Fornitura Bottero, installazione cliente |

**Bundle Consigliato "Full Stack": € 90.000 / sito / anno + € 53.000 one-off**

### 1.3 Struttura Costi Bottero (Per Anno)

#### CAPEX (Una Tantum - Anno 0)
| Voce | Importo | Note |
|------|---------|------|
| **Sviluppo Core (MVP1+MVP2)** | € 410.000 | 7.200h × €57/h (già budgettato) |
| **HW Lab R&D (2 server + switch)** | € 36.000 | Per sviluppo e test interno |
| **Certificazione IEC 62443 SL2** | € 80.000 | Penetration test, audit, documentazione |
| **Integrazione Glassform.ai (API/SLA)** | € 50.000 | Sviluppo connettori, mock layer, test |
| **TOTALE CAPEX INIZIALE** | **€ 576.000** | Già approvato in budget € 107K + integrazioni |

#### OPEX Ricorrenti (Anno 1+)
| Voce | Anno 1 | Anno 2 | Anno 3 | Note |
|------|--------|--------|--------|------|
| **Team Prodotto (3 FTE)** | € 280.000 | € 294.000 | € 308.700 | PM, Lead Dev, ML Engineer (+5%/anno) |
| **Team Delivery (2 FTE)** | € 160.000 | € 240.000 | € 320.000 | Scalabile con # siti (1 FTE/10 siti) |
| **Supporto L2/L3 (1.5 FTE)** | € 120.000 | € 150.000 | € 180.000 | Helpdesk, bug fixing, KB management |
| **Cloud/Inference (GPU)** | € 60.000 | € 90.000 | € 120.000 | On-prem edge + cloud burst, scala con siti |
| **Glassform.ai Licenza (revenue share)** | € 0 | € 45.000 | € 120.000 | 15% revenue con floor € 15K/sito dal 2027 |
| **Marketing & Sales (Events, Demo)** | € 80.000 | € 100.000 | € 120.000 | Glasstec, fiere, ABM, partner enablement |
| **Overhead (15%)** | € 105.000 | € 137.850 | € 172.305 | Facilities, IT, HR, Finance |
| **TOTALE OPEX/ANNO** | **€ 805.000** | **€ 1.056.850** | **€ 1.341.005** | |

---

## 2. STIMA FATTURATO GRUPPI TARGET (Dati Pubblici 2023-2024)

| Gruppo | Fatturato 2023 (M€) | Dipendenti | Siti Produzione | Posizione Mercato | Note |
|--------|---------------------|------------|-----------------|-------------------|------|
| **VERALLIA** | 3.800 | 10.000+ | 60+ | #3 Mondiale | Public (EPA: VRLA) |
| **VERESCENCE** | 1.200 | 3.500 | 15+ | #1 Pharma/Cosmetics | Private (PAI Partners) |
| **VIDRALA** | 1.100 | 4.000 | 10+ | #4 Europa | Public (BME: VID) |
| **STOELZLE** | 650 | 2.500 | 12+ | Leader Pharma/Perfumery | Private (Familiare) |
| **BORMIOLI PHARMA** | 450 | 1.200 | 6 | Leader Pharma packaging | Private (Bormioli Group) |
| **HEINZ GLAS** | 400 | 1.500 | 8 | Pharma/Cosmetics premium | Private |
| **PGP GLASS** | 350 | 2.000 | 8 | India/Sri Lanka/UK | Private (Promoter group) |
| **CINER GLASS** | 1.800 | 5.000 | 12+ | #1 Turchia, #2 Europa | Public (BIST: CINER) |
| **AGI GLASPAC/GREENPAC** | 300 | 1.800 | 5 | Leader India Pharma | Public (NSE: AGI) |
| **NTB (NIHON TAISANBIN)** | 250 | 800 | 4 | Japan precision glass | Private |
| **SGD PHARMA** | 200 | 800 | 4 | France/China/US Pharma | Private (Advent) |
| **BEATSON CLARK** | 180 | 600 | 2 | UK Container glass | Private |
| **IND. VIDRIERA BAJIO** | 150 | 500 | 3 | Mexico LATAM hub | Private |
| **ZIGNIAGO** | 120 | 400 | 3 | Italy premium | Private |
| **GERRESHEIMER** | 1.800 | 11.000 | 40+ | #1 Pharma primary packaging | Public (ETR: GXI) |
| **SCHOTT PHARMA** | 900 | 4.000 | 15+ | Specialty glass pharma | Public (ETR: 1SCH) |

**TOTALE FATTURATO AGGREGATO TOP 15 GRUPPI: ~13,6 MILIARDI €**

---

## 3. PREVISIONE VOLUMI 2027-2030 (Hit Rate 10%)

### 3.1 Funnel di Conversione Annuo

| Anno | Lead Qualificati | Pilot Avviati (30%) | Rollout Confermati (70%) | Siti Cumulativi Attivi |
|------|------------------|---------------------|--------------------------|------------------------|
| **2026** (H2) | 15 (Glasstec) | 0 | 0 | 0 |
| **2027** | 25 | 5 | 0 | 5 (Pilot) |
| **2028** | 35 | 10 | 4 | 14 (4 Rollout + 10 Pilot) |
| **2029** | 40 | 12 | 7 | 33 (11 Rollout + 12 Pilot + 10 esistenti) |
| **2030** | 45 | 14 | 9 | 56 (20 Rollout + 14 Pilot + 22 esistenti) |

*Assunzione: 10% hit rate su 87 target primario = 8-9 deal/anno a regime. Target secondario aggiunge ~3-4 deal/anno.*

### 3.2 Distribuzione per Bundle (Mix Realistico)

| Bundle | % Siti | Prezzo Annuo | Prezzo One-off |
|--------|--------|--------------|----------------|
| **Base** | 20% | € 45.000 | € 35.000 |
| **Base + Action** | 30% | € 60.000 | € 35.000 |
| **Full Stack** | 50% | € 90.000 | € 53.000 |
| **Media Ponderata** | 100% | **€ 73.500** | **€ 44.600** |

### 3.3 Ricavi Proiettati (€ migliaia)

| Anno | Siti Attivi | Ricavi Ricorrenti | Ricavi One-off (Nuovi) | Totale Ricavi | YoY Growth |
|------|-------------|-------------------|------------------------|---------------|------------|
| **2026** | 0 | 0 | 0 | **0** | — |
| **2027** | 5 Pilot | 184 | 223 | **407** | — |
| **2028** | 14 (4 Rollout) | 1.029 | 624 | **1.653** | **+306%** |
| **2029** | 33 (11 Rollout) | 2.426 | 714 | **3.140** | **+90%** |
| **2030** | 56 (20 Rollout) | 4.116 | 846 | **4.962** | **+58%** |
| **2031** | 85 (30 Rollout) | 6.248 | 980 | **7.228** | **+46%** |
| **2032** | 120 (45 Rollout) | 8.820 | 1.120 | **9.940** | **+38%** |

*Nota: Pilot pagano 50% canone anno 1 + full one-off. Rollout = full canone dal mese 7.*

---

## 4. CONTO ECONOMICO PROGETTATO 2026-2030 (€ migliaia)

| Voce | 2026 (H2) | 2027 | 2028 | 2029 | 2030 | **Totale 5 Anni** |
|------|-----------|------|------|------|------|-------------------|
| **RICAVI TOTALI** | 0 | 407 | 1.653 | 3.140 | 4.962 | **10.162** |
| Ricavi Ricorrenti | 0 | 184 | 1.029 | 2.426 | 4.116 | 7.755 |
| Ricavi One-off | 0 | 223 | 624 | 714 | 846 | 2.407 |
| **COSTI TOTALI** | 576 | 1.155 | 1.447 | 1.781 | 2.161 | **7.120** |
| CAPEX Iniziale | 576 | 0 | 0 | 0 | 0 | 576 |
| OPEX Anno | 0 | 805 | 1.057 | 1.341 | 1.611 | 4.814 |
| HW Edge per Sito (CAPEX) | 0 | 90 | 180 | 234 | 288 | 792 |
| Glassform.ai Revenue Share | 0 | 0 | 45 | 120 | 180 | 345 |
| Provisione Rischi (5% ricavi) | 0 | 20 | 83 | 157 | 248 | 508 |
| **EBITDA** | -576 | -748 | +206 | +1.359 | +2.801 | **+3.042** |
| **EBITDA Margin** | — | -184% | +12% | +43% | +56% | **+30%** |
| **CASHFLOW CUMULATIVO** | -576 | -1.324 | -1.118 | +241 | +3.042 | — |

---

## 5. ANALISI ROI & PAYBACK

### 5.1 Break-Even Analysis
| Metrica | Valore | Anno |
|---------|--------|------|
| **Break-even Cumulativo (Cashflow > 0)** | **Maggio 2029** | Anno 3 |
| **Payback Period (da inizio investimento)** | **31 mesi** | Target 24-36 mesi ✓ |
| **ROI a 36 mesi (2029)** | **+22%** | (EBITDA cumulativo / CAPEX+OPEX) |
| **ROI a 48 mesi (2030)** | **+89%** | |
| **ROI a 60 mesi (2031)** | **+198%** | Proiezione estesa |

### 5.2 Sensitività Payback (Mesi)

| Scenario | Hit Rate | Prezzo Medio | OPEX | Payback |
|----------|----------|--------------|------|---------|
| **Base Case** | 10% | € 73.500 | Piano | **31** |
| **Ottimistico** | 15% | € 80.000 | -10% | **22** |
| **Conservativo** | 7% | € 65.000 | +15% | **41** |
| **Solo Target Primario** | 8% | € 75.000 | Piano | **35** |
| **Ritardo Glasstec (6 mesi)** | 10% | € 73.500 | Piano | **36** |

### 5.3 KPI Finanziari Chiave (Steady State 2030+)
| KPI | Target | Note |
|-----|--------|------|
| **ARR (Annual Recurring Revenue)** | € 8,8M | A 2032 |
| **Gross Margin (Ricavi - COGS diretti)** | 78% | Escl. OPEX strutturale |
| **Net Revenue Retention** | 115% | Upsell moduli + espansione siti |
| **CAC Payback** | 14 mesi | Sales + Delivery / Nuovo sito |
| **LTV/CAC** | 5,2x | Lifetime 7 anni, churn <5% |
| **Rule of 40 (Growth + Margin)** | 94% | 58% growth + 36% margin |

---

## 6. PIANO INVESTIMENTI PER FASE (CAPEX FASING)

| Fase | Periodo | Investimento | Motivazione | Funding |
|------|---------|--------------|-------------|---------|
| **Fase 0 - Foundation** | H2 2026 | € 576K | Core dev, certifica, Glassform.ai, HW lab | Budget approvato |
| **Fase 1 - Pilot Enablement** | Q1 2027 | € 180K | 5× HW Edge (€36K), Travel, Training | Cashflow operativo |
| **Fase 2 - Scale Delivery** | Q3 2027 | € 220K | Team Delivery +2 FTE, Automation deploy | Ricavi Pilot |
| **Fase 3 - Platform Hardening** | 2028 | € 300K | Multi-tenancy, Self-service portal, Analytics | Serie A / Cashflow |
| **Fase 4 - International Hubs** | 2029 | € 500K | Entity US/India, Partner program, Localizzazione | Cashflow + Debt |

**TOTALE CAPEX 5 ANNI: € 1,776M** (di cui € 576K already committed)

---

## 7. SCENARI "WHAT-IF" PER DECISIONI STRATEGICHE

### 7.1 Scenario A: Accelerazione via Partnership (es. System Integrator)
| Impatto | Cambio vs Base |
|---------|----------------|
| Hit rate → 15% (channel pull) | Payback: **24 mesi** |
| CAC → -30% (partner led) | ROI 36m: **+45%** |
| Time-to-close → -40% | Break-even: **Gen 2029** |
| Revenue share partner → -20% | Margine netto: -5pp |

**Raccomandazione:** Firmare 2-3 partner strategici (FAMOR, RIT, REVIMAC) entro Q4 2026.

### 7.2 Scenario B: Pricing "Land & Expand" Aggressivo
| Strategia | Impatto |
|-----------|---------|
| Anno 1: € 35K/sito (solo Base) | +50% volume pilot |
| Upsell Action/AR/Pred a 6 mesi | +€ 35K/sito anno 2 |
| Net retention → 130% | ARR 2030: **+25%** |
| Rischio: churn se value non percepito | Mitigazione: Success metrics contrattuali |

### 7.3 Scenario C: Acquisizione Tecnologica (Glassform.ai o competitor)
| Opzione | Costo | Beneficio | Payback Impatto |
|---------|-------|-----------|-----------------|
| Acquisto Glassform.ai | € 5-8M | Controllo IP, margin +15%, no rev-share | +12 mesi payback, poi +€ 1,5M/anno |
| Partnership esclusiva | € 500K | Lock-in roadmap, co-selling | Neutro |
| Build internal ML | € 2M/3 anni | Indipendenza, IP ownership | +18 mesi payback |

---

## 8. RISCHI FINANZIARI & MITIGAZIONI

| Rischio | Probabilità | Impatto Finanziario | Mitigazione | Contingency Budget |
|---------|-------------|---------------------|-------------|-------------------|
| **Glassform.ai API instabile / costi imprevisti** | Alta | +€ 200K/anno / -20% margine | SLA contrattuale, mock layer, clausola price cap | € 150K |
| **Ritardo certificazione IEC 62443** | Media | -6 mesi revenue / +€ 100K | Avvio parallelo, consulente dedicato | € 80K |
| **HW lead time > 6 mesi** | Media | -3 mesi pilot / +€ 50K | Ordine anticipato H2 2026, fallback cloud | € 50K |
| **Adozione operatori < target** | Media | -30% upsell moduli | Champion program, gamification, training 1gg | € 100K |
| **Concorrente lancia chatbot (MSK/Siemens)** | Bassa | -20% win rate / pricing pressure | Differenziazione: PLC native, AR, Invert integration | € 200K (R&D accelerato) |
| **GDPR / Data residency blocca rollout EU** | Bassa | -100% revenue EU | AI Network segregata, EU-only inference, DPA standard | € 50K |

**TOTALE CONTINGENCY BUDGET CONSIGLIATO: € 630K** (da accantonare nel budget 2027)

---

## 9. DASHBOARD ESECUTIVO - KPI DA MONITORARE MENSILMENTE

### 9.1 Leading Indicators (Predictive)
| KPI | Target 2027 | Target 2028 | Frequenza | Owner |
|-----|-------------|-------------|-----------|-------|
| **Qualified Pipeline (€)** | € 5M | € 12M | Mensile | Sales Dir. |
| **Pilot Signed** | 5 | 10 | Mensile | Sales Dir. |
| **Pilot Go-Live** | 3 | 8 | Mensile | Delivery Mgr |
| **Pilot NPS** | > 40 | > 50 | Per pilot | PM |
| **Use Cases Validati/Pilot** | > 15 | > 25 | Per pilot | PM |

### 9.2 Lagging Indicators (Outcome)
| KPI | Target 2027 | Target 2028 | Target 2029 | Frequenza | Owner |
|-----|-------------|-------------|-------------|-----------|-------|
| **ARR** | € 0,2M | € 1,0M | € 2,4M | Mensile | CFO |
| **Cashflow Cumulativo** | -€ 1,3M | -€ 1,1M | +€ 0,2M | Mensile | CFO |
| **Gross Margin** | 45% | 65% | 72% | Trimestrale | CFO |
| **Net Revenue Retention** | — | 110% | 115% | Trimestrale | PM |
| **Churn Rate** | 0% | < 5% | < 5% | Annuale | PM |
| **Avg Deal Size** | € 80K | € 120K | € 150K | Per deal | Sales |

---

## 10. RACCOMANDAZIONI FINALI PER APPROVAZIONE BUDGET

### ✅ **GO DECISION - Punti di Forza**
1. **Payback 31 mesi** dentro target 24-36 mesi
2. **Mercato indirizzabile € 13,6B** fatturato aggregato top 15 gruppi
3. **Tecnologia de-risked**: Architettura validata, Glassform.ai partnership, Invert integration pronta
4. **Barriere all'ingresso**: IEC 62443, PLC native connectors, domain knowledge Bottero
5. **Upsell path chiaro**: Base → Action → AR → Predictive (4× revenue per sito)

### ⚠️ **CONDIZIONI PER GO (Da Chiudere Entro Q3 2026)**
1. **SLA Glassform.ai firmato** con price cap e SLA 99,5%
2. **5 Pilot LOI firmati** (Verescence, Verallia, Stoelzle, Bormioli, Ciner)
3. **Certificazione IEC 62443 avviata** con auditor selezionato
4. **HW ordinato** per 5 pilot + lab (lead time 40gg)
5. **Team Delivery assunto** (2 FTE) per onboarding Gen 2027

### 📋 **MILESTONE FINANZIARIE VINCOLANTI**
| Data | Milestone | Gate Decision |
|------|-----------|---------------|
| **30 Set 2026** | Glasstec Demo + 5 LOI | Go/No-Go Fase 1 |
| **31 Dic 2026** | MVP1 Lab Validato + Certificazione avviata | Budget Release Fase 2 |
| **31 Mar 2027** | 3 Pilot Go-Live + NPS > 40 | Scale Delivery Team |
| **30 Set 2027** | 2 Pilot → Rollout Confirmati | Series A / Debt Facility |
| **31 Dic 2028** | Break-even Cumulativo Raggiunto | Full Investment Committee Review |

---

## ALLEGATO A: DETTAGLIO PREZZI PER GRUPPO (Esempi Preventivo)

| Gruppo | Siti Stimati | Bundle | Anno 1 (Pilot) | Anno 2+ (Rollout) | 3-Year Value |
|--------|--------------|--------|----------------|-------------------|--------------|
| **VERALLIA** | 15 | Full Stack | € 135K (1 pilot) | € 1.35M | € 4,1M |
| **VERESCENCE** | 10 | Full Stack | € 90K (1 pilot) | € 900K | € 2,8M |
| **STOELZLE** | 12 | Full Stack | € 90K (1 pilot) | € 1,08M | € 3,3M |
| **BORMIOLI PHARMA** | 5 | Base+Action | € 60K (1 pilot) | € 300K | € 1,0M |
| **PGP GLASS** | 10 | Full Stack | € 90K (1 pilot) | € 900K | € 2,8M |
| **CINER GLASS** | 5 | Full Stack | € 90K (1 pilot) | € 450K | € 1,4M |
| **HEINZ GLAS** | 6 | Base+Action | € 60K (1 pilot) | € 360K | € 1,2M |
| **NTB** | 4 | Full Stack | € 90K (1 pilot) | € 360K | € 1,1M |

**TOTAL ADDRESSABLE MARKET (Top 8 gruppi, 3 anni): € 17,7M**

---

*Documento preparato per Comitato Investimenti Bottero.  
Assunzioni rivisitabili trimestralmente.  
Prossima revisione: Post-Glasstec Ottobre 2026.*