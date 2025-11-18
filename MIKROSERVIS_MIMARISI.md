# Mikroservis Mimarisi - Proje Dokümantasyonu

## 📋 Proje Özeti

Bu proje, **mikroservis mimarisinin temel prensiplerini** gösteren bir eğitim projesidir. 4 farklı dosya listeleme servisi, tek bir API Gateway üzerinden erişilebilir hale getirilmiştir.

## 🏗️ Mimari Bileşenler

### 1. API Gateway (`gateway.py`)
- **Port**: 8000
- **Görev**: Tüm mikroservislere tek noktadan erişim sağlar
- **Özellikler**:
  - Path-based routing
  - Request/Response proxying
  - Service discovery
  - Request logging

### 2. Mikroservisler

| Servis | Port | Klasör | Dosya |
|--------|------|--------|-------|
| Data Service | 8080 | `wwwroot/data` | `server.py` |
| Data-2 Service | 8081 | `wwwroot/data-2` | `server-2.py` |
| Data-3 Service | 8082 | `wwwroot/data-3` | `server-3.py` |
| Data-4 Service | 8083 | `wwwroot/data-4` | `server-4.py` |

Her servis:
- Kendi klasörünü listeler
- RESTful API endpoint'leri sunar
- Bağımsız olarak çalışır

## 🚀 Hızlı Başlangıç

### Adım 1: Tüm Servisleri Başlat

```bash
python start_all_services.py
```

Bu script, tüm mikroservisleri ve gateway'i otomatik olarak başlatır.

### Adım 2: Gateway Üzerinden Erişim

Tarayıcınızda şu adreslere gidin:

```
http://127.0.0.1:8000/data      → data klasörü
http://127.0.0.1:8000/data-2    → data-2 klasörü
http://127.0.0.1:8000/data-3    → data-3 klasörü
http://127.0.0.1:8000/data-4    → data-4 klasörü
```

## 📊 Request Flow Örneği

```
1. Client Request:
   GET http://127.0.0.1:8000/data

2. Gateway Processing:
   - Path'i analiz eder: /data
   - Service name: "data"
   - Target: localhost:8080
   - New path: /

3. Proxy Request:
   GET http://localhost:8080/

4. Microservice Response:
   HTML content (file list)

5. Gateway Response:
   HTML content → Client
```

## 🔧 Yapılandırma

### Service Registry

`gateway.py` dosyasında servis kayıt defteri:

```python
MICROSERVICES = {
    'data': ('127.0.0.1', 8080),
    'data-2': ('127.0.0.1', 8081),
    'data-3': ('127.0.0.1', 8082),
    'data-4': ('127.0.0.1', 8083),
}
```

Yeni servis eklemek için bu listeye ekleme yapın.

## 📁 Dosya Yapısı

```
mvc-receperturkk/
├── gateway.py                 # API Gateway
├── start_all_services.py      # Tüm servisleri başlatma scripti
├── server.py                  # Mikroservis 1 (data)
├── server-2.py                # Mikroservis 2 (data-2)
├── server-3.py                # Mikroservis 3 (data-3)
├── server-4.py                # Mikroservis 4 (data-4)
├── modal.py                   # Data servisi model
├── modal_2.py                 # Data-2 servisi model
├── modal_3.py                 # Data-3 servisi model
├── modal_4.py                 # Data-4 servisi model
├── view.py                    # Data servisi view
├── view_2.py                  # Data-2 servisi view
├── view_3.py                  # Data-3 servisi view
├── view_4.py                  # Data-4 servisi view
└── wwwroot/
    ├── data/                  # Mikroservis 1 klasörü
    ├── data-2/                # Mikroservis 2 klasörü
    ├── data-3/                # Mikroservis 3 klasörü
    └── data-4/                # Mikroservis 4 klasörü
```

## 🎯 Mikroservis Mimarisi Prensipleri

### 1. Service Discovery (Servis Keşfi)
Gateway, servis kayıt defterini kullanarak servisleri bulur ve yönlendirir.

