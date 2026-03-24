# Student Course Center — Geliştirme planı (Python konsol)

Teknoloji: **Python 3.11+**, **pyodbc**, **native SQL**, **SQL Server**. Yazma kuralları: listeler için **view**'lar, kayıt/yoklama/not için **stored procedure**'ler. Tablo/kolon isimlerine dokunulmaz.

## Faz 0 — Ön koşullar

- Script sırası: `00` → `01` → `02` → `03` → `04` → (isteğe bağlı) `99`.
- ODBC Driver 18 for SQL Server.
- `STUDENT_COURSE_CENTER_CONNECTION_STRING` ortam değişkeni.

## Faz 1 — Proje iskeleti

- `pyproject.toml`, `requirements.txt`, paket `student_course_center`.
- Katmanlar: `domain`, `infrastructure`, `application`, `console`.

## Faz 2 — Altyapı

- Bağlantı, `fetch_all`, `execute_sp`, hata yakalama.

## Faz 3 — Salt okuma (view / tablo)

- Öğrenci, öğretmen, ders, grup listeleri.
- `vw_StudentEnrollmentDetails`, `vw_TeacherSchedule`, `vw_StudentExamResults`.

## Faz 4 — SP komutları

- `usp_EnrollStudentToClassGroup`, `usp_RecordAttendance`, `usp_SaveExamResult`.

## Faz 5 — CRUD (genişletme)

- Kalan modüller için doğrudan SQL; yukarıdaki üç akış SP ile kalır.

## Faz 6 — Sertleştirme

- `.cursor/rules`, pytest, bağlantı varsa DB smoke (`tests/`).

## İlerleme durumu

- [x] Faz 1–2 — iskelet + DB katmanı
- [x] Faz 3 — liste komutları
- [x] Faz 4 — üç SP komutu
- [x] Faz 5 — konsol CRUD (`create` / `update` / `deactivate` / `delete` + ek `list` komutları)
- [x] Faz 6 — temel pytest + eksik komutlar (aşağıda)

## Tamamlanan eksikler (prompt hizalama)

- `AttendanceRecords` / `ExamResults` tablo listeleri: `list attendance-records`, `list exam-results-rows`
- Öğrenci / öğretmen detay: `show student`, `show teacher`
- `IsActive` geri açma: `activate …`
- Not satırı silme: `delete exam-result` (tablo satırı; upsert yine `exam-result` SP)
- Faker: `seed faker` (bkz. README) — yeni kurum + ilişkili sentetik veri
