BOT_NAME = "postalcode_crawler"

SPIDER_MODULES = ["postalcode_crawler.spiders"]
NEWSPIDER_MODULE = "postalcode_crawler.spiders"

ROBOTSTXT_OBEY = True

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

DEFAULT_REQUEST_HEADERS = {
    "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8",
    "Accept": "application/json, text/html;q=0.9,*/*;q=0.8",
}

DOWNLOAD_DELAY = 0.75
RANDOMIZE_DOWNLOAD_DELAY = True
CONCURRENT_REQUESTS = 8
CONCURRENT_REQUESTS_PER_DOMAIN = 4

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"

LOG_LEVEL = "INFO"
TELNETCONSOLE_ENABLED = False

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

ITEM_PIPELINES = {
    "postalcode_crawler.pipelines.DedupePipeline": 100,
    "postalcode_crawler.pipelines.NormalizePipeline": 200,
}

# Optional default output when not using -o (uncomment to enable)
# FEEDS = {
#     "posta_kodlari.jsonl": {"format": "jsonlines", "overwrite": True},
# }
