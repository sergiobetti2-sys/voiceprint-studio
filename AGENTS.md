# AGENTS.md

## Ambito

Questo repository riguarda esclusivamente Voiceprint Studio, applicazione desktop
autonoma per creare, verificare, salvare ed esportare impronte vocali. Non creare
dipendenze da EVA o da altri progetti personali.

## Regole inderogabili sulla privacy

- Non aggiungere mai al repository registrazioni vocali reali, embedding reali,
  dati biometrici, nomi di persone, credenziali, cache o pesi dei modelli.
- Per i test pubblici usare soltanto segnali generati matematicamente o audio
  sintetico espressamente autorizzato.
- I file audio diagnostici devono essere scritti nella cartella temporanea del
  sistema operativo, mai nel repository.
- Prima di ogni commit controllare `git status` e verificare i file non tracciati.

## Architettura

Mantenere separati interfaccia, acquisizione audio, analisi del segnale, controllo
qualità, embedding, enrollment, verifica, salvataggio ed esportazione. La UI non
deve contenere logica biometrica. Il progetto di enrollment e l'esportazione
dell'impronta sono artefatti distinti.

## Qualità e test

- Supporto iniziale: Python 3.11 su Windows 10/11.
- Formattazione e lint: Ruff.
- Test: pytest.
- Il callback audio deve soltanto trasferire campioni verso un buffer o una coda.
- Non dichiarare superato un test senza averne verificato l'output.
- Non introdurre nuove dipendenze senza documentare motivazione, impatto sul
  packaging, licenza e alternative considerate in `DECISIONS.md`.

## Documentazione e versioni

Aggiornare quando necessario `README.md`, `ROADMAP.md`, `DECISIONS.md` e
`CHANGELOG.md`. Usare versionamento semantico e checkpoint verificabili. Il
formato di progetto e il formato di esportazione devono essere aperti,
documentati e versionati.

## Collaborazione con Sergio

Spiegare le decisioni in italiano e in modo comprensibile anche a chi non è
sviluppatore. Quando Sergio deve operare sul proprio PC, fornire un solo comando
o una sola azione alla volta e attendere l'output prima di procedere.
