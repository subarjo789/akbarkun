import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import os  # ← IMPORT UNTUK MEMBUAT FOLDER
from datetime import datetime

def scrape_books():
    """Scraping data buku dari books.toscrape.com"""
    
    base_url = "https://books.toscrape.com/"
    response = requests.get(base_url)
    
    if response.status_code != 200:
        print(f"Gagal mengambil data: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    books_data = []
    
    # Ambil semua buku
    books = soup.find_all('article', class_='product_pod')
    
    for idx, book in enumerate(books, 1):
        # Judul buku
        title = book.h3.a['title']
        
        # Harga
        price = book.find('p', class_='price_color').text
        
        # Rating (dari class star-rating)
        rating_class = book.find('p', class_='star-rating')['class'][1]
        rating_map = {
            'One': 1, 'Two': 2, 'Three': 3, 
            'Four': 4, 'Five': 5
        }
        rating = rating_map.get(rating_class, 0)
        
        # Ketersediaan stok
        stock = book.find('p', class_='instock availability').text.strip()
        
        books_data.append({
            'no': idx,
            'judul': title,
            'harga': price,
            'rating': rating,
            'stok': stock,
            'waktu_scraping': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        print(f"✓ Berhasil mengambil: {title}")
        time.sleep(0.1)  # Jeda agar tidak terlalu cepat
    
    return books_data

def save_to_json(data, filename='hasil/books.json'):
    """Menyimpan data ke file JSON"""
    # Buat folder jika belum ada
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Data disimpan ke {filename}")

def save_to_csv(data, filename='hasil/books.csv'):
    """Menyimpan data ke file CSV"""
    if not data:
        print("Tidak ada data untuk disimpan")
        return
    
    # Buat folder jika belum ada
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"✅ Data disimpan ke {filename}")

def main():
    print("🚀 Memulai web scraping...")
    print("-" * 40)
    
    # Scraping data
    books = scrape_books()
    
    if books:
        print(f"\n📊 Total buku yang diambil: {len(books)}")
        
        # Simpan ke file
        save_to_json(books)
        save_to_csv(books)
        
        print("\n✨ Scraping selesai!")
        print("\n📋 Preview data (3 buku pertama):")
        print("-" * 40)
        for book in books[:3]:
            print(f"📖 {book['judul']}")
            print(f"   Harga: {book['harga']} | Rating: {book['rating']}⭐\n")
    else:
        print("❌ Gagal mengambil data")

if __name__ == "__main__":
    main()