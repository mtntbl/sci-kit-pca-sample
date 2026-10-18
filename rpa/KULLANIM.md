# RPA Bot – Kullanım Kılavuzu

Altı katmanlı bir robot. Hepsi tek pakette ve `RPA_Bot.exe` üzerinden çalışır:

| Katman | Teknoloji | Ne yapar |
|---|---|---|
| Orkestrasyon | **Robot Framework** | `gorevler\*.robot` görevleri, log/rapor (`logs\robot\…\log.html`), tekrarlanabilirlik |
| Masaüstü & tarayıcı | **rpaframework** | `RPA.Windows` (UI Automation), `RPA.Browser.Selenium`, `RPA.Excel`, `RPA.PDF` |
| Belge → görsel | **pymupdf · Pillow · opencv** | PDF sayfasını görsele çevirir; kimlik kartını bulup eğimini düzelterek kırpar |
| OCR | **pytesseract + Tesseract** | Yerel (internetsiz) Türkçe metin okuma; taranmış sayfalar otomatik algılanır |
| Veri & çıktı | **openpyxl · re** | Puantaj Excel'ini okur, TC ile eşleştirir, girişe hazır Excel yazar |
| Ajan katmanı (opsiyonel) | **anthropic · MCP** | OCR'ın okuyamadığı alanları Claude'a sordurur; robotu Claude Desktop'a araç olarak açar |

Ayrıca ilk sürümdeki **PCA analizi** de aynen duruyor.

---

## Hızlı başlangıç

1. `RPA_Bot_Windows.zip` dosyasını bir klasöre çıkarın (ör. `C:\RPA_Bot`).
2. `RPA_Bot.exe`'ye çift tıklayın. Bir menü açılır:

```
  1. PCA analizi (input klasörü)
  2. İşe giriş belgelerini hazırla (input\ise_giris)
  3. Mikro'ya giriş — KURU ÇALIŞMA (yalnızca log)
  4. Mikro'ya giriş — GERÇEK (Mikro açık olmalı)
  5. Mikro ekran keşfi (locator çıkarma)
  6. Örnek: Not Defteri otomasyonu
  7. Örnek: Tarayıcı formu doldurma
  8. Kurulum kontrolü
```

