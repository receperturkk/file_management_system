# Controller Projesi — Sunum

Recep Erturk • Ekim 2025

---

## 1) Amaç ve Kapsam

- **Amaç**: Basit, modüler ve eğitim amaçlı bir Python HTTP sunucusu ile statik içerik sunumu yapmak.
- **Kapsam**: Yerel dosyaların sunulması, temel loglama, doğru MIME türleri, kolay kurulum ve çalıştırma.

---

## 2) Çözümün Özeti

- **Teknoloji**: Python 3, `http.server` standart kütüphanesi
- **Sunucu**: `ThreadingHTTPServer` ile eşzamanlı istekler
- **İstek İşleyici**: `SimpleHTTPRequestHandler` tabanlı özel handler
- **Port**: 8080 (varsayılan)
- **MIME Desteği**: `image/svg+xml` için ek tanımlama
- **Loglama**: IP, tarih, metot ve yol bilgisini stdout'a yazma

---

## 3) Mimarî ve Akış

1. İstemci (tarayıcı/istemci uygulaması) → `http://localhost:8080`
2. Sunucu, çalışma dizinindeki (proje klasörü) dosyaları statik olarak sunar
3. Handler, her isteği loglar; doğru içerik türünü belirler
4. Eşzamanlı istekler iş parçacıkları ile ele alınır

---

## 4) Ana Özellikler

- Statik dosya servisi (ör. `index.html`)
- Kolay kurulum ve tek komutla çalıştırma
- Eşzamanlı istek desteği (Threading)
- Genişletilebilir, modüler yapı
- Windows/macOS/Linux uyumlu (Python 3.8+)

---

## 5) Kurulum

1. Python 3.8+ kurulu olduğundan emin olun
2. Depoyu indirin/klonlayın
3. Proje klasörüne geçin

```cmd
cd "c:\\Users\\recep\\Desktop\\Beykoz Edu\\controller-receperturkk"
```

---

## 6) Çalıştırma

```cmd
python server.py
```

- Çıktı: `Sunucu http://localhost:8080 portunda çalışıyor`
- Tarayıcıdan `http://localhost:8080` adresine gidin

---

## 7) Demo Senaryosu

1. Sunucuyu başlatın
2. `http://localhost:8080` → `index.html` yüklenir
3. Örnek bir dosya (örn. `/style.css`, `/images/logo.svg`) isteyin
4. Terminalde logları gözlemleyin (IP, tarih, yöntem, yol)
5. Bulunmayan bir yol deneyin → 404 yanıtı ve log kaydı

---

## 8) Proje Yapısı

```
controller-receperturkk/
├─ README.md       # Kurulum ve kullanım
├─ SUNUM.md        # Bu sunum
├─ server.py       # HTTP sunucusu
└─ index.html      # Örnek statik içerik (isteğe bağlı)
```

---

## 9) Öne Çıkan Uygulama Detayları

- `ThreadingHTTPServer`: Aynı anda birden fazla isteği işler
- `SimpleHTTPRequestHandler`: Statik dosya servisinin temelini sağlar
- `mimetypes.add_type('image/svg+xml', '.svg')`: SVG için doğru içerik türü
- Çalışma dizini, script dizinine alınır: Dosyalar güvenli ve tutarlı sunulur
- Özel `log_message`: Konsola okunabilir log formatı

---

## 10) Ek: Faydalı Komutlar

```cmd
python -V              # Python sürümünü kontrol et
python server.py       # Sunucuyu başlat
```