# Cursor / AI için kısa yönergeler

- **SQL Server**; tablo ve kolon isimlerini değiştirme; İngilizce entity isimleri korunur.
- **Database-first**: `database/` scriptleri sırayla çalıştırılır.
- **Python konsol**: `src/student_course_center/` — katmanlar `domain`, `infrastructure`, `application`, `console`.
- Listeler: mümkünse `dbo.vw_*` view’ları; ham tablo için `list attendance-records`, `list exam-results-rows`. Kayıt / yoklama / sınav notu: `dbo.usp_*` prosedürleri.
- Detay: `show student`, `show teacher`. `activate` ↔ `deactivate` (`IsActive`).
- Test verisi: `seed faker` (Faker; `pip install -e ".[dev]"`).
- Bağlantı: ortam değişkeni `STUDENT_COURSE_CENTER_CONNECTION_STRING`.
- Plan ve ilerleme: [docs/DEVELOPMENT_PLAN.md](docs/DEVELOPMENT_PLAN.md).
