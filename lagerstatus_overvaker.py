import csv
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import smtplib
from email.mime.text import MIMEText

# CSV-fil for å lagre tidligere lagerstatuser
CSV_FIL = Path(__file__).parent / "status.csv"

# Liste over produkter som skal overvåkes
produkter = [
    {
        "butikk": "Norli",
        "navn": "Secret Hitler (Norli)",
        "url": "https://www.norli.no/spill-og-puslespill/spill/familiespill/spill-secret-hitler-eng-utgave",
        "xpath": '//div[@class="richText-root-SHY"]/b'
    },
    {
        "butikk": "Ark",
        "navn": "Secret Hitler (Ark)",
        "url": "https://www.ark.no/produkt/secret-hitler-en-711746875073",
        "xpath": '//*[@id="__next"]/div[1]/div[2]/article/div/div/div[2]/div/div[5]/div/div/div[2]/div/p'
    }
]

# E-post innstillinger
mottaker = "example@gmail.com"
avsender = "example@gmail.com"
passord = "******"  # Bruk app-passord (https://myaccount.google.com/apppasswords)


# Konfigurer Chrome i headless-modus (usynlig nettleser)
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--headless")

# Start WebDriver
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), 
    options=chrome_options
)


def les_gamle_statuser():
    """Les tidligere status fra CSV-filen."""
    if not CSV_FIL.exists():
        return {}
    with CSV_FIL.open(newline="", encoding="utf-8") as f:
        return {rad[0]: rad[1] for rad in csv.reader(f)}
    

def skriv_ny_status(status_dict):
    """Lagre nye statuser til CSV-filen."""
    with CSV_FIL.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for nøkkel, status in status_dict.items():
            writer.writerow([nøkkel, status])


def sjekk_lager(url, xpath, butikk):
    """Sjekk lagerstatus ved å hente tekst fra gitt XPath."""
    driver.get(url)
    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element.text
    except Exception as e:
        return f"Feil ved henting ({e})"
    

def send_email(melding, emne):
    """Send e-post med statusendringer."""
   
    msg = MIMEText(melding)
    msg["Subject"] = emne
    msg["From"] = avsender
    msg["To"] = mottaker

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(avsender, passord)
            server.sendmail(avsender, mottaker, msg.as_string())
        print("E-post sendt!")
    except Exception as e:
        print(f"Feil ved sending av e-post: {e}")


# --- Hovedlogikk ---
gamle_statuser = les_gamle_statuser()
nye_statuser = {}
endringer = []

for produkt in produkter:
    status = sjekk_lager(produkt["url"], produkt["xpath"], produkt["butikk"])
    nøkkel = f"{produkt['butikk']}|{produkt['navn']}"
    nye_statuser[nøkkel] = status

    gammel_status = gamle_statuser.get(nøkkel)
    if gammel_status != status:
        endringer.append(
            f"{produkt['navn']} har endret status:\n  Før: {gammel_status or 'Ingen'}\n  Nå: {status}"
        )

# Hvis det er endringer, send e-post og lagre ny status
if endringer:
    endrede_produkter = [
        nøkkel.split("|")[1]
        for nøkkel in nye_statuser
        if gamle_statuser.get(nøkkel) != nye_statuser[nøkkel]
    ]
    emne = "Endring i lagerstatus: " + ", ".join(endrede_produkter)
    send_email("\n\n".join(endringer), emne)
    skriv_ny_status(nye_statuser)
else:
    print("Ingen endringer i lagerstatus.")

# Lukk nettleseren etter kjøring
driver.quit()
