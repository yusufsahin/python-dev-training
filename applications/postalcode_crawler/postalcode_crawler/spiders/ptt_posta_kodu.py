from __future__ import annotations

import json
import logging
import re
from typing import Any

import scrapy
from scrapy.http import JsonRequest

from postalcode_crawler.items import PostalCodeItem

logger = logging.getLogger(__name__)

NEXT_DATA_RE = re.compile(
    r'<script id="__NEXT_DATA__"[^>]*>(?P<json>.*?)</script>',
    re.DOTALL,
)

API_URL = "https://www.ptt.gov.tr/api/posta-kodu"
PAGE_URL = "https://www.ptt.gov.tr/posta-kodu"

API_HEADERS = {
    "Content-Type": "application/json",
    "Referer": PAGE_URL,
    "Origin": "https://www.ptt.gov.tr",
}


class PttPostaKoduSpider(scrapy.Spider):
    name = "ptt_posta_kodu"
    allowed_domains = ["ptt.gov.tr", "www.ptt.gov.tr"]

    custom_settings = {
        "DOWNLOAD_DELAY": 0.75,
    }

    def __init__(self, max_il=None, max_ilce=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_il = int(max_il) if max_il else None
        self.max_ilce = int(max_ilce) if max_ilce else None

    def start_requests(self):
        yield scrapy.Request(PAGE_URL, callback=self.parse_index, dont_filter=True)

    def parse_index(self, response: scrapy.http.Response):
        m = NEXT_DATA_RE.search(response.text)
        if not m:
            logger.error("__NEXT_DATA__ not found on %s", response.url)
            return

        try:
            data = json.loads(m.group("json"))
        except json.JSONDecodeError as e:
            logger.error("Invalid __NEXT_DATA__ JSON: %s", e)
            return

        iller = (data.get("props") or {}).get("pageProps", {}).get("illerData") or []
        if not iller:
            logger.error("illerData missing or empty")
            return

        if self.max_il is not None:
            iller = iller[: self.max_il]

        for il in iller:
            kod = il.get("kod")
            ad = (il.get("ad") or "").strip()
            if kod is None or not ad:
                continue
            yield JsonRequest(
                url=API_URL,
                data={"action": "ilceler", "il_kodu": str(kod)},
                callback=self.parse_ilceler,
                errback=self._api_errback,
                headers=API_HEADERS,
                cb_kwargs={"il_ad": ad, "il_kod": str(kod)},
            )

    def parse_ilceler(self, response: scrapy.http.Response, il_ad: str, il_kod: str):
        ilceler = self._load_json_array(response)
        if ilceler is None:
            logger.warning("ilceler failed for il=%s (%s): %s", il_ad, il_kod, response.text[:200])
            return

        count = 0
        for row in ilceler:
            if not isinstance(row, dict):
                continue
            k = row.get("kod")
            ad = (row.get("ad") or "").strip()
            if k is None or k <= 0 or not ad:
                continue
            if self.max_ilce is not None and count >= self.max_ilce:
                break
            count += 1
            yield JsonRequest(
                url=API_URL,
                data={
                    "action": "postakodu",
                    "il_kodu": il_kod,
                    "ilce_kodu": str(k),
                },
                callback=self.parse_postakodu,
                errback=self._api_errback,
                headers=API_HEADERS,
                cb_kwargs={"il_ad": il_ad, "ilce_ad": ad},
            )

    def parse_postakodu(self, response: scrapy.http.Response, il_ad: str, ilce_ad: str):
        rows = self._load_json_array(response)
        if rows is None:
            logger.warning(
                "postakodu failed for %s / %s: %s",
                il_ad,
                ilce_ad,
                response.text[:200],
            )
            return

        for row in rows:
            if not isinstance(row, dict):
                continue
            pk = row.get("posta_Kodu")
            if pk is None:
                continue
            yield PostalCodeItem(
                il=il_ad,
                ilce=ilce_ad,
                mahalle=(row.get("mahalleAdi") or "").strip(),
                sokak=(row.get("sokakAdi") or "").strip(),
                posta_kodu=str(pk).strip(),
            )

    def _load_json_array(self, response: scrapy.http.Response) -> list[Any] | None:
        try:
            body = response.text.strip()
            if not body:
                return None
            data = json.loads(body)
        except json.JSONDecodeError:
            return None
        if isinstance(data, dict) and data.get("error"):
            return None
        if isinstance(data, list):
            return data
        return None

    def _api_errback(self, failure):
        logger.error("API request failed: %s", failure.value)
