from datetime import datetime
from flask import Flask, render_template, request
import pandas as pd
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


def scrape_bahrain_deals():
  # Simulated mock data representing scraped items from Bahrain retail outlets
  # In production, BeautifulSoup parses live HTML tags from Lulu, Carrefour, and Nesto
  data = [
      {
          "product": "Basmati Rice 5kg",
          "store": "Lulu",
          "price": 3.200,
          "date": "2026-11-17",
      },
      {
          "product": "Basmati Rice 5kg",
          "store": "Carrefour",
          "price": 3.400,
          "date": "2026-11-17",
      },
      {
          "product": "Basmati Rice 5kg",
          "store": "Nesto",
          "price": 2.900,
          "date": "2026-11-17",
      },
      {
          "product": "Alokazay Tea 100s",
          "store": "Lulu",
          "price": 1.100,
          "date": "2026-11-17",
      },
      {
          "product": "Alokazay Tea 100s",
          "store": "Carrefour",
          "price": 1.250,
          "date": "2026-11-17",
      },
      {
          "product": "Alokazay Tea 100s",
          "store": "Nesto",
          "price": 1.000,
          "date": "2026-11-17",
      },
      {
          "product": "Fresh Chicken 1kg",
          "store": "Lulu",
          "price": 1.300,
          "date": "2026-11-17",
      },
      {
          "product": "Fresh Chicken 1kg",
          "store": "Carrefour",
          "price": 1.400,
          "date": "2026-11-17",
      },
      {
          "product": "Fresh Chicken 1kg",
          "store": "Nesto",
          "price": 1.150,
          "date": "2026-11-17",
      },
  ]

  df = pd.DataFrame(data)
  return df


@app.route("/", methods=["GET", "POST"])
def index():
  df = scrape_bahrain_deals()

  # Handle search query filtering
  search_query = request.form.get("query", "")
  if search_query:
    df = df[df["product"].str.contains(search_query, case=False, na=False)]

  # Find best offers (minimum price per product using Pandas)
  best_offers = df.loc[df.groupby("product")["price"].idxmin()]

  # Convert dataframes to dictionaries for HTML rendering
  raw_records = df.to_dict(orient="records")
  best_records = best_offers.to_dict(orient="records")

  return render_template(
      "index.html",
      deals=raw_records,
      best_deals=best_records,
      query=search_query,
      current_time=datetime.now().strftime("%Y-%m-%d %H:%M"),
  )


if __name__ == "__main__":
  app.run(debug=True, port=5000)