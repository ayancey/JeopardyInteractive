import requests
from pathlib import Path
import time

# Yes this against TOS, no I don't care.

s = requests.session()
s.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
})

jarchive_folder = Path("jarchive_html")

for i in range(1, 8343):
    new_file = jarchive_folder / f"{i}.html"
    if not new_file.is_file():
        print(i)
        r = s.get(f"https://j-archive.com/showgame.php?game_id={i}")
        with open(new_file, "wb") as f:
            f.write(r.content)

        time.sleep(0.25)
