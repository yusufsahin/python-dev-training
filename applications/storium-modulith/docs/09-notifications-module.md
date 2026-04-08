# 09 — Notifications (Bildirim) Modülü

## Kapsam
- E-posta bildirimleri (Django built-in email framework)
- Sipariş oluşturulduğunda müşteriye e-posta
- Sipariş durumu değiştiğinde müşteriye e-posta
- HTML e-posta template'leri
- Development'ta `console` backend (terminale yazar), production'da SMTP

---

## Dosya Yapısı

```
apps/notifications/
├── __init__.py
├── apps.py
└── services.py       ← EmailNotificationService

templates/emails/
├── order_placed_subject.txt
├── order_placed_body.html
├── order_status_subject.txt
└── order_status_body.html
```

---

## EmailNotificationService (apps/notifications/services.py)

```python
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from core.dtos.order_dtos import OrderOutputDTO


class EmailNotificationService:
    """
    Django email framework üzerine kurulu bildirim servisi.
    Development: console backend (terminalde görünür)
    Production: SMTP backend (gerçek e-posta gönderimi)
    """

    FROM_EMAIL = settings.DEFAULT_FROM_EMAIL

    def send_order_placed(self, order: OrderOutputDTO) -> None:
        """
        Sipariş oluşturulduğunda müşteriye gönderilir.
        Tetikleyen: OrderService.create_order()
        """
        user = self._get_user(order.id)
        if not user or not user.email:
            return

        subject = render_to_string(
            'emails/order_placed_subject.txt',
            {'order': order}
        ).strip()

        html_body = render_to_string(
            'emails/order_placed_body.html',
            {'order': order, 'user': user}
        )
        text_body = f"Siparişiniz alındı. Sipariş No: #{order.id}"

        self._send(
            subject=subject,
            text_body=text_body,
            html_body=html_body,
            to_email=user.email,
        )

    def send_order_status_changed(self, order: OrderOutputDTO) -> None:
        """
        Sipariş durumu değiştiğinde müşteriye gönderilir.
        Tetikleyen: OrderService.update_order_status()
        """
        user = self._get_user(order.id)
        if not user or not user.email:
            return

        subject = render_to_string(
            'emails/order_status_subject.txt',
            {'order': order}
        ).strip()

        html_body = render_to_string(
            'emails/order_status_body.html',
            {'order': order, 'user': user}
        )
        text_body = (
            f"Siparişinizin durumu güncellendi. "
            f"Sipariş No: #{order.id} — Yeni Durum: {order.status_display}"
        )

        self._send(
            subject=subject,
            text_body=text_body,
            html_body=html_body,
            to_email=user.email,
        )

    def _send(
        self,
        subject: str,
        text_body: str,
        html_body: str,
        to_email: str,
    ) -> None:
        """
        EmailMultiAlternatives: hem text/plain hem text/html gönderir.
        E-posta istemcileri HTML desteklemiyorsa text_body görünür.
        """
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=self.FROM_EMAIL,
            to=[to_email],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=True)
        # fail_silently=True → e-posta başarısız olursa uygulama çökmez

    def _get_user(self, order_id: int):
        """Order'ın user'ını DB'den alır."""
        from modules.orders.models import Order
        try:
            order = Order.objects.select_related('user').get(pk=order_id)
            return order.user
        except Order.DoesNotExist:
            return None
```

---

## E-posta Template'leri

### templates/emails/order_placed_subject.txt

```
Siparişiniz alındı — #{{ order.id }} | Storium
```

### templates/emails/order_placed_body.html

