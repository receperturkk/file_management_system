"""
Tüm mikroservisleri ve gateway'i başlatmak için yardımcı script
"""
import subprocess
import sys
import time
import os


def start_service(script_name: str, service_name: str):
    """Bir servisi başlat"""
    try:
        print(f"🚀 {service_name} başlatılıyor...")
        # Windows'ta yeni pencere açmak için
        if sys.platform == 'win32':
            subprocess.Popen(
                [sys.executable, script_name],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            # Linux/Mac için
            subprocess.Popen(
                [sys.executable, script_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        time.sleep(1)  # Servislerin başlaması için bekle
        print(f"✅ {service_name} başlatıldı")
    except Exception as e:
        print(f"❌ {service_name} başlatılamadı: {e}")


def main():
    """Tüm servisleri başlat"""
    print("=" * 70)
    print("🔧 MİKROSERVİS MİMARİSİ - TÜM SERVİSLERİ BAŞLAT")
    print("=" * 70)
    print()
    
    # Mikroservisleri başlat
    services = [
        ('server.py', 'Mikroservis 1 (data) - Port 8080'),
        ('server-2.py', 'Mikroservis 2 (data-2) - Port 8081'),
        ('server-3.py', 'Mikroservis 3 (data-3) - Port 8082'),
        ('server-4.py', 'Mikroservis 4 (data-4) - Port 8083'),
    ]
    
    for script, name in services:
        if os.path.exists(script):
            start_service(script, name)
        else:
            print(f"⚠️  {script} bulunamadı, atlanıyor...")
    
    # Gateway'i başlat
    print("\n" + "-" * 70)
    print("🌐 API Gateway başlatılıyor...")
    print("-" * 70)
    
    if os.path.exists('gateway.py'):
        start_service('gateway.py', 'API Gateway - Port 8000')
    else:
        print("❌ gateway.py bulunamadı!")
        return
    
    print("\n" + "=" * 70)
    print("✅ Tüm servisler başlatıldı!")
    print("=" * 70)
    print("\n📝 Gateway'e erişim:")
    print("   http://127.0.0.1:8000/data")
    print("   http://127.0.0.1:8000/data-2")
    print("   http://127.0.0.1:8000/data-3")
    print("   http://127.0.0.1:8000/data-4")
    print("\n⚠️  Servisleri durdurmak için her pencerede Ctrl+C yapın")
    print("=" * 70)


if __name__ == "__main__":
    main()

