# Student Course Center — Kullanım Kılavuzu

Bu belge **Python konsol uygulamasının** (`scc` / `python -m student_course_center`) son kullanıcı ve yönetici kullanımını anlatır.

---

## 1. Ne işe yarar?

SQL Server üzerindeki **StudentCourseCenterDb** veritabanına bağlanır; öğrenci, öğretmen, ders, grup, kayıt, yoklama ve sınav verilerini **komut satırından** listelemenize, oluşturmanıza ve güncellemenize olanak verir.

---

## 2. Ön koşullar

| Gereksinim | Açıklama |
|------------|----------|
| Python | 3.11 veya üzeri |
| SQL Server | Veritabanı oluşturulmuş ve script’ler uygulanmış olmalı (bkz. proje `README.md`) |
| ODBC Sürücüsü | Örn. **ODBC Driver 18 for SQL Server** (Windows’ta genelde ayrı kurulur) |
| Ağ / yerel erişim | Bağlantı dizesindeki sunucuya erişim |

Veritabanı kurulum sırası: `database/` altındaki `00` → `01` → `02` → `03` → `04` dosyaları (isteğe bağlı `99_smoke_test.sql`).

---

## 3. Kurulum

PowerShell örneği (proje kökü `student-course-center`):

```powershell
cd c:\source\StudentSys\student-course-center
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

Geliştirme araçları, Faker ve pytest için:

```powershell
pip install -e ".[dev]"
```

---

## 4. Bağlantı ayarı

1. `.env.example` dosyasını **`.env`** olarak kopyalayın (aynı klasörde).
2. Şu değişkeni doldurun:

`STUDENT_COURSE_CENTER_CONNECTION_STRING`

### Örnek (SQL kimlik doğrulama, yerel Express)

```text
DRIVER={ODBC Driver 18 for SQL Server};SERVER=.\SQLEXPRESS;DATABASE=StudentCourseCenterDb;UID=sa;PWD=ŞİFRENİZ;TrustServerCertificate=yes;
```

### Örnek (Windows kimlik doğrulama)

```text
DRIVER={ODBC Driver 18 for SQL Server};SERVER=.\SQLEXPRESS;DATABASE=StudentCourseCenterDb;Trusted_Connection=yes;TrustServerCertificate=yes;
```

Uygulama çalışırken **çalışma dizininde** `.env` aranır; genelde proje kökünden komut verin.

**Güvenlik:** `.env` dosyasını versiyon kontrolüne eklemeyin; şifreleri paylaşmayın.

---

## 5. Uygulamayı çalıştırma

### Yöntem A — Modül (önerilir)

```powershell
python -m student_course_center --help
python -m student_course_center ping
```

### Yöntem B — Kısa komut

`pip install -e .` sonrası:

```powershell
scc --help
scc ping
```

Tüm alt komutlar her iki yöntemde de aynıdır; aşağıda `scc` yazılmıştır, dilerseniz `python -m student_course_center` ile değiştirin.

### Yardım

```powershell
scc --help
scc list --help
scc list students --help
scc create --help
```

---

## 6. Önemli kurallar

### Stored procedure ile yapılması gerekenler

| İş | Komut | Açıklama |
|----|--------|----------|
| Öğrenciyi gruba kaydetme | `enroll` | `usp_EnrollStudentToClassGroup` — çift kayıt ve kapasite kontrolü burada |
| Yoklama | `attendance` | `usp_RecordAttendance` — durum ve aktif kayıt kontrolü |
| Sınav notu (ekle/güncelle) | `exam-result` | `usp_SaveExamResult` — not üst sınırı burada |

### Doğrudan SQL ile yapılanlar

`create`, `update`, çoğu `list`, `show`, `deactivate`, `activate` ve sınırlı `delete` komutları tablolara doğrudan yazar/okur.

### Pasifleştirme (soft mantık)

Ana varlıklarda silme yerine **`deactivate`** kullanılır (`IsActive = 0`). Geri almak için **`activate`** (`IsActive = 1`).

### Kalıcı silme (`delete`)

Yalnızca şunlar için: **`lesson-schedule`**, **`teacher-course`**, **`exam-result`** (tek satır). Diğer tablolar için konsolda genel `DELETE` yoktur.

### Listeleme ve görünümler

- Raporlama için: `list enrollment-details`, `teacher-schedule`, `exam-results` → veritabanı **view**’ları.
- Ham tablo: `list attendance-records`, `list exam-results-rows`, `list enrollments` vb.

---

## 7. Komut özeti

### Bağlantı testi

```powershell
scc ping
```

### Sentetik veri (Faker)

Önce: `pip install Faker` veya `pip install -e ".[dev]"`.

```powershell
scc seed faker --dry-run
scc seed faker --seed 42 --students 20 --teachers 4 --courses 5 --groups 4
```

Seçenekler için: `scc seed faker --help` (`--locale`, `--exam-skip-rate`, kapasite aralığı vb.).

### Tek kayıt detayı

```powershell
scc show student --id 1
scc show teacher --id 2
scc show student --id 1 --include-inactive
```

### Listeleme (`list <varlık>`)

Ortak seçenekler (uygulanan komutlarda): `--institution ID`, `--include-inactive`.

| Komut | Açıklama |
|--------|-----------|
| `list students` | Öğrenciler |
| `list teachers` | Öğretmenler |
| `list courses` | Dersler |
| `list class-groups` | Sınıf grupları |
| `list academic-terms` | Akademik dönemler |
| `list institutions` | Kurumlar |
| `list enrollments` | Kayıt tablosu; `--student`, `--group` |
| `list lesson-schedules` | Program; `--group` |
| `list exams` | Sınavlar; `--group` |
| `list teacher-courses` | Öğretmen–ders eşlemesi |
| `list attendance-records` | Yoklama satırları; `--group`, `--student`, `--from-date`, `--to-date` |
| `list exam-results-rows` | `ExamResults` tablosu; `--exam`, `--student` |
| `list enrollment-details` | View: kayıt özeti |
| `list teacher-schedule` | View: öğretmen programı |
| `list exam-results` | View: sınav sonuçları (genişletilmiş) |

### Oluşturma (`create <tür>`)

Detaylı parametreler için: `scc create <tür> --help`.

| Alt komut | Özet |
|-----------|------|
| `create institution` | `--name` (zorunlu); `--phone`, `--email`, `--address` |
| `create student` | `--institution`, `--student-no`, `--first-name`, `--last-name`; isteğe bağlı doğum tarihi, iletişim, okul, sınıf |
| `create teacher` | `--institution`, `--teacher-no`, isimler; isteğe bağlı iletişim, `hire-date` |
| `create course` | `--institution`, `--code`, `--name`; `--description` |
| `create academic-term` | `--institution`, `--name`, `--start`, `--end` (tarih ISO: `YYYY-MM-DD`) |
| `create class-group` | `--institution`, `--term`, `--course`, `--teacher`, `--code`, `--name`; `--capacity`, `--classroom` |
| `create lesson-schedule` | `--group`, `--day` (1–7), `--start`, `--end` (saat `HH:MM` veya `HH:MM:SS`), `--room` |
| `create exam` | `--group`, `--name`, `--date`; `--total` (varsayılan 100) |
| `create teacher-course` | `--teacher`, `--course` |

### Güncelleme (`update <tür>`)

En az bir alan verilmelidir. `scc update student --help` vb.

| Alt komut | Not |
|-----------|-----|
| `update student` | `--id` + isteğe bağlı alanlar |
| `update teacher` | `--id` + alanlar |
| `update course` | `--id`; `--code`, `--name`, `--description` |
| `update academic-term` | `--id`; `--name`, `--start`, `--end` |
| `update institution` | `--id`; iletişim alanları |
| `update class-group` | `--id`; kod, ad, kapasite, sınıf, term/course/teacher |
| `update enrollment` | `--id` (StudentEnrollmentId), `--status` → **Active**, **Left**, **Completed** |
| `update lesson-schedule` | `--id`; `--day`, `--start`, `--end`, `--room` |
| `update exam` | `--id`; `--name`, `--date`, `--total` |

### Pasif / aktif

```powershell
scc deactivate student --id 3
scc activate student --id 3
```

Varlıklar: `institution`, `student`, `teacher`, `course`, `academic-term`, `class-group`.

### Silme

```powershell
scc delete lesson-schedule --id 10
scc delete teacher-course --id 5
scc delete exam-result --id 2
```

### İş kurallı akışlar

```powershell
scc enroll --student 1 --group 1
scc attendance --group 1 --student 1 --date 2026-01-20 --status Present --note "Zamanında"
scc exam-result --exam 1 --student 1 --score 87.5 --note "İyi"
```

**Yoklama durumu (`--status`):** tam olarak **Present**, **Absent**, **Late** veya **Excused** (İngilizce, bu yazımla).

---

## 8. Çıkış kodları

| Kod | Anlam |
|-----|--------|
| 0 | Başarılı |
| 1 | Veritabanı hatası (`pyodbc`) |
| 2 | Kullanım / doğrulama / yapılandırma (ör. bağlantı dizesi yok, geçersiz parametre) |

---

## 9. Örnek iş akışı

1. `scc ping` ile bağlantıyı doğrula.  
2. `scc list institutions` ve `scc list academic-terms --institution 1` ile kurum/dönem ID’lerini gör.  
3. `scc list class-groups --institution 1` ile grup ID’lerini al.  
4. `scc enroll --student <StudentId> --group <ClassGroupId>` ile kayıt.  
5. `scc attendance --group ... --student ... --date ... --status Present` ile yoklama.  
6. `scc create exam --group ... --name "Vize" --date 2026-03-01 --total 100` ile sınav oluştur; `scc list exams --group ...` ile `ExamId` al.  
7. `scc exam-result --exam <ExamId> --student <StudentId> --score 75` ile not gir.

---

## 10. Sorun giderme

- **“Set environment variable STUDENT_COURSE_CENTER_CONNECTION_STRING”**  
  `.env` yok, boş veya yanlış dizinde çalışıyorsunuz. Komutu proje kökünden çalıştırın veya ortam değişkenini elle export edin.

- **ODBC / sürücü hataları**  
  Bağlantı dizesindeki `DRIVER={...}` adı, “ODBC Veri Kaynakları”nda görünen adla aynı olmalı.

- **Kayıt / kapasite / çift kayıt hataları**  
  `enroll` SP mesajlarını okuyun; aynı öğrenci aynı grupta tekrar eklenemez, kapasite aşılamaz.

- **Not sınırı**  
  Not, ilgili sınavın `TotalScore` değerini aşamaz; `exam-result` SP bunu reddeder.

---

## 11. İlgili dosyalar

| Dosya | İçerik |
|--------|--------|
| [README.md](../README.md) | Proje özeti, kurulum, kısa örnekler |
| [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) | Geliştirme fazları |
| `.env.example` | Bağlantı dizesi şablonu |

---

*Bu kılavuz, depodaki konsol uygulamasının mevcut sürümüne göre hazırlanmıştır. Komutların güncel parametreleri için her zaman `scc <komut> --help` kullanın.*