3. İlk iş olarak **8 – Kurulum kontrolü**'nü çalıştırın. Tesseract, Türkçe dil paketi ve kütüphaneler `[OK]` görünmeli.
4. Denemek için `ornek_veri\ise_giris\` içindeki dosyaları `input\ise_giris\` klasörüne kopyalayıp **2**'yi seçin.
   Bu dosyalar **kurgusal** test verisidir.

> Windows SmartScreen uyarısında **Ek bilgi → Yine de çalıştır** deyin (exe imzasızdır).
> ARM64 Windows'ta paket x64 emülasyonuyla çalışır.

## Komut satırı

```
RPA_Bot.exe kontrol                                   kurulum kontrolü
RPA_Bot.exe ise-giris                                 input\ise_giris klasörünü işler
RPA_Bot.exe ise-giris --tc 12345678901 --pdf D:\belge.pdf [--puantaj D:\PUANTAJ.xlsx]
RPA_Bot.exe ocr D:\taranmis.pdf --cikti D:\metin.txt  taranmış PDF → metin
RPA_Bot.exe pca --once | --watch | --file D:\veri.txt PCA analizi
RPA_Bot.exe robot <görev> [Robot seçenekleri]         ör. robot mikro_personel_giris --variable KURU_CALISMA:hayir
RPA_Bot.exe gorevler                                  görev listesi
RPA_Bot.exe mcp                                       MCP sunucusu (Claude Desktop için)
--config D:\baska.ini                                 farklı ayar dosyası
```

Çıkış kodu `0` = başarılı, `1` = hata. UiPath, Power Automate gibi araçlardan çağırırken bu kod kullanılabilir.

---

## 1) İşe giriş belgelerini hazırlama

**Girdi (`input\ise_giris\`):**
- `PUANTAJ BİLGİLERİ.xlsx` – **GİRİŞ** sayfası. Başlık satırı otomatik bulunur. Aranan sütunlar: TC KİMLİK NO, ADI SOYADI,
  DOĞUM TARİHİ, EMEKLİ Mİ DEĞİLMİ, BİRİM, İŞE GİRİŞ TARİHİ, MESLEK, EĞİTİM DURUMU, IBN NO, TELEFON NUMARASI.
- Her personel için tek PDF, adı TC numarası olmalı (ör. `12345678901.pdf`). Dosya adında TC yoksa PDF'in içinde aranır.

**Robot ne yapar:**
1. Her sayfayı açar. Metin katmanı yoksa sayfa taranmış kabul edilir ve Tesseract ile Türkçe OCR yapılır.
2. Sayfanın belge türünü bulur: kimlik kartı, nüfus kayıt örneği, yerleşim yeri belgesi, adli sicil, diploma, sertifika.
3. Fotoğraflanmış ya da fotokopisi çekilmiş kimlik kartını bulur, eğimini düzeltip kırpar ve ayrıca okur (seri no, cinsiyet, doğum tarihi…).
4. Puantaj'la **TC üzerinden** eşleştirir. TC algoritma kontrolünü ve PDF'teki TC ile çapraz doğrulamayı yapar.
5. Checklist kurallarını uygular:
   - Ana Kanun: emekli değil → `01`, emekli → `02`
   - Kanun 2: emekli değil → `5510`, emekli → `0000`. **SEDEF istisnası:** birim SEDEF ise her zaman `0000` (`[ISE_GIRIS] sedef_birimleri`)
   - Ücret tipi her zaman **Aylık**, hesap tipi **Diğer**, çalışma kodu **0**
   - **Ücret kasıtlı olarak boş bırakılır**
   - Sicil, SGK şubesi, entegre grubu, banka ödemesi, meslek ve görev kodu → **HR ONAYI GEREKLİ** (biriminize göre öneri yazılır)
   - Çelişkiler not edilir (ör. sertifikadaki meslek ≠ Puantaj'daki meslek, doğum tarihi uyuşmazlığı, IBAN kontrol hanesi hatası)
   - Eski cüzdana özgü alanlar uydurulmaz → **Bilgi Yok**
6. Çıktı: `output\ise_giris\<AD SOYAD (TC)>_<tarih>\İşe Girişi Hazır - AD SOYAD (TC).xlsx`
   - 5 ekran başlığı altında No / Alan / Değer / Durum / Not / Kaynak
   - Renkler: **sarı** = HR onayı, **gri** = bilgi yok, **turuncu** = LLM önerisi
   - Ayrıca `hazir_veri.json` ve `gorseller\` (sayfa görüntüleri + kırpılmış kimlik) oluşur
7. İşlenen PDF `archive\ise_giris\`, hatalı olan `error\ise_giris\` klasörüne taşınır (yanında `.hata.txt` açıklaması olur).

## 2) Mikro ERP'ye giriş (RPA.Windows)

`gorevler\mikro_personel_giris.robot` dosyası hazır Excel'i okur ve **Personel Sicil Kartları (111100)** ekranının 5 sekmesini doldurur.

**Güvenlik önlemleri:**
- Varsayılan olarak **kuru çalışma** açıktır: robot tuşa basmaz, ne gireceğini yalnızca loglar.
  Gerçek giriş için `config.ini` → `[ROBOT] kuru_calisma = hayir` yapın ya da menüden **4**'ü seçin.
- Durum'u **HR ONAYI GEREKLİ** veya **LLM - KONTROL EDİN** olan satırlar, HR Durum hücresini **ONAYLANDI** yapmadıkça girilmez.
- **Kaydet tuşuna basılmaz.** Kontrol ve kayıt insan tarafından yapılır.
  Otomatik kayıt için: `--variable KAYDET:evet`.

**İlk kurulum – ekran haritası (bir kez yapılır):**
Mikro'daki alan adları sürüme göre değişir. `gorevler\kaynaklar\mikro_ekran_haritasi.resource` dosyası bir **şablondur**.
1. Mikro'da Personel Sicil Kartı ekranını açın.
2. Menüden **5 – Mikro ekran keşfi**'ni çalıştırın. Ekrandaki öğeler `logs\robot\…\log.html` dosyasına yazılır,
   öğe görüntüleri de `ekran_kesfi\` klasörüne kaydedilir.
3. Her alanın `name` / `automationid` değerini haritaya yazın (ör. `1=name:"Giriş Tarihi"` ya da `1=id:txtGirisTarihi`).
   Açılır listeleri `MIKRO_ALAN_TIPLERI` içinde `liste` olarak işaretleyin.
4. Önce kuru çalışmayla, sonra gerçek modda deneyin.

> **Mikro uzak masaüstündeyse (RDP):** RDP penceresinin içindeki öğeler yerel UI Automation'a görünmez.
> Robotu Mikro'nun çalıştığı (uzak) makineye kurun.

## 3) OCR (taranmış PDF → metin)

```
RPA_Bot.exe ocr D:\taranmis.pdf --cikti D:\metin.txt
```
Ayarlar `[OCR]` bölümündedir: `dil = tur+eng`, `dpi = 300`, `psm_belge` / `psm_kimlik` (belge türüne göre sayfa bölümleme modu).
Tesseract paketin `tesseract\` klasöründe gelir. Başka bir kurulum kullanmak için `tesseract_yolu` ayarını değiştirin.

## 4) Robot Framework görevleri

`gorevler\` klasöründeki `.robot` dosyaları düz metindir; Not Defteri'yle düzenlenebilir.
Bot kendi anahtar kelimelerini `RpaBotKeywords` kütüphanesiyle sunar:
`İşe Giriş Klasörünü İşle`, `İşe Giriş Verisi Hazırla`, `PDF Metne Çevir`, `PDF Sayfalarını Görsele Çevir`,
`Kimlik Kartlarını Kırp`, `Görselde OCR Yap`, `Excelden Giriş Verisi Oku`, `Son Hazır Excel`, `PCA Klasörünü İşle`,
`Ayarı Oku`, `Klasör Yolu`, `TC Geçerli Mi` …
Bunları RPA.Windows, RPA.Browser.Selenium, RPA.Excel.Files gibi kütüphanelerle birlikte kullanabilirsiniz.
Her çalıştırmanın raporu `logs\robot\<görev>_<tarih>\log.html` dosyasındadır.

| Görev | Açıklama |
|---|---|
| `ise_giris_hazirla` | input\ise_giris klasörünü işler |
| `mikro_personel_giris` | Hazır Excel → Mikro ekranı (varsayılan kuru çalışma) |
| `mikro_ekran_kesfi` | Mikro ekranındaki öğeleri listeler (haritayı doldurmak için) |
| `ornek_masaustu_notepad` | RPA.Windows örneği: Not Defteri'ni aç, yaz, kaydet |
| `ornek_tarayici` | RPA.Browser örneği: web formunu doldur, ekran görüntüsü al |
| `pca_analizi` | PCA analizi |

## 5) Ajan katmanı (opsiyonel, ücretli)

**a) OCR'ın okuyamadığı alanlar için Claude (`[LLM]`)**
- `aktif = evet` yapın ve API anahtarını `ANTHROPIC_API_KEY` ortam değişkenine yazın.
- Belge düzeni değişip kurallar bir alanı bulamazsa, ilgili sayfa metni ve kimlik görüntüsü Claude'a gönderilir.
  Varsayılan model `claude-opus-5-5`'tir. Ücret kullanıma göre alınır; `effort = low` daha ucuzdur.
- Claude'un doldurduğu alanlar **LLM - KONTROL EDİN** (turuncu) olarak işaretlenir ve onaylanmadan Mikro'ya girilmez.
  Claude kuralın bulduğu değerden farklı bir şey okursa alan **HR ONAYI GEREKLİ** olarak işaretlenir.
- ⚠️ **KVKK:** Bu ayar açılınca kimlik görüntüsü ve kişisel veriler Anthropic API'sine gider. Kurum onayı olmadan açmayın.

**b) MCP sunucusu (Claude Desktop ile robotu yönetme)**
`%APPDATA%\Claude\claude_desktop_config.json` dosyasına şunu ekleyin:
```json
{ "mcpServers": { "rpa-bot": { "command": "C:\\RPA_Bot\\RPA_Bot.exe", "args": ["mcp"] } } }
```
Claude'un kullanabileceği araçlar: `ocr_pdf`, `belge_analizi`, `ise_giris_hazirla`, `ise_giris_klasorunu_isle`,
`pca_analizi`, `gorev_listesi`, `robot_gorevi_calistir` (Mikro görevleri varsayılan olarak kuru çalışır).
Araç sonuçları (OCR metni dahil) Claude'a gider; KVKK uyarısı burada da geçerlidir.

## 6) PCA analizi

`input\` klasörüne `.txt` / `.csv` / `.xlsx` veri dosyası bırakın, sonra `RPA_Bot.exe pca --once` çalıştırın.
Ayarlar `[VERI]`, `[PCA]`, `[GRAFIK]`, `[CIKTI]`, `[EMAIL]` bölümlerindedir. Çıktı `output\<dosya>_<tarih>\` klasörüne yazılır.

## Otomatik çalıştırma

`gorev_zamanlayici_kur.bat` iki görev oluşturur: **RPA_Bot_IseGiris** ve **RPA_Bot_PCA** (varsayılan olarak 15 dakikada bir).
Farklı aralık için: `gorev_zamanlayici_kur.bat 60`. Kaldırmak için: `gorev_zamanlayici_kaldir.bat`.
Mikro girişi zamanlanmaz; HR onayından sonra elle başlatılması önerilir.

## Gizlilik (KVKK)

- Loglarda TC numarası maskelenir (`123******01`, `[ISE_GIRIS] tc_maskele`).
- OCR tamamen yereldir; LLM katmanı kapalıyken hiçbir veri bilgisayardan çıkmaz.
- `output\ise_giris\…\gorseller\` klasörü kimlik görüntüleri içerir. İstemiyorsanız `[OCR] ara_gorselleri_kaydet = hayir` yapın.

## Kaynaktan derleme

Python 3.12 (x64) ve Tesseract (`winget install UB-Mannheim.TesseractOCR`) kurulu bir Windows makinede `build_exe.bat` çalıştırın.
Kurgusal test belgelerini yeniden üretmek için: `python araclar\ornek_belge_uret.py`.
