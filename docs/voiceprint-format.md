# Formati Voiceprint Studio

I nomi e gli schemi qui descritti sono proposte iniziali e saranno stabilizzati
nella milestone `v0.0.3`.

## Progetto di enrollment

Cartella modificabile e riapribile:

```text
NomeProgetto.vpsproj/
├── project.json
├── recordings/       # opzionale
├── derived/          # metriche ed embedding intermedi
└── temporary/        # eliminabile, mai esportato
```

Il progetto può essere incompleto. Se l'utente non conserva gli audio, dopo la
riapertura non potrà riascoltare o rielaborare quei campioni; resteranno soltanto
le informazioni esplicitamente previste dallo schema.

## Impronta esportata

Snapshot interoperabile e non modificabile dall'app:

```text
NomeImpronta.voiceprint/
├── manifest.json
├── embedding.npy     # se selezionato
├── embedding.pt      # se selezionato
├── embedding.json    # se selezionato
└── audio/             # solo con consenso esplicito
```

Il manifest includerà almeno versione dello schema e dell'app, ID, data,
modello e revisione, dimensione e tipo dell'embedding, sample rate,
preprocessing, normalizzazione, aggregazione, quantità e durata dei campioni,
lingua, presenza degli audio e checksum SHA-256.

La soglia di verifica non viene salvata nell'impronta.

## Aggregazione iniziale da validare

1. embedding ECAPA per ogni campione accettato;
2. normalizzazione L2 individuale;
3. media aritmetica;
4. normalizzazione L2 finale.
