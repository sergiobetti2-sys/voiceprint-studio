# Changelog

Tutte le modifiche rilevanti saranno documentate in questo file. Il formato segue
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) e il progetto usa
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned

- Core headless per importazione WAV, qualità, enrollment ed esportazione.

## [0.0.2] - 2026-08-25

### Added

- PoC da riga di comando per la fattibilità ECAPA.
- Modello `speechbrain/spkrec-ecapa-voxceleb` con revisione fissata.
- Installazione del modello nell'area dati locale, esterna al repository.
- Preprocessing mono e resampling polifase a 16 kHz.
- Embedding da 192 valori, normalizzazione L2 e similarità coseno limitata.
- Confronto fra file e controllo di ripetibilità sullo stesso audio.
- Undici test deterministici per preprocessing, resampling e similarità.
- Misurazione manuale di latenza e memoria su CPU.
- Primo pacchetto sperimentale PyInstaller in modalità `onedir`.

### Security

- Nessun audio reale, embedding, peso o cache del modello incluso nel repository.

## [0.0.1] - 2026-08-24

### Added

- Finestra PySide6 per diagnostica audio.
- Enumerazione e selezione dei dispositivi di ingresso.
- Acquisizione mono al sample rate nativo tramite sounddevice.
- Timer, RMS dBFS, picco dBFS e percentuale di clipping.
- Indicatore cromatico blu, verde e rosso.
- Spettro 0-8 kHz aggiornato in tempo reale.
- Arresto automatico dopo 20 secondi.
- Salvataggio WAV nella cartella temporanea del sistema.
- Sei test deterministici per livelli, clipping e FFT a 1 kHz.
- Documentazione e regole privacy iniziali del repository.
