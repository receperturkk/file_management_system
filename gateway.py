"""
API Gateway - Mikroservis Mimarisi
Bu gateway, tek bir porttan tüm mikroservislere erişim sağlar.
"""
import http.server
import urllib.request
import urllib.parse
import json
import socket
import time
from typing import Dict, Tuple


# Gateway portu
GATEWAY_PORT = 8000

# Mikroservis yapılandırması (Service Registry)
MICROSERVICES: Dict[str, Tuple[str, int]] = {
    'data': ('127.0.0.1', 8080),
    'data-2': ('127.0.0.1', 8081),
    'data-3': ('127.0.0.1', 8082),
    'data-4': ('127.0.0.1', 8083),
}


class GatewayRequestHandler(http.server.BaseHTTPRequestHandler):
    """API Gateway Request Handler - İstekleri mikroservislere yönlendirir"""
    
    def log_message(self, format: str, *args) -> None:
        """Log formatını özelleştir"""
        print(f"[GATEWAY] {self.client_address[0]} - - [{self.log_date_time_string()}] " + (format % args))
    
    def _route_request(self, path: str) -> Tuple[str, int, str]:
        """
        İstek path'ini analiz eder ve hedef mikroservisi belirler
        
        Returns:
            (host, port, new_path): Hedef mikroservis bilgileri
        """
        # Path'i temizle
        path = path.strip('/')
        
        # Ana sayfa veya boş path
        if not path or path == 'index.html':
            # Varsayılan olarak data servisine yönlendir
            return MICROSERVICES['data'][0], MICROSERVICES['data'][1], '/'
        
        # Path'i parçala
        parts = path.split('/', 1)
        service_name = parts[0]
        
        # Mikroservis bulunamazsa varsayılan servise yönlendir
        if service_name not in MICROSERVICES:
            print(f"[GATEWAY] Bilinmeyen servis: {service_name}, varsayılan servise yönlendiriliyor")
            return MICROSERVICES['data'][0], MICROSERVICES['data'][1], f'/{path}'
        
        # Mikroservis bilgilerini al
        host, port = MICROSERVICES[service_name]
        
        # Yeni path'i oluştur (servis adını kaldır)
        if len(parts) > 1:
            new_path = f'/{parts[1]}'
        else:
            new_path = '/'
        
        return host, port, new_path
    
    def _proxy_request(self, method: str, host: str, port: int, path: str, 
                      headers: dict = None, body: bytes = None) -> Tuple[int, dict, bytes]:
        """
        İsteği hedef mikroservise proxy eder
        
        Returns:
            (status_code, response_headers, response_body)
        """
        try:
            # URL oluştur
            url = f'http://{host}:{port}{path}'
            
            # Query string varsa ekle
            if '?' in self.path:
                query = self.path.split('?', 1)[1]
                url += f'?{query}'
            
            print(f"[GATEWAY] Proxying {method} {url}")
            
            # Request oluştur
            req = urllib.request.Request(url, data=body, method=method)
            
            # Header'ları kopyala (bazı önemli olanları)
            if headers:
                for key, value in headers.items():
                    # Host header'ını değiştirme, diğerlerini kopyala
                    if key.lower() not in ['host', 'connection', 'content-length']:
                        req.add_header(key, value)
            
            # İsteği gönder
            with urllib.request.urlopen(req, timeout=10) as response:
                status_code = response.getcode()
                response_headers = dict(response.headers)
                response_body = response.read()
                
                return status_code, response_headers, response_body
                
        except urllib.error.HTTPError as e:
            # HTTP hataları
            status_code = e.code
            response_headers = dict(e.headers) if e.headers else {}
            try:
                response_body = e.read()
            except:
                response_body = e.reason.encode('utf-8') if e.reason else b''
            return status_code, response_headers, response_body
            
        except Exception as e:
            # Diğer hatalar
            print(f"[GATEWAY] Proxy hatası: {e}")
            error_msg = json.dumps({
                'error': 'Service Unavailable',
                'message': f'Mikroservis erişilemiyor: {host}:{port}',
                'details': str(e)
            }, ensure_ascii=False).encode('utf-8')
            return 503, {'Content-Type': 'application/json; charset=utf-8'}, error_msg
    
    def do_GET(self):
        """GET isteklerini işle"""
        start_time = time.perf_counter()
        try:
            # İsteği route et
            host, port, new_path = self._route_request(self.path)
            
            # Header'ları al
            headers = dict(self.headers)
            
            # İsteği proxy et
            status_code, response_headers, response_body = self._proxy_request(
                'GET', host, port, new_path, headers
            )
            
            # Yanıtı gönder
            self.send_response(status_code)
            for key, value in response_headers.items():
                # Bazı header'ları filtrele
                if key.lower() not in ['connection', 'transfer-encoding']:
                    self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response_body)
            
        except Exception as e:
            print(f"[GATEWAY] GET hatası: {e}")
            self.send_error(500, f"Gateway Error: {str(e)}")
        finally:
            duration_ms = (time.perf_counter() - start_time) * 1000
            print(f"[GATEWAY] GET {self.path} -> {duration_ms:.1f} ms")
    
    def do_POST(self):
        """POST isteklerini işle"""
        start_time = time.perf_counter()
        try:
            # İsteği route et
            host, port, new_path = self._route_request(self.path)
            
            # Body'yi oku
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None
            
            # Header'ları al
            headers = dict(self.headers)
            
            # İsteği proxy et
            status_code, response_headers, response_body = self._proxy_request(
                'POST', host, port, new_path, headers, body
            )
            
            # Yanıtı gönder
            self.send_response(status_code)
            for key, value in response_headers.items():
                if key.lower() not in ['connection', 'transfer-encoding']:
                    self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response_body)
            
        except Exception as e:
            print(f"[GATEWAY] POST hatası: {e}")
            self.send_error(500, f"Gateway Error: {str(e)}")
        finally:
            duration_ms = (time.perf_counter() - start_time) * 1000
            print(f"[GATEWAY] POST {self.path} -> {duration_ms:.1f} ms")
    
    def do_DELETE(self):
        """DELETE isteklerini işle"""
        start_time = time.perf_counter()
        try:
            # İsteği route et
            host, port, new_path = self._route_request(self.path)
            
            # Header'ları al
            headers = dict(self.headers)
            
            # İsteği proxy et
            status_code, response_headers, response_body = self._proxy_request(
                'DELETE', host, port, new_path, headers
            )
            
            # Yanıtı gönder
            self.send_response(status_code)
            for key, value in response_headers.items():
                if key.lower() not in ['connection', 'transfer-encoding']:
                    self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response_body)
            
        except Exception as e:
            print(f"[GATEWAY] DELETE hatası: {e}")
            self.send_error(500, f"Gateway Error: {str(e)}")
        finally:
            duration_ms = (time.perf_counter() - start_time) * 1000
            print(f"[GATEWAY] DELETE {self.path} -> {duration_ms:.1f} ms")
    
    def do_OPTIONS(self):
        """CORS preflight isteklerini işle"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


def get_local_ips() -> list[str]:
    """Yerel IP adreslerini getirir"""
    ips = []
    try:
        ips.append("127.0.0.1")
        hostname = socket.gethostname()
        host_info = socket.gethostbyname_ex(hostname)
        for ip in host_info[2]:
            if ip not in ips and not ip.startswith("127."):
                ips.append(ip)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            if local_ip not in ips:
                ips.append(local_ip)
        except Exception:
            pass
    except Exception as e:
        print(f"IP adresi tespiti sırasında hata: {e}")
    return ips


def main():
    """API Gateway'i başlat"""
    print("=" * 70)
    print("🚀 API GATEWAY - Mikroservis Mimarisi")
    print("=" * 70)
    print(f"\n📍 Gateway Port: {GATEWAY_PORT}")
    print("\n📡 Kayıtlı Mikroservisler:")
    for service_name, (host, port) in MICROSERVICES.items():
        print(f"   • /{service_name} -> http://{host}:{port}")
    print("\n" + "-" * 70)
    
    # Yerel IP adreslerini al
    local_ips = get_local_ips()
    
    print("🌐 Erişim Adresleri:")
    print(f"   • Localhost: http://127.0.0.1:{GATEWAY_PORT}")
    for ip in local_ips:
        if ip != "127.0.0.1":
            print(f"   • Ağ: http://{ip}:{GATEWAY_PORT}")
    print("\n📝 Örnek Kullanım:")
    print(f"   • http://127.0.0.1:{GATEWAY_PORT}/data")
    print(f"   • http://127.0.0.1:{GATEWAY_PORT}/data-2")
    print(f"   • http://127.0.0.1:{GATEWAY_PORT}/data-3")
    print(f"   • http://127.0.0.1:{GATEWAY_PORT}/data-4")
    print("-" * 70)
    print("⚠️  UYARI: Tüm mikroservislerin çalışır durumda olduğundan emin olun!")
    print("=" * 70 + "\n")
    
    # Gateway sunucusunu başlat
    with http.server.ThreadingHTTPServer(('0.0.0.0', GATEWAY_PORT), GatewayRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n[GATEWAY] Gateway kapatılıyor...")
        finally:
            httpd.server_close()


if __name__ == "__main__":
    main()

