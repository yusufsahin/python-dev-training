from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from core.dtos.order_dtos import OrderOutputDTO


class EmailNotificationService:
    FROM_EMAIL = settings.DEFAULT_FROM_EMAIL

    def send_order_placed(self, order: OrderOutputDTO) -> None:
        user = self._get_user(order.id)
        if not user or not user.email:
            return

        subject = render_to_string(
            "emails/order_placed_subject.txt",
            {"order": order},
        ).strip()

        html_body = render_to_string(
            "emails/order_placed_body.html",
            {"order": order, "user": user},
        )
        text_body = f"Siparişiniz alındı. Sipariş No: #{order.id}"

        self._send(
            subject=subject,
            text_body=text_body,
            html_body=html_body,
            to_email=user.email,
        )

    def send_order_status_changed(self, order: OrderOutputDTO) -> None:
        user = self._get_user(order.id)
        if not user or not user.email:
            return

        subject = render_to_string(
            "emails/order_status_subject.txt",
            {"order": order},
        ).strip()

        html_body = render_to_string(
            "emails/order_status_body.html",
            {"order": order, "user": user},
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
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=self.FROM_EMAIL,
            to=[to_email],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=True)

    def _get_user(self, order_id: int):
        from modules.orders.models import Order

        try:
            order = Order.objects.select_related("user").get(pk=order_id)
            return order.user
        except Order.DoesNotExist:
            return None
