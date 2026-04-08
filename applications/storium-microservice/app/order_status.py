ORDER_STATUS_LABELS = {
    "pending": "Beklemede",
    "confirmed": "Onaylandı",
    "shipped": "Kargoya Verildi",
    "delivered": "Teslim Edildi",
    "cancelled": "İptal Edildi",
}


def status_display(status: str) -> str:
    return ORDER_STATUS_LABELS.get(status, status)
