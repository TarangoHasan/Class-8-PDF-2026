import os
import re
import urllib.request
import urllib.parse
import http.cookiejar

BOOKS = [
    {
        "serial": 1,
        "filename": "01_sahitya_konika.pdf",
        "gdrive_id": "1CRDDFTH32XZoy78SrFQ3m8wUujbLeuFY",
        "backup_url": "https://drive.egovcloud.gov.bd/index.php/s/YBnK8nxVuF8YHaD/download"
    },
    {
        "serial": 2,
        "filename": "02_anandapath.pdf",
        "gdrive_id": "1g77qC2lEOdnFqMYxM8DpyYzhS3m0wgLK",
        "backup_url": "https://drive.egovcloud.gov.bd/index.php/s/lsz7WPFLAZv7gmo/download"
    },
    {
        "serial": 3,
        "filename": "03_bangla_byakoron_o_nirmiti.pdf",
        "gdrive_id": "1O0aS5cJsRDqc47nIWY2uVLqldAEZGtk-",
        "backup_url": "https://drive.egovcloud.gov.bd/index.php/s/c0BButuHGZRxugA/download"
    },
    {
        "serial": 4,
        "filename": "04_english_for_today.pdf",
        "gdrive_id": "1m7TlILofUr64YC61XBW96rhW0fvCI_dv",
        "backup_url": "https://drive.egovcloud.gov.bd/index.php/s/gnSVZ8LoHftPSdo/download"
    },
    {
        "serial": 5,
        "filename": "05_english_grammar_and_composition.pdf",
        "gdrive_id": "1OfJd_F1uVMqE1KDaQHKhN3mQ-LcPm7rt",
        "backup_url": "https://drive.egovcloud.gov.bd/index.php/s/D8FEJJlaJYtzSr8/download"
    },
    {
        "serial": 6,
        "filename": "06_gonit.pdf",
        "gdrive_id": "12ygatNBK0ilJdccpnpuoT1N2G4pcaCya",
        "backup_url": "https://drive.egovcloud.gov.bd/index.php/s/h4caIbfzbyxWmNc/download"
    },
    {
        "serial": 7,
        "filename": "07_ict.pdf",
        "gdrive_id": "1Iiil02LWRp7cZDjOyRF3Lsw3ECkuMWfn",
        "backup_url": "https://drive.egovcloud.gov.bd/index.php/s/ipadnjIh0hQ7xMR/download"
    },
    {
        "serial": 8,
        "filename": "08_bangladesh_o_bishwoporichoy.pdf",
        "gdrive_id": "1aY3sFRDEQsAGUlUg3SvKgh5TI3lKJ1RB",
        "backup_url": "https://drive.egovcloud.gov.bd/index.php/s/yc5DKo4i94aicwV/download"
    },
    {
        "serial": 9,
        "filename": "09_biggan.pdf",
        "gdrive_id": "13Ms7Jse6GAssepHFewohlp_ioc-UuyjH",
        "backup_url": "https://drive.egovcloud.gov.bd/index.php/s/0bOss47EGDKxsPp/download"
    },
    {
        "serial": 15,
        "filename": "15_islam_shikkha.pdf",
        "gdrive_id": "1G9Rd8sUl_8yonygVz5-kBFTJVkiXR97T",
        "backup_url": "https://drive.egovcloud.gov.bd/index.php/s/TbhAtkiy9TtrVTb/download"
    }
]

RAW_DIR = "f:/Desktop/antigravity/book-pdf/raw"
os.makedirs(RAW_DIR, exist_ok=True)

def download_gdrive(file_id, out_path):
    url = f"https://drive.usercontent.google.com/download?id={file_id}&export=download&confirm=t"
    headers = {"User-Agent": "Mozilla/5.0"}
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    req = urllib.request.Request(url, headers=headers)
    
    with opener.open(req, timeout=60) as resp:
        content_type = resp.headers.get("Content-Type", "")
        if "text/html" in content_type:
            html = resp.read().decode("utf-8", errors="ignore")
            match = re.search(r'confirm=([0-9A-Za-z_]+)', html)
            if match:
                confirm = match.group(1)
                url2 = f"https://drive.usercontent.google.com/download?id={file_id}&export=download&confirm={confirm}"
                req2 = urllib.request.Request(url2, headers=headers)
                with opener.open(req2, timeout=60) as resp2:
                    with open(out_path, "wb") as f:
                        f.write(resp2.read())
                return True
            else:
                return False
        else:
            with open(out_path, "wb") as f:
                while True:
                    chunk = resp.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)
            return True

def download_backup(url, out_path):
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=120) as resp:
        with open(out_path, "wb") as f:
            while True:
                chunk = resp.read(1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)
    return True

for book in BOOKS:
    dest = os.path.join(RAW_DIR, book["filename"])
    if os.path.exists(dest) and os.path.getsize(dest) > 100000:
        print(f"[EXISTS] {book['filename']} ({os.path.getsize(dest)} bytes)")
        continue
    
    print(f"Downloading serial {book['serial']}: {book['filename']} from Google Drive (Link 1)...")
    success = False
    try:
        success = download_gdrive(book["gdrive_id"], dest)
        if success and os.path.exists(dest) and os.path.getsize(dest) > 100000:
            print(f"  [SUCCESS] Downloaded {book['filename']} ({os.path.getsize(dest)} bytes)")
        else:
            print(f"  [WARNING] Link 1 returned small or invalid file, trying Link 2 backup...")
            success = False
    except Exception as e:
        print(f"  [ERROR] Link 1 failed: {e}. Trying Link 2...")

    if not success:
        try:
            download_backup(book["backup_url"], dest)
            print(f"  [SUCCESS Link 2] Downloaded {book['filename']} ({os.path.getsize(dest)} bytes)")
        except Exception as e2:
            print(f"  [FAILED] Could not download {book['filename']}: {e2}")

print("Done downloading all books.")
