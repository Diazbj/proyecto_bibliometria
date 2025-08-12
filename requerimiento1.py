import os
import argparse
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.downloader_acm import ACMDownloader
from utils.downloader_sciencedirect import ScienceDirectDownloader

DOWNLOAD_DIR = os.path.abspath("./descargas")

def main(query, headless=False, acm=True, sciencedirect=True):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    if acm:
        print("[INFO] Descargando desde ACM...")
        acm_downloader = ACMDownloader(DOWNLOAD_DIR, headless=headless)
        acm_downloader.download(query)
        acm_downloader.close()

    if sciencedirect:
        print("[INFO] Descargando desde ScienceDirect...")
        sd_downloader = ScienceDirectDownloader(DOWNLOAD_DIR, headless=headless)
        sd_downloader.download(query)
        sd_downloader.close()

    print("[INFO] Descargas finalizadas. Archivos en:", DOWNLOAD_DIR)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automatización descargas ACM y ScienceDirect")
    parser.add_argument("--query", type=str, required=True, help="Cadena de búsqueda")
    parser.add_argument("--headless", action="store_true", help="Ejecutar navegador en modo headless")
    parser.add_argument("--no-acm", action="store_true", help="No descargar desde ACM")
    parser.add_argument("--no-sd", action="store_true", help="No descargar desde ScienceDirect")
    args = parser.parse_args()

    main(
        query=args.query,
        headless=args.headless,
        acm=not args.no_acm,
        sciencedirect=not args.no_sd
    )
