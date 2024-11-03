import requests
import pandas as pd
import tkinter as tk
from tkinter import ttk
import os
import datetime

def normalize_title(title):
    return title.lower().strip()

favorite_manga_list = [
    "One Piece",
    "My Hero Academia",
    "Black Clover",
]# Put your favorite manga titles here

normalized_favorite_manga_list = [normalize_title(title) for title in favorite_manga_list]

def display_manga_updates(favorite_updates):
    root = tk.Tk()
    root.title("Favorite Manga Updates")
    root.geometry("640x400")

    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Treeview.Heading", background="#2E3B4E", foreground="white", font=("Arial", 11, "bold"))
    style.configure("Treeview", background="#1C1C1E", foreground="#E0E0E0", font=("Arial", 10), rowheight=30)

    tree = ttk.Treeview(root, columns=("Title", "New Chapter", "Date", "Website"), show='headings')
    tree.heading("Title", text="Title")
    tree.heading("New Chapter", text="New Chapter")
    tree.heading("Date", text="Date")
    tree.heading("Website", text="Website")

    tree.column("Title", anchor="w", width=220)
    tree.column("New Chapter", anchor="center", width=100)
    tree.column("Date", anchor="center", width=100)
    tree.column("Website", anchor="center", width=100)

    tree.tag_configure('MangaFreak', background='#D3D3D3', foreground='black')
    tree.tag_configure('MangaDex', background='#ADD8E6', foreground='black')

    for entry in favorite_updates:
        website_tag = 'MangaFreak' if entry["Website"] == 'MangaFreak' else 'MangaDex'
        tree.insert("", "end", values=(entry["Title"], entry["New Chapter"], entry["Date"], entry["Website"]), tags=(website_tag,))

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(expand=True, fill='both', padx=10, pady=10)

    root.mainloop()

def filter_favorite_manga_updates():
    today_date = datetime.datetime.now().strftime('%Y-%m-%d')
    mangafreak_csv = f'manga_data_mangafreak_{today_date}.csv'
    mangadex_csv = f'manga_data_mangadex_{today_date}.csv'

    favorite_updates = []

    if os.path.exists(mangafreak_csv):
        df_mangafreak = pd.read_csv(mangafreak_csv)
        df_mangafreak = df_mangafreak[df_mangafreak['Title'].apply(lambda x: normalize_title(x) in normalized_favorite_manga_list)]
        favorite_updates.extend(df_mangafreak.to_dict(orient='records'))

    if os.path.exists(mangadex_csv):
        df_mangadex = pd.read_csv(mangadex_csv)
        df_mangadex = df_mangadex[df_mangadex['Title'].apply(lambda x: normalize_title(x) in normalized_favorite_manga_list)]
        favorite_updates.extend(df_mangadex.to_dict(orient='records'))

    favorite_updates.sort(key=lambda x: (x['Website'], x['Title']))

    display_manga_updates(favorite_updates)

def download_csv_files():
    base_url = "https://raw.githubusercontent.com/Ellimaaac/MangaNotifier/main/dB/"
    today_date = datetime.datetime.now().strftime('%Y-%m-%d')
    mangadex_csv = f'manga_data_mangadex_{today_date}.csv'

    for csv_file in [mangadex_csv]:
        url = base_url + csv_file
        response = requests.get(url)
        if response.status_code == 200:
            with open(csv_file, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {csv_file}")
        else:
            print(f"Failed to download {csv_file}")

download_csv_files()
filter_favorite_manga_updates()