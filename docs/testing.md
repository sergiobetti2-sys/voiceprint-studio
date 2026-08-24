# Strategia di test

## Livelli

- `tests/unit`: funzioni pure e casi deterministici.
- `tests/integration`: collaborazione fra moduli e formati su disco temporanei.
- `tests/hardware`: controlli manuali o marcati che richiedono un microfono.
- `tests/fixtures/synthetic`: eventuali segnali generati e autorizzati.

## Checkpoint v0.0.1

Test automatici:

- silenzio al floor di -120 dBFS;
- ampiezza 1 a 0 dBFS;
- ampiezza 0,5 a circa -6,02 dBFS;
- RMS di una sinusoide full-scale a circa -3,01 dBFS;
- clipping rilevato dalla soglia 0,999;
- tono a 1 kHz rilevato entro un bin FFT;
- sample rate non valido rifiutato.

Test hardware verificato il 24 agosto 2026:

- microfono USB Trust GXT234 YUNIX;
- acquisizione mono a 44.100 Hz per 20,07 secondi;
- 0 overflow e 0 drop;
- WAV riproducibile, chiaro e senza interruzioni;
- RMS complessivo -22,14 dBFS;
- picco -0,14 dBFS, correttamente classificato come rischio eccessivo;
- interfaccia, timer, colori e spettro reattivi.

I valori hardware documentano un singolo ambiente e non costituiscono garanzia
per ogni dispositivo Windows.
