# Voiceprint Studio

Voiceprint Studio è un'applicazione desktop per Windows destinata alla creazione,
verifica, conservazione ed esportazione di impronte vocali riutilizzabili in
progetti differenti.

Il prodotto è progettato per lavorare localmente e, dopo il download iniziale
del modello, anche offline. Il repository non contiene e non dovrà contenere
registrazioni o impronte vocali reali.

> [!WARNING]
> Voiceprint Studio è un progetto sperimentale. La verifica vocale non costituisce
> autenticazione ad alta sicurezza e la versione 0.1.0 non includerà protezione
> anti-spoofing o anti-voice-cloning.

## Stato del progetto

Versione corrente: **0.0.1 — Audio Diagnostics PoC**.

Il primo proof of concept ha validato su Windows:

- acquisizione mono da microfono USB a 44,1 kHz;
- timer e interfaccia reattiva per 20 secondi;
- RMS e picco in dBFS;
- indicatore blu, verde e rosso;
- spettro in tempo reale da 0 a 8 kHz;
- salvataggio WAV nella cartella temporanea del sistema;
- 0 overflow e 0 drop nel test hardware;
- sei test automatici per dBFS, clipping e FFT a 1 kHz.

L'interfaccia completa del prodotto non è ancora in sviluppo. Il prossimo
checkpoint è la fattibilità ECAPA (`v0.0.2`).

## Obiettivo della versione 0.1.0

- creazione di un progetto di enrollment;
- registrazione da microfono o importazione WAV;
- frasi guidate in italiano, inglese e spagnolo;
- analisi della qualità e completezza da 0 a 100%;
- revisione, ascolto, eliminazione e ripetizione dei campioni;
- embedding ECAPA aggregato;
- verifica tramite nuova frase;
- salvataggio e riapertura del progetto;
- esportazione `.npy`, `.pt`, `.json` e `manifest.json`;
- scelta separata sulla conservazione e sull'esportazione degli audio originali.

## Requisiti per il PoC

- Windows 10 o 11;
- Python 3.11;
- microfono compatibile con Windows.

## Installazione per sviluppo

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.lock
```

## Avvio del PoC

```bat
python poc\audio_diagnostics.py
```

Le registrazioni diagnostiche vengono salvate in
`%TEMP%\VoiceprintStudioPoC`, fuori dal repository.

## Controlli di qualità

```bat
python -m ruff check .
python -m pytest -v
```

## Documentazione

- [Roadmap](ROADMAP.md)
- [Decisioni tecniche](DECISIONS.md)
- [Architettura](docs/architecture.md)
- [Formato dell'impronta](docs/voiceprint-format.md)
- [Privacy](docs/privacy.md)
- [Strategia di test](docs/testing.md)

## Licenza

Codice distribuito secondo Apache License 2.0. Le dipendenze e i modelli
mantengono le rispettive licenze; vedere [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
