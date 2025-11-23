# 🥊 PyBoxe

**PyBoxe** è uno strumento web di ricerca avanzata per allenatori e appassionati di pugilato italiano. Permette di cercare pugili nel database ufficiale della [FPI](https://www.fpi.it) (Federazione Pugilistica Italiana) con filtri avanzati e di esportare i risultati direttamente in Excel.

## 🎯 Perché PyBoxe?

Il sito ufficiale della FPI mostra i pugili in pagine di 18 risultati alla volta, costringendo gli utenti a:
- Sfogliare manualmente decine di pagine
- Cliccare su "Mostra dettagli" per ogni singolo atleta
- Non poter filtrare per numero di match

**PyBoxe risolve questi problemi** permettendo agli allenatori di:
- ✅ Filtrare i pugili per **range di match** (es. tra 5 e 15 incontri)
- ✅ Applicare filtri per **comitato regionale**, **qualifica** e **categoria di peso**
- ✅ Ottenere immediatamente un **file Excel** con tutti i dati (nome, età, società, vittorie, sconfitte, pareggi)
- ✅ Risparmiare ore di ricerca manuale

Ideale per trovare rapidamente pugili compatibili con il proprio allievo per organizzare match.

---

## 🚀 Installazione e Utilizzo

### Prerequisiti
- Python 3.10 o superiore
- pip (gestore pacchetti Python)

### 1. Clona la repository
```bash
git clone https://github.com/tuousername/pyboxe.git
cd pyboxe
```

### 2. Installa le dipendenze
```bash
pip install flask requests beautifulsoup4 openpyxl
```

### 3. Avvia il server
```bash
python -m server.server
```

Il server sarà disponibile su: **http://127.0.0.1:5000**

### 4. Utilizza l'interfaccia web
1. Apri il browser e vai su `http://127.0.0.1:5000`
2. Seleziona i filtri desiderati:
   - **Comitato** (opzionale): regione di appartenenza
   - **Qualifica** (obbligatorio): Elite, Youth, ecc.
   - **Peso** (opzionale): categoria di peso specifica
   - **Range match**: numero minimo e massimo di incontri
3. Inserisci il nome del file Excel da generare
4. Clicca su **Scarica 💾**

Il file Excel verrà generato e scaricato automaticamente con tutti i pugili trovati.

---

## 📊 Struttura del Progetto

```
pyboxe/
├── client/                 # Frontend web
│   ├── index.html         # Interfaccia utente
│   ├── scripts/
│   │   └── client.js      # Logica client-side
│   └── styles/
│       └── style.css      # Stili dell'interfaccia
├── server/                # Backend Flask
│   ├── server.py          # Server web e API
│   └── downloads/         # File Excel generati (creata automaticamente)
└── core/                  # Logica di business
    ├── FpiClient.py       # Client HTTP per FPI
    ├── FpiScraper.py      # Parser e ricerca atleti
    ├── FpiAthlete.py      # Modello dati atleta
    └── FpiConverter.py    # Export in Excel
```

---

## 🔧 Tecnologie Utilizzate

### Backend
- **Flask**: web server e routing
- **Requests**: comunicazione HTTP con FPI
- **BeautifulSoup4**: parsing HTML
- **OpenPyXL**: generazione file Excel

### Frontend
- **HTML5/CSS3**: interfaccia utente
- **Vanilla JavaScript**: logica client-side
- **Fetch API**: comunicazione con il backend

---

## 📝 Funzionalità

### Filtri di Ricerca
- **Comitato Regionale**: filtra per regione (es. Emilia-Romagna, Lombardia, ecc.)
- **Qualifica**: Elite, Youth, Schoolboy, ecc.
- **Categoria di Peso**: disponibile dopo aver selezionato la qualifica
- **Range di Match**: cerca pugili con un numero specifico di incontri

### Export Excel
Il file Excel generato contiene:
- Nome completo
- Età
- Società di appartenenza
- Match totali
- Vittorie
- Sconfitte
- Pareggi

---

## ⚡ Note Tecniche

- I file Excel vengono salvati temporaneamente in `server/downloads/`
- Il server mantiene in memoria l'ultimo file generato per il download
- Tutte le richieste al sito FPI sono gestite con sessioni HTTP per prestazioni ottimali
- Gli errori vengono gestiti lato server e comunicati tramite redirect con codici di errore

---

## 🐛 Risoluzione Problemi

### Il server non si avvia
Verifica che la porta 5000 sia libera:
```bash
lsof -i :5000  # Linux/Mac
netstat -ano | findstr :5000  # Windows
```

### "Nessun atleta trovato"
- Verifica che i filtri non siano troppo restrittivi
- Controlla che il sito FPI sia raggiungibile
- Prova ad allargare il range di match

### Errori di download
- Assicurati che la cartella `server/downloads/` sia scrivibile
- Verifica di aver completato una ricerca prima di tentare il download

---

## 📄 Licenza

Questo progetto è rilasciato sotto licenza **GNU GPL v2**. Vedi il file [LICENSE](LICENSE) per maggiori dettagli.

---

## 👨‍💻 Autore

Made by the greatest computer scientist of all time 😎

---

## 🙏 Contributi

Pull request e suggerimenti sono benvenuti! Sentiti libero di aprire una issue per bug o richieste di nuove funzionalità.

---

## ⚠️ Disclaimer

PyBoxe non è affiliato con la Federazione Pugilistica Italiana. È uno strumento indipendente che utilizza dati pubblicamente disponibili sul sito ufficiale FPI per facilitare la ricerca di atleti.