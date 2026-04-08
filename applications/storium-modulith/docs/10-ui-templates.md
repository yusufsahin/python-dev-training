# 10 — UI Templates (Bootstrap 5)

## Genel Prensipler
- Bootstrap 5.3 CDN üzerinden yüklenir (yerel paket gerekmez)
- Django template inheritance: `base.html` → tüm sayfalar
- Django `messages` framework için `_messages.html` partial
- Responsive tasarım: mobile-first
- Türkçe içerik

---

## Base Template (templates/base.html)

```html
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}Storium{% endblock %}</title>
  <!-- Bootstrap 5.3 CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <!-- Bootstrap Icons -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
  <!-- Custom CSS -->
  {% load static %}
  <link rel="stylesheet" href="{% static 'css/storium.css' %}">
  {% block extra_head %}{% endblock %}
</head>
<body>
  {% include 'partials/_navbar.html' %}

  <!-- Mobil: navbar’daki “Kategoriler” → offcanvas-start #categoryOffcanvas, içinde _category_sidebar.html -->

  <main class="container my-4">
    {% include 'partials/_messages.html' %}
    <div class="row g-4">
      <aside class="col-lg-3 d-none d-lg-block">
        <div class="category-sidebar sticky-top">
          {% include 'partials/_category_sidebar.html' %}
        </div>
      </aside>
      <div class="col-12 col-lg-9">
        {% block content %}{% endblock %}
      </div>
    </div>
  </main>

  {% include 'partials/_footer.html' %}

  <!-- Bootstrap 5.3 JS Bundle (Popper dahil) -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
  {% load static %}
  <script src="{% static 'js/storium.js' %}"></script>
  {% block extra_js %}{% endblock %}
</body>
</html>
```

---

## Partials

### templates/partials/_category_sidebar.html

`catalog_nav` ve `catalog_nav_active_slug` (context processor + ürün detayında override) ile kök ve alt kategori linklerini dikey `nav` olarak çizer. Masaüstünde `base.html` sol sütununda, mobilde aynı partial `offcanvas` içinde tekrar kullanılır. Stil: `static/css/storium.css` içinde `.category-sidebar`.

### templates/partials/_navbar.html

```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top">
  <div class="container">
    <!-- Logo / Marka -->
    <a class="navbar-brand fw-bold" href="{% url 'catalog:home' %}">
      <i class="bi bi-shop"></i> Storium
    </a>

    <!-- Hamburger butonu (mobil) -->
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
            data-bs-target="#navbarMain">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarMain">
      <!-- Arama formu (ortada) -->
      <form class="d-flex mx-auto" style="max-width: 400px;"
            method="get" action="{% url 'catalog:product_search' %}">
        <input class="form-control me-2" type="search" name="q"
               placeholder="Ürün ara..." value="{{ request.GET.q|default:'' }}">
        <button class="btn btn-outline-light" type="submit">
          <i class="bi bi-search"></i>
        </button>
      </form>

      <!-- Sağ taraf linkleri -->
      <ul class="navbar-nav ms-auto">
        <!-- Sepet -->
        <li class="nav-item">
          <a class="nav-link" href="{% url 'cart:cart_detail' %}">
            <i class="bi bi-cart3"></i> Sepet
            {% if cart_item_count > 0 %}
              <span class="badge bg-danger rounded-pill">{{ cart_item_count }}</span>
            {% endif %}
          </a>
        </li>
        <!-- Kullanıcı -->
        {% if user.is_authenticated %}
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown">
              <i class="bi bi-person-circle"></i> {{ user.username }}
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
              <li><a class="dropdown-item" href="{% url 'orders:order_list' %}">
                <i class="bi bi-bag-check"></i> Siparişlerim
              </a></li>
              {% if user.is_staff %}
              <li><a class="dropdown-item" href="{% url 'admin:index' %}">
                <i class="bi bi-gear"></i> Admin
              </a></li>
              {% endif %}
              <li><hr class="dropdown-divider"></li>
              <li>
                <form method="post" action="{% url 'logout' %}">
                  {% csrf_token %}
                  <button class="dropdown-item text-danger" type="submit">
                    <i class="bi bi-box-arrow-right"></i> Çıkış Yap
                  </button>
                </form>
              </li>
            </ul>
          </li>
        {% else %}
          <li class="nav-item">
            <a class="nav-link" href="{% url 'login' %}">
              <i class="bi bi-person"></i> Giriş Yap
            </a>
          </li>
        {% endif %}
      </ul>
    </div>
  </div>
</nav>
```

### templates/partials/_footer.html

```html
<footer class="bg-dark text-light mt-5 py-4">
  <div class="container">
    <div class="row">
      <div class="col-md-4">
        <h5><i class="bi bi-shop"></i> Storium</h5>
        <p class="text-muted small">Kaliteli ürünler, uygun fiyatlarla.</p>
      </div>
      <div class="col-md-4">
        <h6>Kategoriler</h6>
        <ul class="list-unstyled small">
          <!-- Dinamik olarak context processor ile ya da statik linkler -->
        </ul>
      </div>
      <div class="col-md-4">
        <h6>Müşteri Hizmetleri</h6>
        <ul class="list-unstyled small">
          <li><a href="#" class="text-muted text-decoration-none">İletişim</a></li>
          <li><a href="#" class="text-muted text-decoration-none">Gizlilik Politikası</a></li>
          <li><a href="#" class="text-muted text-decoration-none">İade Koşulları</a></li>
        </ul>
      </div>
    </div>
    <hr class="border-secondary">
    <p class="text-center text-muted small mb-0">
      &copy; {% now "Y" %} Storium. Tüm hakları saklıdır.
    </p>
  </div>
</footer>
```

