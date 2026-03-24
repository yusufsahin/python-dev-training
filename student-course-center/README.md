# Student Course Center

SQL Server tabanlı öğrenci / ders / öğretmen yönetimi için veritabanı scriptleri ve **Python konsol istemcisi** (pyodbc, native SQL).

Ayrıntılı geliştirme adımları: [docs/DEVELOPMENT_PLAN.md](docs/DEVELOPMENT_PLAN.md).

**Konsol uygulaması kullanım kılavuzu:** [docs/KULLANIM_KLAVUZU.md](docs/KULLANIM_KLAVUZU.md).

## Veritabanı kurulum sırası

1. `database/00_create_database.sql`
2. `database/01_schema.sql`
3. `database/02_views.sql`
4. `database/03_procedures.sql`
5. `database/04_seed.sql`
6. (isteğe bağlı) `database/99_smoke_test.sql`

Varsayılan veritabanı adı: `StudentCourseCenterDb`.

## Python konsol uygulaması

### Kurulum

```powershell
cd student-course-center
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

### Bağlantı

`.env.example` dosyasını `.env` olarak kopyalayın ve `STUDENT_COURSE_CENTER_CONNECTION_STRING` değerini doldurun.

### Komutlar

```powershell
python -m student_course_center ping
python -m student_course_center list students --institution 1
python -m student_course_center list enrollment-details
python -m student_course_center list teacher-schedule
python -m student_course_center list exam-results
python -m student_course_center enroll --student 1 --group 1
python -m student_course_center attendance --group 1 --student 1 --date 2026-01-20 --status Present
python -m student_course_center exam-result --exam 1 --student 1 --score 90
```

Kurulum sonrası `scc` kısa komutu da kullanılabilir: `scc ping`.

**Kayıt / yoklama / sınav notu** yalnızca şu akışlarla yapılır: `enroll`, `attendance`, `exam-result` (stored procedure).

Diğer varlıklar için **doğrudan SQL** (konsol `create`, `update`, `deactivate`, `delete`):

```powershell
python -m student_course_center list institutions
python -m student_course_center list enrollments --group 1
python -m student_course_center list exams --group 1
python -m student_course_center create course --institution 1 --code BIO --name Biyoloji
python -m student_course_center update student --id 1 --phone 05001112233
python -m student_course_center update enrollment --id 1 --status Left
python -m student_course_center deactivate course --id 3
python -m student_course_center delete lesson-schedule --id 1
```

`delete` — `lesson-schedule`, `teacher-course`, `exam-result` (hard delete). Diğer varlıklar `deactivate` / `activate` ile `IsActive`.

```powershell
python -m student_course_center show student --id 1
python -m student_course_center show teacher --id 1
python -m student_course_center list attendance-records --group 1
python -m student_course_center list exam-results-rows --exam 1
python -m student_course_center activate student --id 1
```

## Test

```powershell
pip install -e ".[dev]"
pytest
```

`STUDENT_COURSE_CENTER_CONNECTION_STRING` yoksa veritabanı smoke testleri atlanır; import/help testleri her zaman çalışır.

## Faker ile test verisi

[Faker](https://faker.readthedocs.io/) geliştirme bağımlılığıdır (`pip install -e ".[dev]"` veya `pip install Faker`).

```powershell
python -m student_course_center seed faker --dry-run
python -m student_course_center seed faker --seed 42 --students 20 --teachers 4 --courses 5 --groups 4
```

Yeni bir **Institution** ve bağlı dönem, öğretmen, öğrenci, ders, `TeacherCourses`, gruplar, program satırları, `enroll` (SP), sınavlar ve `exam-result` (SP) üretir. `--locale` (ör. `en_US`, `tr_TR`) ve `--exam-skip-rate` ile oynanabilir.
