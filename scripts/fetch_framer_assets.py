#!/usr/bin/env python3
"""
Rapatrie les logos des competences du site Framer dans assets/img/skills/.
Optionnel : sans ces logos, les competences s'affichent sans icone.

Ne concerne PAS la photo (assets/nl_picture.png), les badges de
certification (deja dans assets/img/) ni l'image de partage (og-image.png).

A lancer UNE fois, depuis la racine du repo, AVANT de resilier Framer :
    python3 scripts/fetch_framer_assets.py        (macOS / Linux)
    py scripts\\fetch_framer_assets.py             (Windows)

Aucune dependance. Si Pillow est installe, les images trop grandes sont reduites.
Relancable sans risque : les fichiers deja presents sont ignores
(ajouter --force pour tout retelecharger).
"""
import io
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
CDN = "https://framerusercontent.com/images/"
UA = "Mozilla/5.0 (fetch_framer_assets.py)"

# fichier local -> (URL Framer, cote max en px ; None = taille d'origine)
ASSETS = {
    "skills/office365.png":    (CDN + "cXhmBdzTzv5MSmmnW6xvmj7L30.png", 128),
    "skills/google-cloud.png": (CDN + "YPSa0pCHxWoweoj2RIHgHd1nNo.png", 128),
    "skills/atlassian.png":    (CDN + "8O5j8ImIECpILYQIhISaFePNQdE.png", 128),
    "skills/adobe.png":        (CDN + "2dTXUAQpn5rzQOL7lKEsYtLLFjY.png", 128),
    "skills/github.png":       (CDN + "d1nodtQNWbrfbUkpLRX35WbxPGM.png", 128),
    "skills/linux.png":        (CDN + "hpCNJUXt9rHTv0siJak1k87AXc8.png", 128),
    "skills/data.png":         (CDN + "Vz2frtsTUqrUDYvWU3seiko2U.png", 128),
    "skills/python.png":       (CDN + "iwQpp2Nqj8bQd3BVzwajmGZ56GI.png", 128),
}

SIGNATURES = {  # premiers octets -> format reel
    b"\xff\xd8\xff": "jpeg",
    b"\x89PNG": "png",
    b"RIFF": "webp",
    b"GIF8": "gif",
}


def sniff(data):
    for sig, fmt in SIGNATURES.items():
        if data.startswith(sig):
            if fmt == "webp" and data[8:12] != b"WEBP":
                continue
            return fmt
    return None


def download(url):
    """urllib d'abord ; curl en secours (cas classique : certificats Python absents sur macOS)."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read()
    except urllib.error.HTTPError:
        raise
    except urllib.error.URLError as err:
        if not shutil.which("curl"):
            raise
        out = subprocess.run(["curl", "-fsSL", "--max-time", "30", "-A", UA, url], capture_output=True)
        if out.returncode != 0:
            raise RuntimeError("urllib: %s / curl: code %d" % (err.reason, out.returncode))
        return out.stdout


def fetch(url, max_px):
    """Demande d'abord une version deja reduite au CDN Framer, sinon l'original."""
    if max_px:
        try:
            return download("%s?scale-down-to=%d" % (url, max_px))
        except urllib.error.HTTPError:
            pass
    return download(url)


def shrink(data, max_px):
    """Reduit l'image si Pillow est dispo et qu'elle depasse max_px. Sinon, inchangee."""
    if not max_px:
        return data
    try:
        from PIL import Image
    except ImportError:
        return data
    img = Image.open(io.BytesIO(data))
    if max(img.size) <= max_px:
        return data
    fmt = img.format
    if img.mode in ("P", "L", "LA", "1"):
        img = img.convert("RGBA")
    img.thumbnail((max_px, max_px), Image.LANCZOS)
    buf = io.BytesIO()
    if fmt == "JPEG":
        img.convert("RGB").save(buf, "JPEG", quality=85, optimize=True, progressive=True)
    elif fmt == "PNG":
        img.save(buf, "PNG", optimize=True)
    else:
        img.save(buf, fmt)
    return buf.getvalue()


def main():
    force = "--force" in sys.argv
    ok = skipped = failed = 0
    print("Destination : %s" % IMG)
    for rel, (url, max_px) in ASSETS.items():
        dest = IMG / rel
        if dest.exists() and dest.stat().st_size > 0 and not force:
            print("  deja la   %s" % rel)
            skipped += 1
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            data = fetch(url, max_px)
            real = sniff(data)
            if real is None:
                raise RuntimeError("la reponse n'est pas une image (%d octets)" % len(data))
            data = shrink(data, max_px)
            dest.write_bytes(data)
            note = "" if real in dest.suffix.lower() or (real == "jpeg" and dest.suffix == ".jpg") else "  (format reel : %s)" % real
            print("  ok        %s  %d Ko%s" % (rel, max(1, len(data) // 1024), note))
            ok += 1
        except Exception as err:  # noqa: BLE001 - on veut continuer sur les autres images
            print("  ECHEC     %s  -- %s\n            source : %s" % (rel, err, url))
            failed += 1

    print("\n%d telechargee(s), %d deja presente(s), %d echec(s)." % (ok, skipped, failed))
    if failed:
        print("Relance le script. Si l'echec persiste, ouvre l'URL Framer dans le navigateur,")
        print("enregistre l'image sous le nom indique dans assets/img/, puis relance.")
        sys.exit(1)
    print("Verification locale : python3 -m http.server 8000  puis  http://localhost:8000")


if __name__ == "__main__":
    main()
