# Lagerstatus-overvåker for Nettbutikker

## 🛒 Introduksjon

Python-skript som automatisk overvåker lagerstatus for spesifikke produkter hos nettbutikker. Ved endringer i lagerstatus sendes det ut en e-postvarsling til angitt adresse. Skriptet benytter `Selenium` for nettskraping og `smtplib` for e-postvarsling.

---

## 🚀 Funksjoner

- 🔍 Overvåker lagerstatus for spesifikke produkter
- 📧 Sender e-postvarsling ved endringer
- 📊 Logger tidligere statuser i en CSV-fil

---

## 📦 Krav

- Python 3.7 eller nyere
- [selenium](https://pypi.org/project/selenium/)
- [webdriver-manager](https://pypi.org/project/webdriver-manager/)
- Google-konto med aktivert [app-passord](https://myaccount.google.com/apppasswords)

---

## ⚙️ Installasjon

Installer moduler:

    pip install selenium webdriver-manager

## 🔧 Konfigurasjon

Produkter defineres i listen produkter:

    {
        "butikk": "Norli",
        "navn": "Secret Hitler (Norli)",
        "url": "https://www.norli.no/...",
        "xpath": "//div[@class='...']"
    }
    
- xpath: peker til HTML-elementet med lagerstatus.
- url: må være en direkte link til produktsiden.
- butikk og navn: brukes kun i e-postvarslingen.

**E-postinnstillinger**

E-post kan sendes til og fra samme adresse.


    mottaker = "example@gmail.com"
    avsender = "example@gmail.com"
    passord = "******"
👉 Opprett app-passord her: https://myaccount.google.com/apppasswords

## 📅 Automatisering
Skriptet kan kjøres automatisk ved hjelp av:

- macOS/Linux: `cron`
- Windows: Oppgaveplanlegger (Task Scheduler)

Eksempel med cron (kjører hver time) med .log-fil:

    0 * * * * /usr/bin/python3 /sti/til/lagerstatus_overvaker.py >> /sti/til/cron.log 2>&1

## ❗ Feilhåndtering 
Scriptet sender en e-post ved første forekomst av feilmelding.

Vanlige årsaker til feil:
- Innhold ikke lastet (f.eks. krever scrolling)
- Endret XPath på nettsiden.
  
**Tips:** Unngå XPath som div[2]/div[1]/.... Bruk klasser ved hjelp av [@class="..."] når mulig.

