import subprocess


def aterspela_pcap(granssnitt, pcap_fil, hastighet="normal", loopar=1):
    # Bygg baskommandot med sudo för tcpreplay
    kommando = ["sudo", "tcpreplay", "-i", granssnitt, pcap_fil]

    # Lägg till hastighetsalternativ baserat på användarens val
    if hastighet == "max":
        kommando.append("-t")
    elif hastighet == "mbps":
        kommando.extend(["--mbps", "1000"])
    # För "normal" gör vi inget, eftersom tcpreplay kör på ursprunglig hastighet som standard

    # Lägg till loopar om fler än 1 anges
    if loopar > 1:
        kommando.extend(["--loop", str(loopar)])

    # Logga kommandot för felsökning
    print(f"Kör kommando: {' '.join(kommando)}")

    try:
        # Kör tcpreplay-kommandot och fånga utdata
        resultat = subprocess.run(kommando, capture_output=True, text=True, check=True)
        return f"Återspelning klar: {resultat.stdout}"
    except subprocess.CalledProcessError as e:
        return f"Återspelning misslyckades: {e.stderr}"
    except FileNotFoundError:
        return "Fel: tcpreplay är inte installerat eller hittas inte i PATH."
    except Exception as e:
        return f"Oväntat fel: {str(e)}"