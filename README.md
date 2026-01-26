# Py Code Analyzer (LITE)

CLI alat za analizu Python projekata. LITE verzija fokusirana je na:
- pokretanje statičke analize (Ruff),
- generisanje izveštaja (TXT + JSON),
- opcioni prikaz “kontekst linija” oko problema.

> Napomena: napredne funkcije (npr. AI auto-fix, advanced scoring, GUI) nisu deo LITE verzije.

---

## Šta radi

1) Uzme putanju do projekta/foldera ili fajla  
2) Pokrene **Ruff** i prikupi nalaze (warnings/errors)  
3) Sačuva izveštaje:
- `report.txt` (čitljivo za čoveka)
- `report.json` (strukturisano za automatizaciju)

---

## Instalacija

### 1) Python
Potrebno: Python 3.10+ 

### 2) Ruff
```bash
pip install ruff

Quick test:
python analyzer-lite.py examples/sample_bad.py --out report.txt --json report.json --context 2

## Quickstart

```bash
pip install -r requirements.txt
python analyzer-lite.py examples/sample_bad.py --out report.txt --json report.json --context 2



### B) “LITE vs PRO” mini tabela 

```md
## LITE vs PRO

- LITE: analiza + report (TXT/JSON), opcioni context
- PRO: AI auto-fix, advanced scoring, batch pipeline, audit/backup workflow, GUI (planirano)


