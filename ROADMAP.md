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

## v0.0.2 — ECAPA Feasibility

- [ ] Installare una combinazione compatibile di PyTorch, torchaudio e SpeechBrain.
- [ ] Scaricare in modo controllato `speechbrain/spkrec-ecapa-voxceleb`.
- [ ] Registrare la revisione esatta del modello.
- [ ] Convertire audio mono al formato richiesto: 16 kHz.
- [ ] Estrarre un embedding ECAPA di 192 valori finiti.
- [ ] Verificare ripetibilità sullo stesso file.
- [ ] Confrontare stessa voce e voce differente tramite similarità coseno.
- [ ] Misurare tempo e memoria su CPU.
- [ ] Ripetere l'avvio senza rete usando la cache locale.
- [ ] Provare precocemente un pacchetto PyInstaller `onedir`.

## v0.0.3 — Core headless

- [ ] Moduli audio e signal indipendenti dalla UI.
- [ ] Importazione WAV e resampling.
- [ ] Controlli qualità versionati.
- [ ] Enrollment, aggregazione e completezza `completeness-v1`.
- [ ] Formato di progetto versionato.
- [ ] Esportazione con manifest e checksum.
- [ ] Verifica con soglia esterna all'impronta.

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
