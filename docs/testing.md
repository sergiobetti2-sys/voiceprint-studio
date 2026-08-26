# Strategia di test

## Livelli

- `tests/unit`: funzioni pure e casi deterministici.
- `tests/integration`: collaborazione fra moduli e formati su disco temporanei.
- `tests/hardware`: controlli manuali o marcati che richiedono un microfono.
- `tests/fixtures/synthetic`: eventuali segnali generati e autorizzati.

## Checkpoint v0.0.1

Test automatici:

- silenzio al floor di -120 dBFS;
- ampiezza 1 a 0 dBFS;
- ampiezza 0,5 a circa -6,02 dBFS;
- RMS di una sinusoide full-scale a circa -3,01 dBFS;
- clipping rilevato dalla soglia 0,999;
- tono a 1 kHz rilevato entro un bin FFT;
- sample rate non valido rifiutato.

Test hardware verificato il 24 agosto 2026:

- microfono USB Trust GXT234 YUNIX;
- acquisizione mono a 44.100 Hz per 20,07 secondi;
- 0 overflow e 0 drop;
- WAV riproducibile, chiaro e senza interruzioni;
- RMS complessivo -22,14 dBFS;
- picco -0,14 dBFS, correttamente classificato come rischio eccessivo;
- interfaccia, timer, colori e spettro reattivi.

I valori hardware documentano un singolo ambiente e non costituiscono garanzia
per ogni dispositivo Windows.

## Checkpoint v0.0.2

Test automatici aggiunti:

- mantenimento del mono già a 16 kHz;
- downmix stereo deterministico;
- resampling polifase da 44.100 a 16.000 Hz;
- rifiuto di sample rate non validi e valori non finiti;
- normalizzazione L2 a norma unitaria;
- valori di riferimento della similarità coseno;
- limite numerico della similarità nell'intervallo `[-1, 1]`;
- rifiuto di vettori con dimensioni differenti;
- mapping verificato del file label encoder nella revisione del modello.

Validazione manuale su Windows con Python 3.11:

- PyTorch 2.11 CPU, torchaudio 2.11 e SpeechBrain 1.1 compatibili;
- modello `speechbrain/spkrec-ecapa-voxceleb` fissato alla revisione
  `0f99f2d0ebe89ac095bcc5903c4dd8f72b367286`;
- installazione controllata e successivo avvio offline riusciti;
- embedding da 192 valori finiti con normalizzazione L2 unitaria;
- due estrazioni sullo stesso input identiche;
- file reale mono a 44,1 kHz convertito correttamente a 16 kHz;
- score della stessa voce chiaramente superiore al controllo con voce differente;
- inferenza osservata fra circa 0,03 e 0,13 secondi su CPU;
- memoria residente osservata fino a circa 464 MiB;
- pacchetto PyInstaller `onedir` funzionante con modello esterno;
- pacchetto sperimentale di circa 498 MiB e 2.729 file.

Le registrazioni usate per la prova manuale sono rimaste esclusivamente nella
cartella temporanea del sistema e non fanno parte del repository. Tempi, memoria
e dimensioni documentano un singolo ambiente e devono essere misurati nuovamente
su altre configurazioni.
