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

## ADR-013 — Modello fissato e autonomo da EVA

**Decisione:** il backend usa `speechbrain/spkrec-ecapa-voxceleb` alla revisione
`0f99f2d0ebe89ac095bcc5903c4dd8f72b367286`. Il download è gestito tramite
Hugging Face Hub e i file necessari vengono copiati in
`%LOCALAPPDATA%\VoiceprintStudio\models`, fuori dal repository. Voiceprint Studio
non legge modelli, profili o embedding appartenenti a EVA.

**Motivazione:** una revisione immutabile rende gli esperimenti riproducibili. La
copia evita i privilegi richiesti dai collegamenti simbolici su Windows e rende
il prodotto indipendente da altri progetti. Il modello resta esterno anche nel
pacchetto PyInstaller.

## ADR-014 — Dipendenze del PoC ECAPA

**Decisione:** il PoC introduce PyTorch, torchaudio, SpeechBrain e Hugging Face
Hub per l'inferenza; SoundFile per la lettura robusta degli audio; psutil per la
misura diagnostica della memoria; PyInstaller come strumento di sviluppo.

**Impatto:** lo stack ML aumenta sensibilmente download, ambiente virtuale e
pacchetto Windows. Il primo `onedir` verificato misura circa 498 MiB; la riduzione
è rimandata a una fase di ottimizzazione, dopo aver preservato la correttezza.
psutil e PyInstaller non fanno parte della logica biometrica.

**Alternative considerate:** SciPy da solo copre bene il WAV PCM ma non tutti i
formati supportati da libsndfile; ONNX potrebbe ridurre il runtime futuro, ma
aggiungerebbe ora un secondo percorso d'inferenza non ancora validato. Le licenze
dirette e l'eccezione di distribuzione PyInstaller sono inventariate in
`THIRD_PARTY_NOTICES.md`.

## ADR-015 — Similarità non percentuale

**Decisione:** il confronto restituisce una similarità coseno nell'intervallo
`[-1, 1]`, limitata numericamente per evitare valori appena superiori a 1 dovuti
all'arrotondamento `float32`. Lo score non viene mostrato come probabilità o
percentuale di riconoscimento.

**Motivazione:** trasformare direttamente lo score in percentuale sarebbe
fuorviante. La decisione stessa voce/voce differente richiede una soglia calibrata
su dati rappresentativi e tale soglia resta esterna all'impronta.

## ADR-016 — Sviluppo proprietario dalla v0.0.3

**Decisione:** la `v0.0.2` rimane il proof of concept pubblico distribuito con
Apache License 2.0. Dalla `v0.0.3`, il codice del prodotto viene sviluppato in un
repository privato e con licenza proprietaria. Il repository pubblico resta una
vetrina tecnica e può ricevere documentazione, avanzamento generale, immagini e
dimostrazioni, ma non il nuovo codice sorgente proprietario.

**Motivazione:** il progetto deve essere visibile come portfolio e come possibile
prodotto commerciale, senza concedere automaticamente a terzi l'uso gratuito del
nuovo lavoro. La separazione fra vetrina pubblica e sviluppo privato evita
ambiguità e mantiene verificabile la storia tecnica già pubblicata.

**Impatto:** i diritti già concessi sulla `v0.0.2` non vengono revocati. Prima di
distribuire eseguibili o concedere licenze commerciali saranno verificati i
termini delle dipendenze, del modello, del runtime e la disciplina privacy delle
impronte vocali. Il modello commerciale definitivo ed eventuali condizioni d'uso
saranno decisi prima della prima distribuzione a terzi.

**Sostituisce parzialmente:** ADR-011 per il codice sviluppato dopo la `v0.0.2`.
ADR-011 continua ad applicarsi alla versione pubblica `v0.0.2`.

## ADR-017 — Backend di speaker embedding intercambiabile

**Decisione:** il core dipende da un contratto `SpeakerEmbeddingBackend`, non
direttamente da SpeechBrain o da ECAPA. Preprocessing, estrazione, aggregazione,
similarità e decisione di verifica rimangono responsabilità separate. ECAPA è il
primo adattatore concreto del contratto.

**Motivazione:** il modello validato nella `v0.0.2` non deve diventare un vincolo
architetturale permanente. L'interfaccia permette test senza caricare il modello,
sostituzioni future del backend e manifest che descrivono esplicitamente quale
implementazione ha prodotto l'impronta.

## ADR-018 — Confine funzionale della prima release

**Decisione:** fino alla `v0.1.0` Voiceprint Studio resta focalizzato su
enrollment e verifica 1:1. Identificazione 1:N, sintesi vocale, voice cloning e
voice conversion non entrano nella roadmap corrente.

**Motivazione:** queste funzioni richiedono modelli, metriche, rischi privacy,
misure anti-abuso e posizionamento di prodotto differenti. Potranno essere
valutate successivamente come moduli o prodotti separati, dopo aver completato e
validato il nucleo di impronta vocale.
