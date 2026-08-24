# Decisioni architetturali

Le decisioni sono numerate e non vengono riscritte retroattivamente. Un cambio
futuro aggiungerà una nuova decisione che sostituisce esplicitamente la precedente.

## ADR-001 — Prodotto autonomo

**Decisione:** Voiceprint Studio è indipendente da EVA. Concetti già sperimentati
possono essere reimplementati, ma non importati come dipendenze progettuali.

## ADR-002 — Python 3.11 iniziale

**Decisione:** sviluppo e test iniziali usano Python 3.11. Riduce il rischio di
incompatibilità fra GUI, stack audio e librerie ML rispetto a versioni Python più
recenti non ancora supportate uniformemente.

## ADR-003 — PySide6 per il desktop

**Decisione:** PySide6 è il toolkit GUI. La logica audio e biometrica resta fuori
dai widget per consentire test indipendenti e future modifiche dell'interfaccia.

## ADR-004 — Acquisizione al sample rate nativo

**Decisione:** il microfono viene acquisito al proprio sample rate nativo. Il
resampling a 16 kHz avviene successivamente e fuori dal callback audio.

## ADR-005 — ECAPA come primo backend

**Decisione:** il primo backend da validare è
`speechbrain/spkrec-ecapa-voxceleb`. Modello e revisione esatta saranno scritti nel
manifest. L'efficacia su italiano e spagnolo deve essere testata, non presunta.

## ADR-006 — Progetto ed esportazione distinti

**Decisione:** il progetto di enrollment è modificabile e riapribile;
l'esportazione è uno snapshot finale interoperabile. Le due strutture hanno schema
e ciclo di vita separati.

## ADR-007 — Soglia non incorporata

**Decisione:** l'impronta non contiene una soglia definitiva di verifica. La
soglia appartiene al sistema che usa l'impronta e può essere calibrata per il suo
contesto.

## ADR-008 — Completezza versionata

**Decisione:** la percentuale indica completezza dell'enrollment, non certezza
biometrica. La formula sarà identificata da una versione, inizialmente
`completeness-v1`.

## ADR-009 — Privacy del repository

**Decisione:** nessun audio reale, embedding reale, progetto utente, cache o peso
del modello viene versionato. I test pubblici usano segnali matematici o audio
sintetico autorizzato.

## ADR-010 — Packaging `onedir`

**Decisione:** PyInstaller verrà provato presto in modalità `onedir`, più semplice
da diagnosticare rispetto a `onefile`. Il modello resterà esterno all'eseguibile.

## ADR-011 — Apache License 2.0

**Decisione:** il codice del progetto usa Apache License 2.0. Le licenze delle
dipendenze e del modello restano separate e saranno documentate prima della release.

## ADR-012 — Audio diagnostico temporaneo

**Decisione:** il PoC salva il WAV in `%TEMP%\VoiceprintStudioPoC`, mai nella
cartella Git. Questo riduce il rischio di pubblicazione accidentale di voce reale.
