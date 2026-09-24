Documento di Specifiche: Data Quality & Reconciliation Engine

1. Obiettivo del Progetto
Sviluppare una pipeline ETL (Extract, Transform, Load) semplificata che simuli l'acquisizione di un flusso di transazioni finanziarie giornaliere. Il sistema dovrà applicare regole di Data Quality (DQ) per filtrare i record anomali, storicizzare i dati in un database relazionale e fornire una dashboard per il monitoraggio operativo e di business.

2. Architettura di Sistema (Tech Stack)
Sorgente Dati (Extract): File .csv grezzi (simulazione di un dump di un sistema bancario o e-commerce).

Motore di Elaborazione (Transform): Script in Python (libreria Pandas).

Storage (Load): Database Relazionale (PostgreSQL o SQLite per facilità di deployment nel portfolio).

Presentazione (Data Viz): Dashboard interattiva sviluppata in Streamlit (Python) o PowerBI.

3. Specifiche del Modello Dati (Input)
Il flusso in ingresso prevederà un file CSV con i seguenti campi (Tracciato Record):

transaction_id (Stringa/UUID): Identificativo univoco della transazione.

date (Date/Timestamp): Data e ora della transazione.

account_id (Stringa): Identificativo del conto del cliente.

amount (Float): Importo della transazione.

currency (Stringa): Valuta (es. EUR, USD).

type (Stringa): Tipo di operazione (IN, OUT, TRANSFER).

4. Specifiche Funzionali: Regole di Data Quality (Business Rules)
Il cuore del progetto. Il motore in Python dovrà leggere il CSV e applicare i seguenti controlli su ogni riga:

Regola di Completezza: I campi transaction_id, date, e amount non devono essere Null o vuoti.

Regola di Validità Temporale: La date non può essere nel futuro rispetto alla data di esecuzione del processo.

Regola di Validità Logica: Il campo amount non può essere negativo (i deflussi sono indicati dal campo type = 'OUT', l'importo deve restare in valore assoluto).

Regola di Dominio: Il campo currency deve appartenere a un dizionario accettato (solo 'EUR' o 'USD').

5. Progettazione del Database (Logica Relazionale)
Il sistema dovrà alimentare automaticamente due tabelle separate:

Tabella valid_transactions: Conterrà solo i record che hanno superato TUTTI i controlli di Data Quality. Servirà per le analisi di business.

Tabella dq_error_log: Conterrà i record scartati, con l'aggiunta di una colonna error_reason che descrive quale regola ha fallito (es. "Importo negativo" o "Valuta sconosciuta").

6. Flusso di Esecuzione (Il Processo ETL)
Il programma Python si avvia e legge il file CSV dalla cartella input_data/.

Viene eseguita una funzione di validazione che smista le righe (Dataframe Filtering).

Il programma si connette al Database (tramite libreria SQLAlchemy).

Esegue gli INSERT massivi (batch) per popolare le tabelle valid_transactions e dq_error_log.

Sposta il file CSV originale in una cartella processed_data/ (best practice aziendale per non rielaborare gli stessi dati).

7. Deliverables: Specifiche della Dashboard
La dashboard finale dovrà avere due "Pagine" o "Viste" distinte:

Vista Business (Executive):

KPI: Totale transato (in Euro), Numero totale di transazioni valide.

Grafico: Andamento temporale (Time series) degli importi validi per giorno.

Vista IT / Compliance (Monitoraggio Data Quality):

KPI: Percentuale di scarto (es. "Il 4.5% dei record in ingresso oggi era anomalo").

Tabella: Ultime 50 righe dalla tabella dq_error_log per ispezionare gli errori.

Grafico a torta: Distribuzione delle cause di errore (es. 60% Importo Negativo, 40% Data Futura).