import socket

def get_local_ip():
    # Bağlantı oluşturup IP adresini bul
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Sahte bir bağlantı aç, internet erişimi gerekmez
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
    except Exception as e:
        ip_address = "IP adresi bulunamadı"
    finally:
        s.close()

    return ip_address

# IP adresini al ve ekrana yazdır
ip_address = get_local_ip()
print(f"IP adresiniz: {ip_address}")
