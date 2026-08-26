# Architettura

Voiceprint Studio adotta una struttura modulare. I PoC `v0.0.1` e `v0.0.2` sono
volutamente isolati in `poc/`; i moduli definitivi cresceranno sotto
`src/voiceprint_studio/`.

## Moduli previsti

| Modulo | Responsabilità |
|---|---|
| `app` | Coordinamento dei casi d'uso e dei worker |
| `audio` | Dispositivi, acquisizione, riproduzione e importazione |
| `signal` | dBFS, FFT, resampling, mono e qualità |
| `embedding` | Interfaccia backend e implementazione ECAPA |
| `enrollment` | Campioni, aggregazione e completezza |
| `verification` | Similarità e risultato della verifica |
| `storage` | Salvataggio, riapertura e migrazioni |
| `export` | Formati portabili, manifest e checksum |
| `ui` | Finestre e componenti grafici privi di logica biometrica |
| `resources` | Frasi guidate e configurazioni linguistiche |

## Vincoli del tempo reale

Il callback audio non esegue FFT, scrittura su disco, inferenza o operazioni
bloccanti. Copia i campioni in una coda limitata. Il thread dell'interfaccia
consuma la coda a intervalli regolari; elaborazioni più pesanti useranno worker
separati.

## Flusso previsto

1. Acquisizione o importazione audio.
2. Normalizzazione del formato e controllo qualità.
3. Estrazione di un embedding per campione accettato.
4. Aggregazione e normalizzazione L2.
5. Salvataggio del progetto modificabile oppure esportazione di uno snapshot.
6. Verifica con una frase nuova e soglia definita dall'applicazione chiamante.

## Backend ECAPA validato

Il PoC `v0.0.2` implementa il percorso tecnico:

1. lettura del file audio come `float32`;
2. downmix mono quando necessario;
3. resampling polifase a 16 kHz;
4. estrazione ECAPA su CPU;
5. verifica di 192 valori finiti;
6. normalizzazione L2;
7. confronto tramite similarità coseno limitata a `[-1, 1]`.

Il modello e la revisione sono dichiarati nel codice. I pesi vivono nella
cartella dati locale dell'utente e non nel repository o nel pacchetto Windows.
Le future soglie di decisione saranno configurazione del modulo `verification`,
non proprietà dell'embedding esportato.
