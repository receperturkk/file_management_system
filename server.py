import http.server  # Python'un yerleşik HTTP sunucu modülü
import os  # İşletim sistemi ile ilgili dosya/dizin işlemleri için
import mimetypes  # İçerik türlerini (MIME types) yönetmek için
import socket  # IP adresi tespiti için
import json  # JSON işlemleri için
import urllib.parse  # URL parse işlemleri için
import time  # İstek süresi ölçümü için
from pathlib import Path  # Path işlemleri için
from view import render_index_html  # Dinamik HTML oluşturmak için
from modal import BASE_ROOT, get_current_path_from_url, is_safe_path, rename_file_or_folder, delete_file_or_folder  # URL işlemleri için


PORT = 8080  # Sunucunun dinleyeceği port numarası


class CustomRequestHandler(http.server.SimpleHTTPRequestHandler):  # İstekleri işlemek için özel handler sınıfı
    def __init__(self, *args, **kwargs):  # Handler kurucu metodu
        super().__init__(*args, directory=os.getcwd(), **kwargs)  # Mevcut çalışma dizininden dosyaları servis edecek şekilde yapılandır

    def log_message(self, format: str, *args) -> None:  # Her HTTP isteği için log formatını belirler
        print(f"{self.client_address[0]} - - [{self.log_date_time_string()}] " + (format % args))  # IP, zaman damgası ve mesajı stdout'a yaz

    def do_GET(self):  # GET isteklerini işler
        start_time = time.perf_counter()
        try:
            if self.path == '/' or self.path == '/index.html':  # Ana sayfa isteği
                try:
                    print(f"Ana sayfa isteği: {self.path} - {self.client_address[0]}")
                    # Dinamik HTML oluştur
                    html_content = render_index_html()
                    
                    # HTTP yanıtı gönder
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                    self.send_header('Pragma', 'no-cache')
                    self.send_header('Expires', '0')
                    self.end_headers()
                    self.wfile.write(html_content.encode('utf-8'))
                    
                except Exception as e:
                    print(f"Ana sayfa oluşturulurken hata: {e}")
                    # Hata durumunda 500 hatası gönder
                    self.send_error(500, "Internal Server Error")
            elif self.path.startswith('/') and not self.path.startswith(f'/{BASE_ROOT}'):  # Klasör navigasyonu
                try:
                    print(f"Klasör isteği: {self.path} - {self.client_address[0]}")
                    # URL path'inden gerçek dosya yolunu al
                    current_path = get_current_path_from_url(self.path)
                    
                    # Güvenlik kontrolü
                    if not is_safe_path(BASE_ROOT, current_path):
                        self.send_error(403, "Forbidden")
                        return
                    
                    # Dinamik HTML oluştur
                    html_content = render_index_html(current_path)
                    
                    # HTTP yanıtı gönder
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                    self.send_header('Pragma', 'no-cache')
                    self.send_header('Expires', '0')
                    self.end_headers()
                    self.wfile.write(html_content.encode('utf-8'))
                    
                except Exception as e:
                    print(f"Klasör sayfası oluşturulurken hata: {e}")
                    # Hata durumunda 500 hatası gönder
                    self.send_error(500, "Internal Server Error")
            elif self.path.startswith('/api/download/'):  # Download endpoint
                try:
                    # Download path'ini al
                    download_path = self.path.replace('/api/download/', '')
                    download_path = urllib.parse.unquote(download_path)
                    
                    # Path'i kök klasör ile birleştir
                    if download_path.startswith(f'{BASE_ROOT}/'):
                        file_path = Path(download_path)
                    else:
                        file_path = Path(BASE_ROOT) / download_path
                    
                    # Güvenlik kontrolü
                    if not is_safe_path(BASE_ROOT, str(file_path.resolve())):
                        self.send_error(403, "Güvenlik hatası")
                        return
                    
                    if not file_path.exists() or file_path.is_dir():
                        self.send_error(404, "Dosya bulunamadı")
                        return
                    
                    # Dosyayı gönder
                    self.send_response(200)
                    
                    # MIME type'ı belirle
                    mime_type, _ = mimetypes.guess_type(str(file_path))
                    if not mime_type:
                        mime_type = 'application/octet-stream'
                    
                    self.send_header('Content-type', mime_type)
                    self.send_header('Content-Disposition', f'attachment; filename="{file_path.name}"')
                    self.end_headers()
                    
                    # Dosyayı oku ve gönder
                    with open(file_path, 'rb') as f:
                        self.wfile.write(f.read())
                    
                except Exception as e:
                    print(f"Download hatası: {e}")
                    self.send_error(500, "Download hatası")
            else:
                # Diğer dosyalar için normal davranış
                super().do_GET()
        finally:
            duration_ms = (time.perf_counter() - start_time) * 1000
            print(f"GET {self.client_address[0]} {self.path} -> {duration_ms:.1f} ms")
    
    def do_POST(self):  # POST isteklerini işler (Rename için)
        start_time = time.perf_counter()
        try:
            if self.path.startswith('/api/rename'):
                try:
                    # İstek gövdesini oku
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    data = json.loads(post_data.decode('utf-8'))
                    
                    old_path = data.get('path', '')
                    new_name = data.get('new_name', '')
                    
                    if not old_path or not new_name:
                        self.send_error(400, "Eksik parametreler")
                        return
                    
                    # Path'i decode et
                    old_path = urllib.parse.unquote(old_path)
                    
                    # Güvenlik kontrolü
                    full_path = get_current_path_from_url(old_path) if not old_path.startswith(BASE_ROOT) else old_path
                    if not is_safe_path(BASE_ROOT, full_path):
                        self.send_error(403, "Güvenlik hatası")
                        return
                    
                    # Yeniden adlandır
                    result = rename_file_or_folder(full_path, new_name)
                    
                    # JSON yanıt gönder
                    self.send_response(200 if result['success'] else 400)
                    self.send_header('Content-type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
                    
                except Exception as e:
                    print(f"Rename hatası: {e}")
                    self.send_error(500, "Rename hatası")
            else:
                self.send_error(404, "Endpoint bulunamadı")
        finally:
            duration_ms = (time.perf_counter() - start_time) * 1000
            print(f"POST {self.client_address[0]} {self.path} -> {duration_ms:.1f} ms")
    
    def do_DELETE(self):  # DELETE isteklerini işler
        start_time = time.perf_counter()
        try:
            if self.path.startswith('/api/delete'):
                try:
                    # Query parametrelerini al
                    parsed_path = urllib.parse.urlparse(self.path)
                    query_params = urllib.parse.parse_qs(parsed_path.query)
                    
                    file_path = query_params.get('path', [None])[0]
                    
                    if not file_path:
                        self.send_error(400, "Eksik parametre")
                        return
                    
                    # Path'i decode et
                    file_path = urllib.parse.unquote(file_path)
                    
                    # Güvenlik kontrolü
                    full_path = get_current_path_from_url(file_path) if not file_path.startswith(BASE_ROOT) else file_path
                    if not is_safe_path(BASE_ROOT, full_path):
                        self.send_error(403, "Güvenlik hatası")
                        return
                    
                    # Sil
                    result = delete_file_or_folder(full_path)
                    
                    # JSON yanıt gönder
                    self.send_response(200 if result['success'] else 400)
                    self.send_header('Content-type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
                    
                except Exception as e:
                    print(f"Delete hatası: {e}")
                    self.send_error(500, "Delete hatası")
            else:
                self.send_error(404, "Endpoint bulunamadı")
        finally:
            duration_ms = (time.perf_counter() - start_time) * 1000
            print(f"DELETE {self.client_address[0]} {self.path} -> {duration_ms:.1f} ms")


def get_local_ips() -> list[str]:  # Yerel IP adreslerini getirir
    """Bilgisayarın tüm yerel IP adreslerini döndürür"""
    ips = []
    try:
        # localhost ekle
        ips.append("127.0.0.1")
        
        # Ana hostname'in IP adreslerini al
        hostname = socket.gethostname()
        host_info = socket.gethostbyname_ex(hostname)
        
        # Tüm IP adreslerini ekle (localhost hariç)
        for ip in host_info[2]:
            if ip not in ips and not ip.startswith("127."):
                ips.append(ip)
        
        # UDP socket ile gerçek yerel IP'yi bul (alternatif yöntem)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))  # Google DNS'ye bağlanmadan sadece yerel IP öğrenmek için
            local_ip = s.getsockname()[0]
            s.close()
            if local_ip not in ips:
                ips.append(local_ip)
        except Exception:
            pass
            
    except Exception as e:
        print(f"IP adresi tespiti sırasında hata: {e}")
    
    return ips


def main() -> None:  # Uygulama giriş noktası
    mimetypes.add_type('image/svg+xml', '.svg')  # SVG dosyaları için doğru MIME türünü ekle

    script_dir = os.path.dirname(os.path.abspath(__file__))  # Bu dosyanın bulunduğu dizini al
    os.chdir(script_dir)  # Çalışma dizinini script dizinine değiştir

    with http.server.ThreadingHTTPServer(('0.0.0.0', PORT), CustomRequestHandler) as httpd:  # Çoklu isteği aynı anda işlemek için Threading tabanlı HTTP sunucu
        # Yerel IP adreslerini al
        local_ips = get_local_ips()
        
        print("=" * 60)
        print(f"Sunucu başlatıldı! Port: {PORT}")
        print("-" * 60)
        print("Erişim adresleri:")
        print(f"  • Localhost: http://127.0.0.1:{PORT}")
        for ip in local_ips:
            if ip != "127.0.0.1":
                print(f"  • Ağ erişimi: http://{ip}:{PORT}")
        print("-" * 60)
        print("UYARI: Bu sunucu tüm ağ arayüzlerinde (0.0.0.0) dinliyor.")
        print("       Güvenlik riski olabilir!")
        print("=" * 60)
        try:
            httpd.serve_forever()  # Sunucuyu kesintisiz çalıştır
        except KeyboardInterrupt:
            pass  # Ctrl+C ile kesildiğinde hatayı bastır
        finally:
            httpd.server_close()  # Sunucu kapatılırken temiz şekilde soketi kapat


if __name__ == "__main__":  # Dosya doğrudan çalıştırıldığında
    main()  # Ana fonksiyonu başlat


