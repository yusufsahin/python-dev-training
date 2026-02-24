# Görev Yöneticisi (Ch07CursorTaskApp)

PyQt6 ve SQLite ile masaüstü görev yöneticisi. Plan: `görev_yöneticisi_masaüstü_uygulaması_7e1753d8.plan.md`

## Kurulum

```bash
cd Ch07CursorTaskApp
pip install -r requirements.txt
```

## Çalıştırma

```bash
python main.py
```

Veritabanı varsayılan olarak `Ch07CursorTaskApp/tasks.db` konumunda oluşturulur. Farklı bir yol için ortam değişkeni:

```bash
set DB_PATH=C:\veri\tasks.db
python main.py
```

## Özellikler

- **Görev CRUD**: Yeni görev (Ctrl+N), düzenle (Ctrl+E), sil (Delete), listeden çift tıklayarak düzenleme
- **Filtreleme**: Durum, öncelik, kategori; başlık/açıklama arama (Ctrl+F ile arama kutusuna odak)
- **Kategoriler**: Düzenle → Kategoriler ile ekleme/düzenleme/silme ve renk seçimi
- **Durum çubuğu**: Toplam ve tamamlanan görev sayısı
- **Dışa/içe aktarma**: Dosya menüsünden JSON yedekleme ve içe aktarma

## Proje yapısı

```
Ch07CursorTaskApp/
  main.py              # Giriş noktası
  database/
    db.py              # get_db_path, get_connection, create_tables
    tasks.py           # Görev CRUD
    categories.py      # Kategori CRUD
  ui/
    main_window.py     # Ana pencere, menü, toolbar, filtre, statusbar
    task_list.py       # Görev tablosu
    task_edit_dialog.py # Görev ekleme/düzenleme formu
    category_dialog.py # Kategori yönetimi
  requirements.txt
```
