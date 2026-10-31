# Pregătire pentru interviu — Voice Appointment Intake

Roluri țintă: Voice AI / Applied Python.

## Prezentare de 90 de secunde

1. Explică problema concretă și cine folosește rezultatul.
2. Rulează `make demo` sau fluxul din UI.
3. Arată testul pentru un caz de eșec, apoi explică mecanismul din cod.
4. Spune ce limite are demonstrația și ce ai construi pentru producție.

Decizia de explicat: A local Whisper model transcribes audio. A conservative parser extracts unambiguous date/time inputs or requests clarification. Even confirmed intake is not a booking; availability belongs to a separate booking service.

## Cinci întrebări

1. Cum separi ASR de intent extraction?
2. De ce clarifici data?
3. Ce se întâmplă la ambiguitate AM/PM?
4. De ce confirmarea nu rezervă slotul?
5. Cum măsori WER versus succesul taskului?

## Exercițiu înainte de a aplica

Add time-zone selection and a larger consented ASR/date-extraction evaluation set.

Alege o parte mică a acestei modificări, implementeaz-o personal, adaugă un test care verifică comportamentul și descrie rezultatul într-un commit real. Nu declara că ai înțeles sau construit singur o parte pe care nu o poți explica.

## Checklist personal

- [ ] Pot porni proiectul dintr-un checkout curat.
- [ ] Pot urmări cererea până la rezultatul salvat.
- [ ] Pot explica diferența dintre fixture și model local.
- [ ] Pot demonstra un eșec și recuperarea lui.
- [ ] Am făcut o modificare proprie și o pot explica în engleză.

Aceste puncte necesită review-ul tău; nu au fost bifate automat.
