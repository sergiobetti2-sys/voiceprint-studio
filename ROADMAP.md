# Roadmap

La roadmap privilegia checkpoint piccoli, verificabili e reversibili. Le date non
sono promesse di consegna: ogni milestone avanza solo dopo i relativi test.

## v0.0.1 — Audio Diagnostics PoC — completata il 24 agosto 2026

- [x] Enumerazione e selezione del microfono.
- [x] Acquisizione mono `float32` al sample rate nativo.
- [x] Timer, RMS dBFS, picco dBFS e clipping.
- [x] Indicatore blu, verde e rosso.
- [x] Spettro in tempo reale con finestra Hann.
- [x] Arresto automatico a 20 secondi.
- [x] WAV temporaneo fuori dal repository.
- [x] Test hardware: 0 overflow/drop e audio integro.
- [x] Test matematici: 6 test superati, compresa FFT a 1 kHz.
- [x] Ruff senza errori sui file del PoC.

## v0.0.2 — ECAPA Feasibility — completata il 25 agosto 2026

- [x] Combinazione compatibile: PyTorch 2.11, torchaudio 2.11 e SpeechBrain 1.1.
- [x] Installazione controllata di `speechbrain/spkrec-ecapa-voxceleb`.
- [x] Revisione esatta del modello registrata e fissata nel PoC.
- [x] Conversione mono e resampling da 44,1 kHz a 16 kHz.
- [x] Estrazione di embedding ECAPA con 192 valori finiti.
- [x] Ripetibilità deterministica sullo stesso segnale e sullo stesso file.
- [x] Separazione qualitativa fra stessa voce e voce differente.
- [x] Tempo e memoria misurati su CPU.
- [x] Installazione e avvio verificati offline dalla cache locale.
- [x] Pacchetto PyInstaller `onedir` avviato con modello esterno.

## Strategia di sviluppo dalla v0.0.3

La `v0.0.2` resta il proof of concept pubblico distribuito con Apache License
2.0. Il prodotto completo prosegue dalla `v0.0.3` in un repository privato e
con licenza proprietaria. Il repository pubblico rimane una vetrina tecnica:
potrà contenere documentazione, avanzamento generale, immagini e dimostrazioni,
ma non il nuovo codice sorgente proprietario.

## v0.0.3 — Core headless proprietario

### Transizione e protezione del prodotto

- [ ] Creare il repository privato destinato allo sviluppo del prodotto.
- [ ] Importare la baseline tecnica verificata nella `v0.0.2`.
- [ ] Applicare al nuovo sviluppo una licenza proprietaria, distinguendola
      esplicitamente dal PoC `v0.0.2` già distribuito con Apache 2.0.
- [ ] Mantenere nel repository pubblico una roadmap generale senza pubblicare
      il nuovo codice sorgente.
- [ ] Verificare le licenze di dipendenze, modello e runtime prima di qualsiasi
      distribuzione commerciale.

### Core applicativo senza interfaccia grafica

- [ ] Portare la logica stabile fuori da `poc/` nel package di produzione
      `src/voiceprint_studio/`.
- [ ] Organizzare il core in moduli indipendenti per audio, preprocessing,
      qualità, backend embedding, enrollment, progetto, esportazione,
      similarità e decisione di verifica.
- [ ] Definire un'interfaccia `SpeakerEmbeddingBackend` affinché ECAPA sia il
      primo backend intercambiabile e non diventi l'architettura del prodotto.
- [ ] Importare WAV mono o stereo con validazione, conversione mono e
      resampling a 16 kHz.
- [ ] Introdurre controlli qualità versionati per durata utile, livello,
      clipping e utilizzabilità del campione.
- [ ] Gestire una sessione di enrollment con aggiunta, elenco ed eliminazione
      dei campioni.
- [ ] Aggregare gli embedding e normalizzare l'impronta risultante.
- [ ] Calcolare la completezza con la formula versionata `completeness-v1`,
      distinguendola sempre dalla probabilità di riconoscimento.
- [ ] Definire un formato di progetto versionato, salvabile e riapribile.
- [ ] Esportare `.npy`, `.pt`, `.json` e `manifest.json` con checksum SHA-256.
- [ ] Includere nel manifest almeno schema, modello, revisione, dimensione,
      sample rate, preprocessing, normalizzazione, aggregazione e timestamp.
- [ ] Conservare la soglia di verifica fuori dall'impronta esportata.
- [ ] Coprire il core con test deterministici per stereo/mono, sample rate non
      standard, file vuoto o corrotto, NaN/Inf, audio troppo corto, silenzio,
      clipping e incompatibilità di dimensione o versione dell'embedding.
- [ ] Aggiungere alla CI un smoke test del core e un job Windows manuale o di
      milestone per verificare la build PyInstaller senza appesantire ogni push.
- [ ] Mantenere Ruff, pytest e controlli privacy come condizioni obbligatorie.

### Criteri di uscita

- [ ] Un test end-to-end headless importa più WAV, crea un enrollment, salva e
      riapre il progetto senza perdita di dati.
- [ ] L'esportazione produce file coerenti, manifest versionato e checksum
      verificabili.
- [ ] La verifica confronta una nuova registrazione con l'impronta usando una
      soglia fornita dal chiamante.
- [ ] Il backend ECAPA può essere sostituito nei test da un backend fittizio
      senza modificare enrollment, esportazione o verifica.
- [ ] Nessun audio reale, embedding reale, modello o credenziale entra nel
      repository o nei test.

## v0.0.4 — Desktop alpha

- [ ] Flusso guidato minimo PySide6.
- [ ] Italiano, inglese e spagnolo.
- [ ] Registrazione e importazione.
- [ ] Ascolto, ripetizione ed eliminazione dei campioni.
- [ ] Salvataggio e riapertura del progetto.

## v0.1.0-rc.1 — End-to-end candidate

- [ ] Enrollment completo e verifica.
- [ ] Esportazioni `.npy`, `.pt`, `.json` e `manifest.json`.
- [ ] Scelte separate per conservazione ed esportazione degli audio.
- [ ] Migrazioni e gestione degli errori.
- [ ] Test su Windows 10 e 11.

## v0.1.0 — Prima release

- [ ] Eseguibile Windows `onedir` verificato su macchina pulita.
- [ ] Documentazione utente e tecnica completa.
- [ ] CI verde, Ruff e pytest superati.
- [ ] Licenze e avvisi di terze parti verificati.
- [ ] Nessun dato biometrico o modello incluso nel repository o nella release.
