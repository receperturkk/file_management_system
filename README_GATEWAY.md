# API Gateway - Mikroservis Mimarisi

Bu proje, mikroservis mimarisinin temel prensiplerini gösteren bir örnektir.

## 🏗️ Mimari Yapı

```
                    ┌─────────────┐
                    │   Client    │
                    │  (Browser)  │
                    └──────┬──────┘
                           │
                           │ HTTP Request
                           │
                    ┌──────▼──────┐
                    │ API Gateway │
                    │  Port 8000  │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐      ┌──────▼──────┐    ┌─────▼─────┐
   │ Service │      │   Service   │    │  Service  │
   │  Data   │      │   Data-2    │    │  Data-3   │
   │ :8080   │      │   :8081     │    │  :8082    │
   └─────────┘      └─────────────┘    └───────────┘
                           │
                    ┌──────▼──────┐
                    │   Service   │
                    │   Data-4    │
                    │   :8083     │
                    └─────────────┘
```

## 📋 Özellikler

### API Gateway

- **Tek nokta erişim**: Tüm mikroservislere tek bir porttan erişim
- **Request Routing**: Path-based routing ile istekleri doğru servise yönlendirme
- **Service Discovery**: Servis kayıt defteri (Service Registry)
- **Load Balancing**: Gelecekte eklenebilir
- **Request/Response Logging**: Tüm istekler loglanır

### Mikroservisler

- **Bağımsız çalışma**: Her servis kendi portunda çalışır
- **Özel klasör**: Her servis farklı bir klasörü listeler
- **RESTful API**: Standart HTTP metodları (GET, POST, DELETE)

## 🚀 Kullanım

### 1. Tüm Servisleri Başlatma

**Otomatik (Önerilen):**

```bash
python start_all_services.py
```

**Manuel:**

```bash
# Terminal 1
python server.py      # Port 8080 - data

# Terminal 2
python server-2.py    # Port 8081 - data-2

# Terminal 3
python server-3.py    # Port 8082 - data-3

# Terminal 4
python server-4.py    # Port 8083 - data-4

# Terminal 5
python gateway.py     # Port 8000 - Gateway
```

### 2. Gateway Üzerinden Erişim

Gateway üzerinden tüm servislere erişebilirsiniz:

```
http://127.0.0.1:8000/data      → Mikroservis 1 (data)
http://127.0.0.1:8000/data-2    → Mikroservis 2 (data-2)
http://127.0.0.1:8000/data-3    → Mikroservis 3 (data-3)
http://127.0.0.1:8000/data-4    → Mikroservis 4 (data-4)
```

### 3. Doğrudan Mikroservis Erişimi

Her servise doğrudan da erişebilirsiniz:

```
http://127.0.0.1:8080    → data
http://127.0.0.1:8081    → data-2
http://127.0.0.1:8082    → data-3
http://127.0.0.1:8083    → data-4
```

## 🔧 Yapılandırma

### Gateway Yapılandırması

`gateway.py` dosyasında servis kayıt defteri:

```python
MICROSERVICES = {
    'data': ('127.0.0.1', 8080),
    'data-2': ('127.0.0.1', 8081),
    'data-3': ('127.0.0.1', 8082),
    'data-4': ('127.0.0.1', 8083),
}
```

Yeni bir servis eklemek için bu listeye ekleme yapın.

## 📊 Mikroservis Mimarisi Prensipleri

### 1. Service Discovery (Servis Keşfi)

- Gateway, servis kayıt defterini kullanarak servisleri bulur
- Her servis kendi adresi ve portu ile kayıtlıdır

### 2. API Gateway Pattern

- Tüm istekler gateway üzerinden geçer
- Gateway, routing, logging, authentication gibi cross-cutting concern'leri yönetir

### 3. Loose Coupling (Gevşek Bağlantı)

- Servisler birbirinden bağımsızdır
- Her servis kendi veritabanı/klasörüne sahiptir

### 4. Single Responsibility (Tek Sorumluluk)

- Her servis tek bir klasörü yönetir
- Gateway sadece routing yapar

## 🔍 Request Flow

1. **Client** → Gateway'e istek gönderir: `GET /data`
2. **Gateway** → Path'i analiz eder ve `data` servisini bulur
3. **Gateway** → İsteği `localhost:8080/` adresine proxy eder
4. **Mikroservis** → İsteği işler ve yanıt döner
5. **Gateway** → Yanıtı client'a iletir

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

## 🎯 Gelecek Geliştirmeler

- [ ] Health Check endpoints
- [ ] Load Balancing
- [ ] Rate Limiting
- [ ] Authentication & Authorization
- [ ] Request/Response Transformation
- [ ] Circuit Breaker Pattern
- [ ] Distributed Tracing
- [ ] Service Mesh entegrasyonu

## 📚 Kaynaklar

- [Microservices Patterns](https://microservices.io/patterns/)
- [API Gateway Pattern](https://microservices.io/patterns/apigateway.html)
- [Service Discovery](https://microservices.io/patterns/service-registry.html)
