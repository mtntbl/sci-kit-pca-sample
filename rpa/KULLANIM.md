# PCA RPA Botu – Kullanım Kılavuzu

`PCA_Example.ipynb` içindeki PCA analizini otomatik çalıştıran Windows botu.
`input` klasörüne bırakılan veri dosyalarını alır, PCA uygular, Excel raporu ve grafik üretir,
dosyayı arşive taşır ve isteğe bağlı olarak sonucu e-posta ile gönderir.

## Paket içeriği

| Dosya / Klasör | Açıklama |
|---|---|
| `PCA_RPA.exe` | Bot (Python gerektirmez) |
| `config.ini` | Tüm ayarlar |
| `calistir.bat` | Klasördeki dosyaları bir kez işler |
| `izleme_modu.bat` | `input` klasörünü sürekli izler |
| `gorev_zamanlayici_kur.bat` | Botu Windows Görev Zamanlayıcı'ya ekler (varsayılan 15 dk'da bir) |
| `gorev_zamanlayici_kaldir.bat` | Zamanlanmış görevi siler |
| `input\` | İşlenecek dosyaları buraya bırakın |
| `output\` | Raporlar (her dosya için zaman damgalı alt klasör) |
| `archive\` | Başarıyla işlenen kaynak dosyalar |
| `error\` | İşlenemeyen dosyalar + `*.hata.txt` açıklaması |
| `logs\` | Günlük log dosyaları (30 gün saklanır) |
| `ornek_veri\data2.txt` | Test için örnek veri |

## Hızlı başlangıç

1. Zip'i bir klasöre çıkarın (ör. `C:\PCA_RPA`).
2. `ornek_veri\data2.txt` dosyasını `input\` klasörüne kopyalayın.
3. `calistir.bat`'a çift tıklayın.
4. `output\data2_<tarih>\` altında şunları bulacaksınız:
   - `data2_pca_rapor.xlsx` – sayfalar: **Ozet**, **Varyans** (oran + kümülatif), **Yukler** (loadings), **PCA_Skorlari** (+ orijinal veri)
   - `data2_pca_scatter.png` – 3B PCA saçılım grafiği (`DURATION_SECONDS < 3600` kırmızı, diğerleri mavi)
   - `data2_variance.png` – açıklanan / kümülatif varyans grafiği

> Windows SmartScreen "tanınmayan uygulama" uyarısı verirse **Ek bilgi → Yine de çalıştır** deyin
> (exe imzasızdır). İlk açılış birkaç saniye sürebilir.

## Çalışma modları

```
PCA_RPA.exe                      config.ini'deki [GENEL] mod değerine göre
PCA_RPA.exe --once               bir kez işle ve çık (Görev Zamanlayıcı için)
PCA_RPA.exe --watch              sürekli izle
PCA_RPA.exe --file D:\veri.txt   tek bir dosyayı işle
PCA_RPA.exe --config D:\x.ini    farklı ayar dosyası kullan
PCA_RPA.exe --init               eksikse config.ini ve klasörleri oluştur
```

Çıkış kodu: `0` = tüm dosyalar başarılı, `1` = en az bir dosya hatalı (başka RPA araçlarından,
ör. UiPath / Power Automate Desktop'tan çağırırken kullanılabilir).

## Önemli ayarlar (`config.ini`)

- **[KLASORLER]** – Göreli yollar exe klasörüne göredir. Ağ klasörü de verilebilir:
  `giris = \\sunucu\paylasim\pca_giris`
- **[VERI]**
  - `ayirici` – `tab` (orijinal `data2.txt`), `virgul`, `noktali_virgul`, `auto` …
  - `kodlama` – `auto` UTF‑8 ve Windows Türkçe (cp1254) dener
  - `cikarilacak_sutunlar` – analize girmeyecek sütunlar (notebook'taki `drop`)
  - `kodlanacak_sutunlar` – `auto`: yalnızca metin sütunları LabelEncoder'dan geçer;
    `all`: notebook'taki gibi tüm sütunlar kodlanır
  - `bos_deger` – `sil` / `sifir` / `ortalama`
- **[PCA]** – `bilesen_sayisi` (varsayılan 3), `standartlastir` (StandardScaler)
- **[GRAFIK]** – renk sütunu ve eşiği (varsayılan `DURATION_SECONDS`, 3600 sn = 1 saat)
- **[CIKTI]** – Excel raporu, orijinal veriyi ekleme, arşive taşıma
- **[EMAIL]** – `aktif = evet` yapın, SMTP bilgilerini girin. Şifreyi dosyaya yazmak yerine
  `PCA_RPA_SMTP_SIFRE` ortam değişkeni kullanılabilir.

Sütun adlarındaki tırnaklar (`'PARTNO'`) otomatik temizlenir; ayarlarda tırnaksız yazın.

## Otomatik çalıştırma

`gorev_zamanlayici_kur.bat` → her 15 dakikada bir `--once` ile çalışır.
Farklı aralık için komut satırından: `gorev_zamanlayici_kur.bat 60`.
Kurulum sonrası görev, **Görev Zamanlayıcı → Görev Zamanlayıcı Kitaplığı → PCA_RPA** altında
görülebilir/düzenlenebilir (ör. "kullanıcı oturum açmamışken de çalıştır").

## Kaynaktan derleme

Python 3.10+ kurulu bir Windows makinede `build_exe.bat` çalıştırın; `PCA_RPA_Windows.zip` üretir.
Kaynak kod: `pca_rpa.py`.
