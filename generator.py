from scapy.all import Ether, IP, TCP, UDP, ICMP, RandIP, RandMAC, RandShort, wrpcap
import random


def generera_pcap(antal_paket, utfil):
    # Lista för att lagra paketen
    paketlista = []

    # Skapa paket
    for i in range(antal_paket):
        kalla_ip = RandIP()._fix()  # Slumpmässig käll-IP
        mal_ip = RandIP()._fix()  # Slumpmässig mål-IP
        kalla_mac = RandMAC()._fix()  # Slumpmässig käll-MAC
        mal_mac = RandMAC()._fix()  # Slumpmässig mål-MAC

        # Välj protokoll slumpmässigt: TCP (50%), UDP (30%), ICMP (20%)
        protokoll = random.choices(["tcp", "udp", "icmp"], weights=[50, 30, 20], k=1)[0]
        eth = Ether(src=kalla_mac, dst=mal_mac)

        if protokoll == "tcp":
            paket = eth / IP(src=kalla_ip, dst=mal_ip) / TCP(sport=RandShort(), dport=RandShort(), flags="S")
        elif protokoll == "udp":
            paket = eth / IP(src=kalla_ip, dst=mal_ip) / UDP(sport=RandShort(), dport=RandShort())
        else:  # icmp
            paket = eth / IP(src=kalla_ip, dst=mal_ip) / ICMP()

        paketlista.append(paket)

    # Spara paketen till en PCAP-fil
    wrpcap(utfil, paketlista)
    return f"Skapade {antal_paket} paket till {utfil}"