 import requests, json, re
  from datetime import datetime
  from typing import List, Dict, Optional
  from dataclasses import dataclass, asdict

  @dataclass
  class Product:
      id: int
      title: str
      brand: str
      price: float
      currency: str
      url: str
      size: Optional[str] = None
      condition: Optional[str] = None
      created_at: str = ""
      photo_url: Optional[str] = None

  class VintedScraper:
      def __init__(self, timeout=15):
          self.session = requests.Session()
          self.session.headers.update({
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) 
  Chrome/120.0.0.0 Safari/537.36",
              "Accept": "application/json, text/plain, */*",
          })
          self.timeout = timeout

      def search_products(self, query: str) -> List[Product]:
          params = {"query": query, "price_from": 15, "price_to": 20, "search": "items", "sort": "relevancy", "page": 1,
  "per_page": 40}
          try:
              resp = self.session.get("https://www.vinted.it/catalog", params=params, timeout=self.timeout)
              resp.raise_for_status()
              return self._parse(resp.text)
          except Exception as e:
              print(f"Errore: {e}")
              return []

      def _parse(self, html: str) -> List[Product]:
          products = []
          for key in ["__NEXT_DATA__", "__INITIAL_STATE__"]:
              m = re.search(rf'<script id="{key}">([^<]+)</script>', html, re.DOTALL)
              if m:
                  try:
                      data = json.loads(m.group(1))
                      items = self._extract_items(data)
                      for i in items[:30]:
                          if isinstance(i, dict):
                              p = i.get("price", {})
                              products.append(Product(
                                  id=int(i.get("id", 0)),
                                  title=str(i.get("title", "")),
                                  brand=str(i.get("brand", {}).get("name", "Sconosciuto")),
                                  price=float(p.get("value", 0)) if isinstance(p, dict) else 0.0,
                                  currency=p.get("currency", "EUR") if isinstance(p, dict) else "EUR",
                                  url=i.get("link", "") if i.get("link", "").startswith("http") else
  f"https://www.vinted.it{i.get('link', '')}"
                              ))
                      if products:
                          return products
                  except:
                      pass
          return products

      def _extract_items(self, data):
          for path in [["props", "pageProps", "catalog", "items"], ["catalog", "items"], ["items"]]:
              r = data
              for k in path:
                  if isinstance(r, dict) and k in r:
                      r = r[k]
                  else:
                      r = None
                      break
              if isinstance(r, list):
                  return r
          return []

      def search_all(self):
          queries = {"Timberland": "timberland", "Philippe Model Temple": "philippe model temple", "Valentino Untiled":
  "valentino unttiled"}
          return {name: self.search_products(q) for name, q in queries.items()}

  if __name__ == "__main__":
      s = VintedScraper()
      r = s.search_all()
      for n, p in r.items():
          print(f"{n}: {len(p)} prodotti")
