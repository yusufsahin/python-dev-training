import re

from scrapy.exceptions import DropItem


class DedupePipeline:
    """Drop exact duplicate rows (same location + postal code)."""

    def __init__(self):
        self._seen: set[tuple[str, str, str, str, str]] = set()

    def process_item(self, item, spider):
        key = (
            item["il"],
            item["ilce"],
            item["mahalle"],
            item["sokak"],
            item["posta_kodu"],
        )
        if key in self._seen:
            raise DropItem(f"duplicate: {key!r}")
        self._seen.add(key)
        return item


_ws_re = re.compile(r"\s+")


class NormalizePipeline:
    """Trim whitespace in text fields."""

    def process_item(self, item, spider):
        for k in ("il", "ilce", "mahalle", "sokak", "posta_kodu"):
            if item.get(k) is not None:
                v = _ws_re.sub(" ", str(item[k]).strip())
                item[k] = v
        return item
