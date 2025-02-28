import tkinter as tk
from tkinter import ttk, messagebox
from packet_generator.generator import generera_pcap
from replay.aterspelning import aterspela_pcap
import threading


class PaketTestarGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pakettestare för Switch % Routrar")
        self.root.geometry("400x500")

        # Sektion för paketgenerering
        tk.Label(root, text="Generera PCAP").pack(pady=5)
        tk.Label(root, text="Antal paket:").pack()
        self.antal_paket = tk.Entry(root)
        self.antal_paket.insert(0, "100000")
        self.antal_paket.pack()

        tk.Label(root, text="Utdatafil:").pack()
        self.utfil = tk.Entry(root)
        self.utfil.insert(0, "test_trafik.pcap")
        self.utfil.pack()

        tk.Button(root, text="Generera", command=self.starta_generering).pack(pady=5)

        # Sektion för återspelning
        tk.Label(root, text="Återspela PCAP").pack(pady=5)
        tk.Label(root, text="Gränssnitt:").pack()
        self.granssnitt = tk.Entry(root)
        self.granssnitt.insert(0, "eth0")
        self.granssnitt.pack()

        tk.Label(root, text="PCAP-fil:").pack()
        self.aterspelningsfil = tk.Entry(root)
        self.aterspelningsfil.insert(0, "test_trafik.pcap")
        self.aterspelningsfil.pack()

        tk.Label(root, text="Hastighet:").pack()
        self.hastighet = ttk.Combobox(root, values=["normal", "max", "mbps"])
        self.hastighet.set("normal")
        self.hastighet.pack()

        tk.Label(root, text="Loopar:").pack()
        self.loopar = tk.Entry(root)
        self.loopar.insert(0, "1")
        self.loopar.pack()

        tk.Button(root, text="Återspela", command=self.starta_aterspelning).pack(pady=5)

        # Statusfält
        self.status = tk.Label(root, text="Klar", wraplength=350)
        self.status.pack(pady=10)

    def starta_generering(self):
        def kor():
            try:
                antal = int(self.antal_paket.get())
                fil = self.utfil.get()
                self.status.config(text="Genererar...")
                resultat = generera_pcap(antal, fil)
                self.status.config(text=resultat)
            except Exception as e:
                messagebox.showerror("Fel", str(e))

        threading.Thread(target=kor, daemon=True).start()

    def starta_aterspelning(self):
        def kor():
            try:
                iface = self.granssnitt.get()
                fil = self.aterspelningsfil.get()
                hast = self.hastighet.get()
                loop = int(self.loopar.get())
                self.status.config(text="Återspelar...")
                resultat = aterspela_pcap(iface, fil, hast, loop)
                self.status.config(text=resultat)
            except Exception as e:
                messagebox.showerror("Fel", str(e))

        threading.Thread(target=kor, daemon=True).start()


def starta_gui():
    root = tk.Tk()
    app = PaketTestarGUI(root)
    root.mainloop()