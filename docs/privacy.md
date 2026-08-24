# Privacy e dati biometrici

Una registrazione vocale e un embedding possono essere dati biometrici o
personali a seconda del contesto e dell'uso. Voiceprint Studio deve applicare
minimizzazione, trasparenza e controllo locale dei dati.

## Regole del repository pubblico

- Nessuna voce reale o impronta reale.
- Nessun progetto di enrollment o esportazione utente.
- Nessuna cache o peso del modello.
- Nessuna credenziale o configurazione personale.
- Fixture soltanto sintetiche o espressamente autorizzate.
- Controllo manuale di `git status` prima di ogni commit.

## Regole del prodotto

La conservazione degli audio nel progetto e la loro inclusione nell'esportazione
sono due scelte indipendenti. L'interfaccia deve spiegare le conseguenze della
cancellazione degli originali. La `v0.1.0` opererà localmente ma non promette
cifratura del progetto, anti-spoofing o autenticazione ad alta sicurezza.

Il PoC scrive il WAV reale esclusivamente nella cartella temporanea del sistema.
L'utente deve poterlo eliminare con gli strumenti del sistema operativo.
