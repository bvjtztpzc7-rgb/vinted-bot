  import os
  BASE_URL = "https://www.vinted.it"
  SEARCH_URL = f"{BASE_URL}/catalog"
  PRODUCTS = [
      {"name": "Timberland", "search_query": "timberland"},
      {"name": "Philippe Model Temple", "search_query": "philippe model temple"},
      {"name": "Valentino Untiled", "search_query": "valentino unttiled"}
  ]
  PRICE_MIN = 15
  PRICE_MAX = 20
  TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
  TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
  SCHEDULE_HOURS = [9, 18]
  HEADERS = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 
  Safari/537.36",
      "Accept": "application/json, text/plain, */*",
      "Accept-Language": "it-IT,it,en-US;q=0.9,en;q=0.8",
      "Referer": BASE_URL,
  }
