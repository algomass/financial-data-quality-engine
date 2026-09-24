# Financial Data Quality Engine

Questo è un progetto portfolio di Data Engineering che simula una pipeline completa di acquisizione, pulizia (Data Quality) e visualizzazione di transazioni finanziarie.

## 🚀 Come provare il progetto sul tuo PC (Local Setup)

Non c'è bisogno di alcun hosting o server complesso. Segui questi semplici passaggi per eseguire l'intera pipeline e visualizzare la Dashboard in locale sul tuo computer.

### Prerequisiti
[Python 3.8+](https://www.python.org/downloads/) installato sul tuo computer.

### 1. Clona il repository
Apri il terminale (o Prompt dei Comandi/PowerShell) e clona questo progetto:
```bash
git clone https://github.com/tuo-username/financial-data-quality-engine.git
cd financial-data-quality-engine
```

### 2. Crea un Ambiente Virtuale (Consigliato) ed installa le dipendenze
È sempre buona norma isolare le librerie del progetto:
```bash
# Crea l'ambiente virtuale
python -m venv venv

# Attiva l'ambiente virtuale
# Su Windows:
venv\Scripts\activate
# Su Mac/Linux:
source venv/bin/activate

# Installa le librerie necessarie
pip install -r requirements.txt
```

### 3. Esegui la Pipeline di Data Engineering
Ora puoi eseguire gli step della pipeline in sequenza:

1. **Genera i dati di test (Mock Data):**
   ```bash
   python generate_mock_data.py
   ```
   *Questo creerà un file `transactions_mock.csv` con errori intenzionali.*

2. **Esegui il motore di Data Quality (Filtro Pandas):**
   ```bash
   python dq_engine.py
   ```
   *Questo script validerà le regole e separerà i dati puliti da quelli anomali.*

3. **Carica i dati nel Data Warehouse (SQLite):**
   ```bash
   python database.py
   ```
   *Creerà il database locale `financial_data.db`.*

### 4. Avvia la Dashboard
Per visualizzare i risultati, avvia l'interfaccia Streamlit:
```bash
streamlit run app.py
```
Si aprirà automaticamente una pagina nel tuo browser (solitamente all'indirizzo `http://localhost:8501`) dove potrai esplorare i dati e le metriche di Data Quality.
