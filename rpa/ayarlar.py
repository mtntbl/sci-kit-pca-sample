# -*- coding: utf-8 -*-
"""Ortak ayarlar: PCA varsayılanları + belge/OCR/işe giriş/LLM/robot bölümleri."""

import os
import shutil
import sys

import pca_rpa

EK_CONFIG = """
; =====================================================================
;  BELGE İŞLEME / OCR / İŞE GİRİŞ / ROBOT / LLM
; =====================================================================

[OCR]
; Tesseract yolu. Paketle gelen sürüm: tesseract\\tesseract.exe
; Boş bırakılırsa PATH ve C:\\Program Files\\Tesseract-OCR aranır.
tesseract_yolu = tesseract\\tesseract.exe
; Dil(ler): tur, eng ya da tur+eng
dil = tur+eng
; PDF sayfalarını görsele çevirirken çözünürlük (OCR için 300 önerilir)
dpi = 300
; Tesseract sayfa bölümleme modu. 3 = otomatik, 4 = tek sütun, 6 = tek blok, 11 = dağınık metin
psm_belge = 4
psm_kimlik = 11
; Sayfada bu kadar karakterden az metin katmanı varsa taranmış kabul edilir ve OCR yapılır
min_metin_karakter = 40
; Görselleri gri/eşikleme ile iyileştir
on_isleme = evet
; Ara görselleri (sayfa PNG'leri, kırpılmış kimlik) çıktı klasörüne kaydet
ara_gorselleri_kaydet = evet

[ISE_GIRIS]
; Personel PDF'lerinin bırakılacağı klasör. Dosya adında 11 haneli TC olmalı (ör. 12345678901.pdf)
giris = input\\ise_giris
; Puantaj Excel dosyası (tam yol ya da exe klasörüne göre)
puantaj = input\\ise_giris\\PUANTAJ BİLGİLERİ.xlsx
puantaj_sayfa = GİRİŞ
; Çıktı klasörü
cikti = output\\ise_giris
; İşlenen PDF'i arşive taşı
arsive_tasi = evet
; Kurallar (checklist): Sedef istisnası uygulanacak birim adları (virgülle)
sedef_birimleri = SEDEF
; Loglarda TC'yi maskele (KVKK)
tc_maskele = evet

[LLM]
; Ajan katmanı (opsiyonel). Düzen değişince / OCR'ın okuyamadığı alanlarda Claude'a sorar.
; DİKKAT: Etkinleştirilirse kişisel veriler (kimlik görüntüsü, OCR metni) Anthropic API'sine gönderilir.
; KVKK açısından kurum onayı alınmadan açmayın.
aktif = hayir
; API anahtarı ANTHROPIC_API_KEY ortam değişkeninden okunur. İsterseniz buraya yazabilirsiniz.
api_anahtari =
model = claude-opus-5-5
; low | medium | high  (düşük = daha ucuz/hızlı)
effort = medium
; Kimlik kartı görüntüsünü de gönder (görsel okuma)
gorsel_gonder = evet
; Yalnızca kural/OCR ile bulunamayan alanlar için çağır
sadece_eksikler = evet

[ROBOT]
; Robot Framework görev dosyalarının klasörü
gorev_klasoru = gorevler
; Robot log/rapor klasörü
cikti = logs\\robot
; Mikro giriş robotunda gerçek tuş/tıklama yerine yalnızca log yaz (güvenli deneme)
kuru_calisma = evet
"""

TAM_CONFIG = pca_rpa.DEFAULT_CONFIG + EK_CONFIG


class Ayarlar(pca_rpa.Settings):
    """pca_rpa.Settings'in tüm bölümleri tanıyan sürümü."""

    def __init__(self, path):
        import configparser

        self.path = path
        self.base = os.path.dirname(os.path.abspath(path))
        cp = configparser.ConfigParser(interpolation=None, inline_comment_prefixes=(";", "#"))
        cp.read_string(TAM_CONFIG)
        if os.path.exists(path):
            with open(path, encoding="utf-8-sig") as f:
                cp.read_file(f)
        self.cp = cp

    def yol(self, sec, key, olustur=False):
        p = self.get(sec, key)
        if not p:
            return ""
        p = pca_rpa.resolve(p, self.base)
        if olustur:
            os.makedirs(p, exist_ok=True)
        return p


def varsayilan_config_yolu():
    return os.path.join(pca_rpa.app_dir(), "config.ini")


def ayarlari_yukle(path=None):
    return Ayarlar(path or varsayilan_config_yolu())


def tesseract_bul(ayarlar):
    """Tesseract çalıştırılabilir dosyasını bulur; bulunamazsa None."""
    adaylar = []
    p = ayarlar.yol("OCR", "tesseract_yolu")
    if p:
        adaylar.append(p)
    w = shutil.which("tesseract")
    if w:
        adaylar.append(w)
    if sys.platform.startswith("win"):
        for k in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA"):
            base = os.environ.get(k)
            if base:
                adaylar.append(os.path.join(base, "Tesseract-OCR", "tesseract.exe"))
                adaylar.append(os.path.join(base, "Programs", "Tesseract-OCR", "tesseract.exe"))
    for a in adaylar:
        if a and os.path.isfile(a):
            return a
    return None
