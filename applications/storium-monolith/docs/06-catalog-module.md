# 06 — Catalog Modülü

## Kapsam
- Ana sayfa (kök kategoriler + öne çıkan ürünler)
- Kategori bazlı ürün listesi (sayfalama ile)
- Ürün detay sayfası
- Ürün arama

---

## URL Yapısı (apps/catalog/urls.py)

```python
from django.urls import path
from apps.catalog import views

app_name = 'catalog'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('kategori/<slug:slug>/', views.CategoryProductListView.as_view(), name='category_detail'),
    path('urun/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('arama/', views.ProductSearchView.as_view(), name='product_search'),
]
```

Ana `storium/urls.py`'de:
```python
path('', include('apps.catalog.urls', namespace='catalog')),
```

---

## Views (apps/catalog/views.py)

### Ortak Service Fabrikası

`apps/catalog/service_provider.py` içinde `get_catalog_service()` — view'lar ve `catalog_nav` context processor aynı örneği kullanır (repository wiring tek yerde).

### Context processor (sol menü / footer)

`apps/catalog/context_processors.catalog_nav`, `storium/settings/base.py` içinde kayıtlıdır. `CatalogService.get_category_nav_tree()` ile kök + bir seviye alt kategorileri `CategoryNavNode` DTO listesi olarak şablona verir (`catalog_nav`). `/kategori/<slug>/` yolundan `catalog_nav_active_slug` üretilir; ürün detayında `ProductDetailView` aynı anahtarı ürünün `category_slug` değeriyle günceller (sidebar’da aktif kategori vurgusu).

### HomeView

```python
class HomeView(View):
    template_name = 'catalog/home.html'

    def get(self, request):
        service = get_catalog_service()
        context = {
            'root_categories': service.get_root_categories(),
            'featured_products': service.get_featured_products(count=8),
        }
        return render(request, self.template_name, context)
```

### CategoryProductListView

```python
class CategoryProductListView(View):
    template_name = 'catalog/product_list.html'

    def get(self, request, slug):
        page = int(request.GET.get('page', 1))
        service = get_catalog_service()
        try:
            data = service.get_category_with_products(slug, page=page)
        except CategoryNotFoundException:
            raise Http404
        return render(request, self.template_name, {'data': data})
```

### ProductDetailView

```python
class ProductDetailView(View):
    template_name = 'catalog/product_detail.html'

    def get(self, request, slug):
        service = get_catalog_service()
        try:
            data = service.get_product_detail(slug)
        except ProductNotFoundException:
            raise Http404
        return render(request, self.template_name, {
            'data': data,
            'catalog_nav_active_slug': data.product.category_slug,
        })
```

### ProductSearchView

```python
class ProductSearchView(View):
    template_name = 'catalog/search_results.html'

    def get(self, request):
        query = request.GET.get('q', '').strip()
        data = None
        if len(query) >= 2:     # En az 2 karakter aranmalı
            service = get_catalog_service()
            data = service.search_products(query, page=int(request.GET.get('page', 1)))
        return render(request, self.template_name, {'data': data, 'query': query})
```

---

## Template Yapısı

### templates/catalog/home.html

Bloklar:
- `{% block title %}Storium — Ana Sayfa{% endblock %}`
- Hero banner: Jumbotron veya full-width Bootstrap carousel
- **Kategoriler bölümü**: `root_categories` — Bootstrap card grid (3-4 sütun)
  - Her kart: kategori ismi, `href="{% url 'catalog:category_detail' slug=cat.slug %}"`
- **Öne çıkan ürünler**: `featured_products` — Bootstrap card grid (4 sütun, md:2, sm:1)
  - Her kart: ürün görseli, isim, fiyat, "İncele" butonu

### templates/catalog/product_list.html

- `{% block title %}{{ data.category.name }}{% endblock %}`
- Breadcrumb: `{% include 'partials/_breadcrumb.html' with breadcrumb=data.breadcrumb %}`
- Başlık: `<h1>{{ data.category.name }}</h1>` + `<small>{{ data.total_count }} ürün</small>`
- Ürün grid: Bootstrap card, 3 sütun (col-lg-4 col-md-6)
  - Her kart: görsel, isim, fiyat, stok durumu badge, "Detay" linki
- Sayfalama: `{% include 'partials/_pagination.html' with data=data %}`

### templates/catalog/product_detail.html

- `{% block title %}{{ data.product.name }}{% endblock %}`
- Breadcrumb
- İki sütun Bootstrap row:
  - Sol (col-md-5): ürün görseli (`<img class="img-fluid">`)
  - Sağ (col-md-7):
    - Ürün adı `<h1>`
    - Fiyat `<p class="display-6 text-primary">`
    - Stok: "Stokta Var" / "Stokta Yok" badge
    - Açıklama
    - **Sepete Ekle formu** (aşağıya bakınız)
    - "Kategoriye Dön" linki
- İlgili ürünler: küçük kart grid (4 ürün, `related_products`)

**Sepete Ekle Formu**:
```html
<form method="post" action="{% url 'cart:cart_add' %}">
  {% csrf_token %}
  <input type="hidden" name="product_id" value="{{ data.product.id }}">
  <input type="hidden" name="next" value="{{ request.path }}">
  <div class="input-group mb-3" style="max-width: 200px;">
    <input type="number" name="quantity" value="1" min="1"
           max="{{ data.product.stock }}" class="form-control">
    <button type="submit" class="btn btn-primary"
            {% if not data.product.is_in_stock %}disabled{% endif %}>
      Sepete Ekle
    </button>
  </div>
</form>
```

### templates/catalog/search_results.html

- Arama kutusu (GET formu, `?q=`)
- Sonuç yoksa: "Arama sonucu bulunamadı" mesajı
- `data.products` — ürün liste kartları
- Sayfalama (varsa)

---

## Admin Kaydı (apps/catalog/admin.py)

```python
from django.contrib import admin
from apps.catalog.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_active', 'parent']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_active', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_active', 'category']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock', 'is_active']
```

---

## Catalog İş Kuralları

1. Pasif (`is_active=False`) kategoriler ve ürünler hiçbir public URL'de görünmez
2. Stokta olmayan ürünler listelenir fakat "Sepete Ekle" butonu `disabled`
3. Slug URL'de kullanılır; değiştirilmesi SEO açısından önerilmez
4. Kategori silindiğinde ürünler korunur (`on_delete=PROTECT`)
5. Arama en az 2 karakter gerektirir
