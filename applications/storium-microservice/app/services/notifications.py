import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config import get_settings
from app.order_status import status_display
from app.repositories import user_repo
from app.schemas.order import OrderOutputDTO
from sqlalchemy.orm import Session


class EmailNotificationService:
    def __init__(self, db: Session):
        self._db = db

    def send_order_placed(self, order: OrderOutputDTO) -> None:
        user = user_repo.user_get_by_id(self._db, self._user_id_for_order(order.id))
        if not user or not user.email:
            return
        subject = f"Siparişiniz alındı — #{order.id}"
        html = f"<p>Sipariş No: #{order.id}</p><p>Toplam: {order.total_price} ₺</p>"
        text = f"Siparişiniz alındı. Sipariş No: #{order.id}"
        self._send(subject, text, html, user.email)

    def send_order_status_changed(self, order: OrderOutputDTO) -> None:
        user = user_repo.user_get_by_id(self._db, self._user_id_for_order(order.id))
        if not user or not user.email:
            return
        disp = order.status_display or status_display(order.status)
        subject = f"Sipariş durumu güncellendi — #{order.id}"
        html = f"<p>Sipariş No: #{order.id}</p><p>Yeni durum: {disp}</p>"
        text = f"Sipariş No: #{order.id} — Yeni durum: {disp}"
        self._send(subject, text, html, user.email)

    def _user_id_for_order(self, order_id: int) -> int:
        from sqlalchemy import select
        from app.models import Order

        oid = self._db.scalar(select(Order.user_id).where(Order.id == order_id))
        return int(oid or 0)

    def _send(self, subject: str, text_body: str, html_body: str, to_email: str) -> None:
        settings = get_settings()
        if not settings.smtp_host:
            return
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.default_from_email
        msg["To"] = to_email
        msg.attach(MIMEText(text_body, "plain", "utf-8"))
        msg.attach(MIMEText(html_body, "html", "utf-8"))
        try:
            with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                if settings.smtp_user:
                    server.starttls()
                    server.login(settings.smtp_user, settings.smtp_password)
                server.sendmail(settings.default_from_email, [to_email], msg.as_string())
        except OSError:
            pass
