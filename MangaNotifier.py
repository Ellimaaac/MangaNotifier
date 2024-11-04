import os
import pandas as pd
import datetime
from tkinter import Tk, ttk
import requests
import favorite_manga

def normalize_title(title):
    return title.lower().strip()

favorite_manga_list = [
    "One Piece",
    "My Hero Academia",
    "Black Clover",
]  # Put your favorite manga titles here

normalized_favorite_manga_list = [normalize_title(title) for title in favorite_manga_list]

def display_favorite_manga_updates(favorite_updates):
    root = Tk()
    root.title("Favorite Manga Updates")
    root.geometry("640x400")

    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Treeview.Heading", background="#2E3B4E", foreground="white", font=("Arial", 11, "bold"))
    style.configure("Treeview", background="#1C1C1E", foreground="#E0E0E0", font=("Arial", 10), rowheight=30)

    tree = ttk.Treeview(root, columns=("Title", "New Chapter", "Date", "Website"), show="headings")
    tree.heading("Title", text="Title")
    tree.heading("New Chapter", text="New Chapter")
    tree.heading("Date", text="Date")
    tree.heading("Website", text="Website")

    tree.column("Title", anchor="w", width=220)
    tree.column("New Chapter", anchor="center", width=100)
    tree.column("Date", anchor="center", width=100)
    tree.column("Website", anchor="center", width=100)

    tree.tag_configure('MangaDex', background='#ADD8E6', foreground='black')

    for entry in favorite_updates:
        tree.insert("", "end", values=(entry["Title"], entry["New Chapter"], entry["Date"], entry["Website"]), tags=('MangaDex',))

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(expand=True, fill='both', padx=10, pady=10)

    root.mainloop()

def filter_favorite_manga_updates():
    today_date = datetime.datetime.now().strftime('%Y-%m-%d')
    mangadex_csv = f'manga_data_mangadex_{today_date}.csv'

    favorite_updates = []

    if os.path.exists(mangadex_csv) and os.path.getsize(mangadex_csv) > 0:
        df_mangadex = pd.read_csv(mangadex_csv)
        favorite_updates.extend(df_mangadex[df_mangadex['Title'].str.lower().isin(normalized_favorite_manga_list)].to_dict('records'))
    else:
        print(f"No updates found for MangaDex ({mangadex_csv}).")

    if not favorite_updates:
        print("No favorite manga updates found.")
        return

    display_favorite_manga_updates(favorite_updates)

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