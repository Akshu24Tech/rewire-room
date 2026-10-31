import urllib.request
import urllib.parse
import json
import os
from pathlib import Path

DEST = Path("assets/avatars")
DEST.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) RewireRoom/1.0"}

def get_wiki_thumb(page_title):
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(page_title)}&prop=pageimages&format=json&pithumbsize=600"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
        pages = data.get("query", {}).get("pages", {})
        for pid in pages:
            if "thumbnail" in pages[pid]:
                return pages[pid]["thumbnail"]["source"]
    return None

def download_file(url, out_path):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp, open(out_path, "wb") as out:
        out.write(resp.read())
    print(f"Downloaded {out_path} ({os.path.getsize(out_path)} bytes)")

sources = {
    "galloway": ("wiki", "Scott Galloway (professor)"),
    "greene": ("wiki", "Robert Greene (American author)"),
    "huberman": ("wiki", "Andrew Huberman"),
    "grant": ("wiki", "Adam Grant"),
    "yousef": ("direct", "https://haas.berkeley.edu/wp-content/uploads/SaharYousef_Headshot-600x600.jpg"),
    "kukushkin": ("direct", "https://as.nyu.edu/content/dam/nyu-as/liberalStudies/images/faculty/Nikolay-Kukushkin.jpg")
}

for name, (kind, target) in sources.items():
    out_file = DEST / f"{name}.jpg"
    try:
        if kind == "wiki":
            img_url = get_wiki_thumb(target)
            if not img_url:
                print(f"Failed to find wiki thumb for {name} ({target})")
                continue
        else:
            img_url = target
        print(f"Downloading {name} from {img_url}...")
        download_file(img_url, out_file)
    except Exception as e:
        print(f"Error downloading {name}: {e}")

