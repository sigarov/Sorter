#!/usr/bin/env bash
#
# Baut eine AppImage fuer den Medien-Sortierer.
#
# WICHTIG: AppImages lassen sich NUR unter Linux bauen
#          (nativ, WSL2 oder eine Linux-VM).
#
# Aufruf:   chmod +x build_linux_appimage.sh
#           ./build_linux_appimage.sh
#
set -euo pipefail

# Immer im Ordner dieses Skripts arbeiten
cd "$(dirname "$(readlink -f "$0")")"

echo "============================================================"
echo "  Medien-Sortierer - Linux-AppImage bauen"
echo "============================================================"
echo

# --- 0) Grundvoraussetzungen pruefen ---------------------------------
if [ "$(uname -s)" != "Linux" ]; then
    echo "[FEHLER] AppImages lassen sich nur unter Linux bauen."
    echo "         Nutze Linux nativ, WSL2 (wsl --install) oder eine VM."
    echo "         Auf Windows/macOS kann dieses Skript nicht laufen."
    exit 1
fi

fehlend=()
command -v python3 >/dev/null 2>&1 || fehlend+=("python3")
command -v wget    >/dev/null 2>&1 || fehlend+=("wget")
command -v file    >/dev/null 2>&1 || fehlend+=("file")
if [ ${#fehlend[@]} -gt 0 ]; then
    echo "[FEHLER] Fehlende Programme: ${fehlend[*]}"
    echo "         Installation (Debian/Ubuntu):"
    echo "         sudo apt update && sudo apt install -y python3 python3-venv python3-tk wget file"
    exit 1
fi

# tkinter muss vorhanden sein, sonst fehlt Tk spaeter in der AppImage
if ! python3 -c 'import tkinter' >/dev/null 2>&1; then
    echo "[FEHLER] tkinter fehlt. Ohne das startet die GUI in der AppImage nicht."
    echo "         Installation (Debian/Ubuntu):"
    echo "         sudo apt install -y python3-tk"
    exit 1
fi

echo "Python: $(python3 --version 2>&1)"
echo

# --- 1) Eingabedatei abfragen ----------------------------------------
while :; do
    read -r -p "Welche Datei soll umgewandelt werden? [main.py]: " SCRIPT
    SCRIPT="${SCRIPT:-main.py}"
    if [ -f "$SCRIPT" ]; then
        break
    fi
    echo "[FEHLER] Datei \"$SCRIPT\" nicht gefunden. Bitte erneut eingeben."
    echo
done

# --- 2) App-Namen abfragen -------------------------------------------
read -r -p "Wie soll die AppImage heissen? [MedienSortierer]: " APPNAME
APPNAME="${APPNAME:-MedienSortierer}"
# Leerzeichen sind im Dateinamen unhandlich -> Bindestrich
APPNAME="${APPNAME// /-}"
# Binaername: klein, ohne Sonderzeichen (fuer AppRun/.desktop)
BINNAME="$(printf '%s' "$APPNAME" | tr '[:upper:]' '[:lower:]' | tr -cd 'a-z0-9._-')"
if [ -z "$BINNAME" ]; then
    BINNAME="medien-sortierer"
fi

AUSGABE="${APPNAME}-x86_64.AppImage"

echo
echo "------------------------------------------------------------"
echo "  Eingabedatei : $SCRIPT"
echo "  App-Name     : $APPNAME"
echo "  Binaer       : $BINNAME"
echo "  Ausgabe      : $AUSGABE"
echo "  Modus        : --onedir (empfohlen fuer AppImage)"
echo "------------------------------------------------------------"
echo
read -r -p "Starten? [J/n]: " OK
case "$OK" in
    [nN]*) echo "Abgebrochen."; exit 0 ;;
esac

# --- 3) Build-Umgebung -----------------------------------------------
BUILDVENV=".build-venv"
if [ ! -d "$BUILDVENV" ]; then
    echo "Erzeuge Build-Umgebung ($BUILDVENV) ..."
    python3 -m venv "$BUILDVENV"
fi
# shellcheck disable=SC1091
. "$BUILDVENV/bin/activate"

echo "Installiere/aktualisiere PyInstaller ..."
pip install --quiet --upgrade pip pyinstaller

# --- 4) PyInstaller ---------------------------------------------------
rm -rf build "dist/$BINNAME"
echo
echo "Baue mit PyInstaller ..."
pyinstaller --noconfirm --clean --onedir --windowed --name "$BINNAME" "$SCRIPT"

if [ ! -x "dist/$BINNAME/$BINNAME" ]; then
    echo "[FEHLER] Build fehlgeschlagen: dist/$BINNAME/$BINNAME nicht gefunden."
    exit 1
fi

# --- 5) AppDir aufbauen ----------------------------------------------
APPDIR="AppDir"
rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin"
cp -r "dist/$BINNAME/." "$APPDIR/usr/bin/"

cat > "$APPDIR/AppRun" <<EOF
#!/bin/sh
HERE="\$(dirname "\$(readlink -f "\$0")")"
exec "\$HERE/usr/bin/$BINNAME" "\$@"
EOF
chmod +x "$APPDIR/AppRun"

cat > "$APPDIR/$BINNAME.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=$APPNAME
Exec=$BINNAME
Icon=$BINNAME
Categories=Utility;FileTools;
Terminal=false
EOF

# --- 6) Icon ----------------------------------------------------------
if [ -f icon.png ]; then
    cp icon.png "$APPDIR/$BINNAME.png"
    echo "Icon: icon.png uebernommen."
else
    echo "Kein icon.png gefunden - erzeuge ein schlichtes Platzhalter-Icon."
    python3 - "$APPDIR/$BINNAME.png" <<'PY'
import struct, sys, zlib

w = h = 256
r, g, b = 0x2E, 0x5A, 0x88  # dunkles Blau
zeile = b"\x00" + bytes([r, g, b]) * w
rohdaten = zeile * h

def chunk(tag, daten):
    return (
        struct.pack(">I", len(daten))
        + tag
        + daten
        + struct.pack(">I", zlib.crc32(tag + daten) & 0xFFFFFFFF)
    )

png = b"\x89PNG\r\n\x1a\n"
png += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
png += chunk(b"IDAT", zlib.compress(rohdaten, 9))
png += chunk(b"IEND", b"")

with open(sys.argv[1], "wb") as f:
    f.write(png)
PY
fi

# --- 7) appimagetool holen -------------------------------------------
TOOL="appimagetool-x86_64.AppImage"
if [ ! -x "$TOOL" ]; then
    echo "Lade appimagetool ..."
    wget -q -O "$TOOL" \
        "https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage"
    chmod +x "$TOOL"
fi

# --- 8) AppImage bauen -----------------------------------------------
export ARCH=x86_64
echo
echo "Erzeuge $AUSGABE ..."
if ! "./$TOOL" "$APPDIR" "$AUSGABE" 2>/dev/null; then
    echo "Direkter Aufruf fehlgeschlagen (meist fehlt FUSE) - nutze Extract-and-run ..."
    "./$TOOL" --appimage-extract-and-run "$APPDIR" "$AUSGABE"
fi

chmod +x "$AUSGABE"

echo
echo "============================================================"
echo "  Fertig:  $AUSGABE"
echo "============================================================"
echo
echo "Testen:"
echo "  ./$AUSGABE"
echo
echo "Hinweis: Bitte auf einem Linux OHNE python3-tk testen, damit du"
echo "         merkst, falls Tk doch nicht mit eingepackt wurde."
echo