### 2. API Gateway Pattern
- Tüm istekler gateway üzerinden geçer
- Cross-cutting concern'ler (logging, routing) gateway'de yönetilir
- Client'lar sadece gateway'i bilir

### 3. Loose Coupling (Gevşek Bağlantı)
- Servisler birbirinden bağımsızdır
- Her servis kendi verisini yönetir
- Servisler arası doğrudan iletişim yok

### 4. Single Responsibility (Tek Sorumluluk)
- Her servis tek bir klasörü yönetir
- Gateway sadece routing yapar
- Her component kendi sorumluluğuna odaklanır

### 5. Independent Deployment (Bağımsız Dağıtım)
- Her servis ayrı ayrı başlatılabilir
- Bir servisin çökmesi diğerlerini etkilemez

## 🔍 API Endpoints

### Gateway Endpoints

Tüm endpoint'ler gateway üzerinden erişilebilir:

```
GET  /data              → Ana sayfa (data servisi)
GET  /data-2            → Ana sayfa (data-2 servisi)
GET  /data-3            → Ana sayfa (data-3 servisi)
GET  /data-4            → Ana sayfa (data-4 servisi)

POST /data/api/rename   → Dosya/klasör yeniden adlandırma
DELETE /data/api/delete → Dosya/klasör silme
GET  /data/api/download → Dosya indirme
```

### Mikroservis Endpoints (Doğrudan Erişim)

Her servise doğrudan da erişilebilir:

```
GET  http://localhost:8080/              → data servisi
POST http://localhost:8080/api/rename    → Rename
DELETE http://localhost:8080/api/delete  → Delete
GET  http://localhost:8080/api/download  → Download
```

## 📝 Log Örnekleri

### Gateway Logları
```
[GATEWAY] 127.0.0.1 - - [2025-01-XX XX:XX:XX] "GET /data HTTP/1.1" 200
[GATEWAY] Proxying GET http://127.0.0.1:8080/
[GATEWAY] GET /data -> 45.2 ms
```

### Mikroservis Logları
```
Ana sayfa isteği: / - 127.0.0.1
GET 127.0.0.1 / -> 12.5 ms
```

## 🧪 Test Senaryoları

### Senaryo 1: Gateway Üzerinden Erişim
1. Gateway'i başlat: `python gateway.py`
2. Tüm mikroservisleri başlat
3. Tarayıcıda `http://127.0.0.1:8000/data` adresine git
4. Dosya listesinin göründüğünü doğrula

### Senaryo 2: Doğrudan Mikroservis Erişimi
1. Sadece `server.py`'yi başlat
2. Tarayıcıda `http://127.0.0.1:8080` adresine git
3. Dosya listesinin göründüğünü doğrula

### Senaryo 3: Servis Çökmesi
1. Tüm servisleri başlat
2. Bir mikroservisi durdur (Ctrl+C)
3. Gateway üzerinden o servise istek at
4. 503 Service Unavailable hatası alındığını doğrula

## 🎓 Öğrenilen Kavramlar

1. **API Gateway Pattern**: Merkezi giriş noktası
2. **Service Discovery**: Servis kayıt defteri
3. **Request Routing**: Path-based routing
4. **Reverse Proxy**: İstekleri başka servislere yönlendirme
5. **Microservices Architecture**: Bağımsız, küçük servisler

## 🚧 Gelecek Geliştirmeler

- [ ] Health Check endpoints
- [ ] Load Balancing
- [ ] Rate Limiting
- [ ] Authentication & Authorization
- [ ] Request/Response Transformation
- [ ] Circuit Breaker Pattern
- [ ] Distributed Tracing
- [ ] Service Mesh (Istio, Linkerd)

## 📚 Kaynaklar

- [Microservices.io](https://microservices.io/)
- [API Gateway Pattern](https://microservices.io/patterns/apigateway.html)
- [Service Discovery](https://microservices.io/patterns/service-registry.html)
- [Martin Fowler - Microservices](https://martinfowler.com/articles/microservices.html)