```html
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: Arial, sans-serif; color: #333; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    .header { background-color: #2c3e50; color: white; padding: 20px; text-align: center; }
    .order-table { width: 100%; border-collapse: collapse; margin: 20px 0; }
    .order-table th, .order-table td { border: 1px solid #ddd; padding: 10px; text-align: left; }
    .order-table th { background-color: #f5f5f5; }
    .total-row { font-weight: bold; background-color: #f9f9f9; }
    .footer { margin-top: 30px; font-size: 12px; color: #777; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Storium</h1>
      <p>Siparişiniz Alındı!</p>
    </div>

    <p>Merhaba {{ user.get_full_name|default:user.username }},</p>
    <p>
      <strong>#{{ order.id }}</strong> numaralı siparişiniz başarıyla oluşturuldu.
      Siparişiniz en kısa sürede hazırlanacaktır.
    </p>

    <h3>Sipariş Özeti</h3>
    <table class="order-table">
      <thead>
        <tr>
          <th>Ürün</th>
          <th>Adet</th>
          <th>Birim Fiyat</th>
          <th>Ara Toplam</th>
        </tr>
      </thead>
      <tbody>
        {% for item in order.items %}
        <tr>
          <td>{{ item.product_name }}</td>
          <td>{{ item.quantity }}</td>
          <td>₺{{ item.unit_price }}</td>
          <td>₺{{ item.line_total }}</td>
        </tr>
        {% endfor %}
        <tr class="total-row">
          <td colspan="3">Genel Toplam</td>
          <td>₺{{ order.total_price }}</td>
        </tr>
      </tbody>
    </table>

    <h3>Teslimat Adresi</h3>
    <p>
      {{ order.shipping_name }}<br>
      {{ order.shipping_address }}<br>
      {{ order.shipping_city }}<br>
      {% if order.shipping_phone %}Tel: {{ order.shipping_phone }}{% endif %}
    </p>

    <div class="footer">
      <p>Bu e-posta otomatik olarak gönderilmiştir. Lütfen yanıtlamayınız.</p>
      <p>Storium — storium.example.com</p>
    </div>
  </div>
</body>
</html>
```

### templates/emails/order_status_subject.txt

```
Sipariş Durumu Güncellendi — #{{ order.id }} | Storium
```

### templates/emails/order_status_body.html

```html
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <style>
    /* Aynı stil bloğu order_placed_body.html ile aynı */
    body { font-family: Arial, sans-serif; color: #333; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    .header { background-color: #2c3e50; color: white; padding: 20px; text-align: center; }
    .status-badge { display: inline-block; padding: 6px 14px; border-radius: 4px;
                    font-weight: bold; background-color: #27ae60; color: white; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Storium</h1>
      <p>Sipariş Durumu Güncellendi</p>
    </div>

    <p>Merhaba {{ user.get_full_name|default:user.username }},</p>
    <p>
      <strong>#{{ order.id }}</strong> numaralı siparişinizin durumu güncellendi:
    </p>

    <p style="font-size: 18px;">
      Yeni Durum: <span class="status-badge">{{ order.status_display }}</span>
    </p>

    {% if order.status == 'shipped' %}
    <p>Siparişiniz kargoya verilmiştir. Yakında teslim edilecektir.</p>
    {% elif order.status == 'delivered' %}
    <p>Siparişiniz teslim edilmiştir. İyi günler dileriz!</p>
    {% elif order.status == 'cancelled' %}
    <p>Siparişiniz iptal edilmiştir. Ödeme iadesi için bizimle iletişime geçiniz.</p>
    {% endif %}

    <div style="margin-top: 20px; font-size: 12px; color: #777;">
      <p>Bu e-posta otomatik olarak gönderilmiştir. Lütfen yanıtlamayınız.</p>
    </div>
  </div>
</body>
</html>
```

---

## Settings Konfigürasyonu

### Development (storium/settings/development.py)
```python
# E-postalar terminale yazdırılır (gerçek e-posta gönderilmez)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@storium.local'
```

### Production (storium/settings/production.py)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')              # örn: smtp.gmail.com
EMAIL_PORT = env.int('EMAIL_PORT', 587)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', 'noreply@storium.com')
```

---

## Genişletme Notları (İlerideki Geliştirmeler)

Bu versiyonda e-postalar **senkron** gönderilir (sipariş kaydıyla aynı request döngüsünde).

İleride asenkron yapmak için:
- `Celery` + `Redis` ile task queue eklenebilir
- `send_order_placed` → `send_order_placed_task.delay(order.id)` çağrısına dönüştürülür
- Bu değişiklik sadece `EmailNotificationService`'i etkiler; diğer katmanlar değişmez

Ek bildirim türleri eklenebilir:
- SMS (Twilio, Netgsm)
- Push notification
- Slack webhook (admin bildirimi)
Bunlar `EmailNotificationService` ile aynı interface'i uygulayan ayrı servis sınıfları olarak eklenebilir.
