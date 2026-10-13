"""Tests fuer die reinen Hilfsfunktionen in utils.py."""

import os
from datetime import datetime

import utils
from utils import datum_aus_name, ermittle_datum, freier_platz, kopiere_verifiziert, lesbare_groesse


def test_datum_aus_name_kompakt():
    assert datum_aus_name("IMG_20200102_123.jpg") == datetime(2020, 1, 2)


def test_datum_aus_name_getrennt():
    assert datum_aus_name("Urlaub 2020-05-06 Strand.jpg") == datetime(2020, 5, 6)


def test_datum_aus_name_mit_punkt():
    assert datum_aus_name("Foto 2019.11.30.jpg") == datetime(2019, 11, 30)


def test_datum_aus_name_nur_jahr():
    assert datum_aus_name("Urlaub 2015.jpg") == datetime(2015, 1, 1)


def test_datum_aus_name_jahr_nach_unterstrich():
    # Bekanntes Verhalten: '_' ist ein Wortzeichen, deshalb greift \b nicht
    # und ein reines Jahr direkt nach '_' wird nicht erkannt.
    assert datum_aus_name("DSC_2015.jpg") is None


def test_datum_aus_name_kein_datum():
    assert datum_aus_name("bild.jpg") is None
    assert datum_aus_name("IMG_1234.jpg") is None


def test_datum_aus_name_ungueltiges_datum_faellt_auf_jahr_zurueck():
    # 2020-13-45 ist ungueltig; die Jahres-Erkennung greift und liefert 2020-01-01.
    assert datum_aus_name("2020-13-45.jpg") == datetime(2020, 1, 1)


def test_kopiere_verifiziert(tmp_path):
    src = tmp_path / "quelle.jpg"
    dst = tmp_path / "ziel.jpg"
    src.write_bytes(b"medieninhalt")

    assert kopiere_verifiziert(src, dst) is True
    assert dst.read_bytes() == b"medieninhalt"
    assert not dst.with_name(dst.name + ".tmp").exists()


def test_ermittle_datum_nutzt_video_metadaten(monkeypatch, tmp_path):
    aufnahme = datetime(2024, 3, 4, 5, 6, 7)
    video = tmp_path / "clip.mp4"
    video.touch()
    monkeypatch.setattr(utils, "exif_datum", lambda _pfad: None)
    monkeypatch.setattr(utils, "video_datum", lambda _pfad: aufnahme)

    assert ermittle_datum(video) == (aufnahme, "Video")


def test_lesbare_groesse():
    assert lesbare_groesse(0) == "0.0 KB"
    assert lesbare_groesse(1024) == "1.0 KB"
    assert lesbare_groesse(1024 * 1024) == "1.0 MB"
    assert lesbare_groesse(1024**3) == "1.00 GB"


def test_freier_platz_liefert_wert_oder_none(tmp_path):
    frei = freier_platz(tmp_path)
    assert frei is None or frei > 0


def test_freier_platz_none_bei_fehler(monkeypatch):
    monkeypatch.setattr(
        utils.shutil, "disk_usage", lambda _p: (_ for _ in ()).throw(OSError("kein Zugriff"))
    )
    assert freier_platz("X:\\nicht\\vorhanden") is None


def test_hash_datei_gleich_und_verschieden(tmp_path):
    a = tmp_path / "a.bin"
    b = tmp_path / "b.bin"
    c = tmp_path / "c.bin"
    a.write_bytes(b"inhalt")
    b.write_bytes(b"inhalt")
    c.write_bytes(b"anderer inhalt")

    assert utils.hash_datei(a) == utils.hash_datei(b)
    assert utils.hash_datei(a) != utils.hash_datei(c)


def test_hash_datei_none_bei_fehlender_datei(tmp_path):
    assert utils.hash_datei(tmp_path / "gibtsnicht.bin") is None


def test_lang_pfad_kurzer_pfad_bleibt_unveraendert():
    pfad = os.path.join("unterordner", "datei.txt")
    assert utils.lang_pfad(pfad) == pfad


def test_lang_pfad_langer_pfad_bekommt_prefix(tmp_path):
    lang = tmp_path / ("x" * 200) / ("y" * 100) / "datei.txt"

    ergebnis = utils.lang_pfad(lang)

    if os.name == "nt":
        assert ergebnis.startswith("\\\\?\\")
    else:
        assert ergebnis == str(lang)
