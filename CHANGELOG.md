# Changelog

Tutte le modifiche rilevanti saranno documentate in questo file. Il formato segue
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) e il progetto usa
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned

- Proof of concept ECAPA e verifica del funzionamento offline.

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