### templates/partials/_messages.html

```html
{% if messages %}
  {% for message in messages %}
    <div class="alert alert-{{ message.tags|default:'info' }} alert-dismissible fade show" role="alert">
      {{ message }}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>
  {% endfor %}
{% endif %}
```

Django mesaj tag → Bootstrap class eşleşmesi (`settings.py`'de ayarlanacak):
```python
from django.contrib.messages import constants as messages_constants
MESSAGE_TAGS = {
    messages_constants.DEBUG:   'secondary',
    messages_constants.INFO:    'info',
    messages_constants.SUCCESS: 'success',
    messages_constants.WARNING: 'warning',
    messages_constants.ERROR:   'danger',
}
```

### templates/partials/_breadcrumb.html

```html
{% if breadcrumb %}
  <nav aria-label="breadcrumb">
    <ol class="breadcrumb">
      <li class="breadcrumb-item"><a href="{% url 'catalog:home' %}">Ana Sayfa</a></li>
      {% for crumb in breadcrumb %}
        {% if forloop.last %}
          <li class="breadcrumb-item active" aria-current="page">{{ crumb.name }}</li>
        {% else %}
          <li class="breadcrumb-item"><a href="{{ crumb.url }}">{{ crumb.name }}</a></li>
        {% endif %}
      {% endfor %}
    </ol>
  </nav>
{% endif %}
```

### templates/partials/_pagination.html

```html
{% if data.total_pages > 1 %}
  <nav aria-label="Sayfalama" class="mt-4">
    <ul class="pagination justify-content-center">
      {% if data.page > 1 %}
        <li class="page-item">
          <a class="page-link" href="?page={{ data.page|add:'-1' }}">
            <i class="bi bi-chevron-left"></i>
          </a>
        </li>
      {% endif %}

      {% for i in data.total_pages|make_list %}
        <li class="page-item {% if forloop.counter == data.page %}active{% endif %}">
          <a class="page-link" href="?page={{ forloop.counter }}">{{ forloop.counter }}</a>
        </li>
      {% endfor %}

      {% if data.page < data.total_pages %}
        <li class="page-item">
          <a class="page-link" href="?page={{ data.page|add:'1' }}">
            <i class="bi bi-chevron-right"></i>
          </a>
        </li>
      {% endif %}
    </ul>
  </nav>
{% endif %}
```

> **Not**: `make_list` filter sayı üzerinde çalışmaz. Gerçek implementasyonda
> `range(1, total_pages+1)` context'e eklenmelidir ya da custom template tag yazılır.

---

## Renk Paleti ve Custom CSS (static/css/storium.css)

```css
/* Storium marka renkleri */
:root {
  --storium-primary: #2c3e50;
  --storium-accent: #e74c3c;
  --storium-light: #ecf0f1;
}

/* Ürün kartı hover efekti */
.product-card {
  transition: transform 0.2s, box-shadow 0.2s;
}
.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

/* Fiyat gösterimi */
.price-display {
  color: var(--storium-accent);
  font-weight: 700;
}

/* Sepet badge */
.cart-badge {
  font-size: 0.65rem;
}
```

---

## Ürün Kart Bileşeni (Tekrar Kullanılabilir)

Tüm sayfalarda aynı ürün kartı kullanılır. Bir partial oluşturulabilir:

### templates/partials/_product_card.html

```html
<div class="col-lg-3 col-md-4 col-sm-6 mb-4">
  <div class="card h-100 product-card">
    {% if product.image_url %}
      <img src="{{ product.image_url }}" class="card-img-top" alt="{{ product.name }}"
           style="height: 200px; object-fit: cover;">
    {% else %}
      <div class="bg-light d-flex align-items-center justify-content-center"
           style="height: 200px;">
        <i class="bi bi-image text-muted" style="font-size: 3rem;"></i>
      </div>
    {% endif %}
    <div class="card-body d-flex flex-column">
      <h6 class="card-title">{{ product.name }}</h6>
      <p class="card-text text-muted small flex-grow-1">
        {{ product.description|truncatewords:15 }}
      </p>
      <div class="d-flex justify-content-between align-items-center mt-2">
        <span class="price-display fs-5">₺{{ product.price }}</span>
        {% if product.is_in_stock %}
          <span class="badge bg-success">Stokta Var</span>
        {% else %}
          <span class="badge bg-danger">Stokta Yok</span>
        {% endif %}
      </div>
    </div>
    <div class="card-footer bg-transparent">
      <a href="{% url 'catalog:product_detail' slug=product.slug %}"
         class="btn btn-outline-primary btn-sm w-100">
        <i class="bi bi-eye"></i> İncele
      </a>
    </div>
  </div>
</div>
```

Kullanım: `{% include 'partials/_product_card.html' with product=p %}`

---

## Auth Template'leri (Django built-in)

Django'nun yerleşik auth view'ları `registration/` prefix'li template'leri arar:

```
templates/registration/
├── login.html          ← Bootstrap login formu
├── logout.html         ← "Çıkış yapıldı" sayfası (opsiyonel)
└── password_change_form.html  ← opsiyonel
```

`settings.py`'de yönlendirmeler:
```python
LOGIN_URL = '/giris/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
```

`storium/urls.py`'de:
```python
path('giris/', auth_views.LoginView.as_view(), name='login'),
path('cikis/', auth_views.LogoutView.as_view(), name='logout'),
```
