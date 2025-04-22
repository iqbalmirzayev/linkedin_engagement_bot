# LinkedIn Auto Engagement Bot

Bu skript LinkedIn profillərində avtomatik `like` və `comment` etmək üçün hazırlanmışdır. Tətbiq Selenium ilə Chrome browser üzərindən işləyir.

## 0. `.env` Faylının Hazırlanması

Layihənin kök qovluğunda olan `.env` faylında dəyişiklər edin içini öz məlumatlarınız ilə doldurun:


Əgər `.env` faylı görünmürsə:

- [Windows 10 üçün izah videosu](https://www.youtube.com/watch?v=Y1iz0-j8uKo)
- [Windows 11 üçün izah videosu](https://www.youtube.com/watch?v=H6JI0kv-_io)

---

## 1. Python Yüklənməsi

Əgər sisteminizdə Python yoxdur:

- [Python necə yüklənir - izah videosu](https://www.youtube.com/watch?v=C3bOxcILGu4)  
Videoda əsas olan hissə **2:45-ə qədərdir**, amma tamamını izləmək də faydalıdır.

---

## 2. Terminalda Layihə Qovluğunu Açın

Botun yerləşdiyi qovluğa gəlin, `scraper.py`, `requirements.txt` və `.env` faylları bu qovluqda olmalıdır.

- Qovluğa sağ klik edin → **“Terminalda açın” (Open in Terminal)** seçin

---

## 3. Kitabxanaların Qurulması

Terminala aşağıdakı əmr daxil edin:

```
pip install -r requirements.txt
```

---

## 4. Botun İşə Salınması

```
python scraper.py
```

Əgər **ilk dəfə** çalışdırırsınızsa, **birinci dəfə** giriş üçün skript avtomatik LinkedIn-ə daxil olacaq və cookie-ləri saxlayacaq. **İkinci dəfə** yenidən `python scraper.py` yazaraq normal istifadəyə başlaya bilərsiniz.

---

## 5. Şərhləri Dəyişmək

`comments.txt` adlı faylda istədiyiniz sayda fərqli şərhləri ayrı-ayrı sətirlərdə yaza bilərsiniz. Bot bu fayldan random şəkildə birini seçib şərh kimi yazacaq.

---

## Qeyd

Bu skript yalnız şəxsi test və tədris məqsədləri üçün nəzərdə tutulub.