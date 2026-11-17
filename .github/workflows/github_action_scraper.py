#!/usr/bin/env python3
  import asyncio, logging, json
  from datetime import datetime
  from telegram import Bot
  from scrapper import VintedScraper
  from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, PRICE_MIN, PRICE_MAX

  logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
  logger = logging.getLogger(__name__)

  async def run():
      if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
          print("Configura i Secrets: TELEGRAM_TOKEN, TELEGRAM_CHAT_ID")
          return
      chat_id = int(TELEGRAM_CHAT_ID)
      scraper = VintedScraper()
      results = scraper.search_all()
      data = {"timestamp": datetime.now().isoformat(), "products": {n: [p.__dict__ for p in ps] for n, ps in
  results.items()}}
      open("products.json", "w").write(json.dumps(data, indent=2))
      bot = Bot(TELEGRAM_TOKEN)
      for name, products in results.items():
          for p in products:
              await bot.send_message(chat_id, f"<b>{p.title}</b>\n€{p.price} - <a href='{p.url}'>Vai</a>",
  parse_mode="HTML")

  if __name__ == "__main__":
      asyncio.run(run())
