# -*- coding: utf-8 -*-
"""Polskie tlumaczenia zagrozen z biblioteki "INTUITEM Common Catalog" (ICT-001..ICT-023).

Bierze oryginal z backend/library/libraries/intuitem-common-catalog.yaml, dopisuje translations.pl
(nazwa i opis) do biblioteki i kazdego zagrozenia, podbija wersje o 1 i zapisuje do
octopus/libraries/intuitem-common-catalog.yaml. Ten plik jest montowany w backendzie w miejsce
oryginalu, a na istniejacej instancji biblioteke aktualizuje sie przyciskiem "Aktualizuj"
(albo skryptem aktualizuj-istniejaca-instancje.sh). Angielskie nazwy zostaja dla uzytkownikow EN.
Po aktualizacji upstream uruchom ponownie: python3 octopus/translations/build_intuitem_common_catalog_pl.py
"""
import os
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "backend", "library", "libraries", "intuitem-common-catalog.yaml")
OUT = os.path.join(HERE, "..", "libraries", "intuitem-common-catalog.yaml")

LIBRARY_PL = {"name": "Katalog wspólny INTUITEM", "description": "Katalog wspólny INTUITEM - zagrożenia"}

PL = {
    "ICT-001": ("Ransomware",
                "Złośliwe oprogramowanie szyfruje dane i żąda okupu za klucze deszyfrujące"),
    "ICT-002": ("Phishing i spear phishing",
                "Fałszywe e-maile lub wiadomości nakłaniają użytkowników do ujawnienia poufnych informacji "
                "albo umożliwienia dostępu"),
    "ICT-003": ("Ataki przez dostawców i łańcuch dostaw",
                "Przejęcie dostawcy zewnętrznego w celu uzyskania dostępu do właściwej organizacji"),
    "ICT-004": ("Wykorzystanie podatności zero-day",
                "Wykorzystanie nieznanych podatności, zanim dostępne będą poprawki"),
    "ICT-005": ("Zagrożenia wewnętrzne",
                "Złośliwe lub niedbałe działania pracowników albo wykonawców"),
    "ICT-006": ("Zaawansowane długotrwałe zagrożenia (APT)",
                "Długotrwałe, ukierunkowane ataki cyberszpiegowskie prowadzone przez grupy wspierane przez państwa"),
    "ICT-007": ("Ataki DoS / DDoS",
                "Przeciążenie systemów powodujące niedostępność usług"),
    "ICT-008": ("Socjotechnika",
                "Manipulowanie ludźmi w celu wyłudzenia poufnych informacji lub uzyskania dostępu"),
    "ICT-009": ("Złośliwe oprogramowanie i oprogramowanie szpiegujące",
                "Oprogramowanie służące do uszkodzenia systemów lub szpiegowania"),
    "ICT-010": ("Cryptojacking",
                "Nieuprawnione wykorzystanie zasobów obliczeniowych do wydobywania kryptowalut"),
    "ICT-011": ("Podszywanie się pod DNS i przejęcie DNS",
                "Przejęcie kontroli nad DNS w celu przekierowania użytkowników na złośliwe strony"),
    "ICT-012": ("Ataki na hasła (brute force, credential stuffing)",
                "Wielokrotne próby odgadnięcia haseł lub użycie wykradzionych danych logowania"),
    "ICT-013": ("Deepfake i oszustwa z fałszywą tożsamością",
                "Wykorzystanie treści generowanych przez AI do podszywania się pod inne osoby"),
    "ICT-014": ("Zagrożenia związane ze sztuczną inteligencją i manipulacja modelami",
                "Stronniczość modeli, ataki adwersarialne, zatruwanie modeli, manipulacja danymi i obchodzenie "
                "zabezpieczeń modeli językowych, prowadzące do nieuprawnionych działań, dezinformacji i błędnych decyzji"),
    "ICT-015": ("Zagrożenia dla bezpieczeństwa chmury",
                "Błędy konfiguracji, niezabezpieczone API i przejęcia kont w środowiskach chmurowych, prowadzące "
                "do ujawnienia danych i nieuprawnionego dostępu"),
    "ICT-016": ("Podatności urządzeń IoT",
                "Niezabezpieczone urządzenia i czujniki inteligentne, prowadzące do przejęcia sieci i nieuprawnionego "
                "dostępu do wrażliwych danych"),
    "ICT-017": ("Zagrożenia dla urządzeń mobilnych",
                "Ryzyka związane z urządzeniami mobilnymi, w tym złośliwe aplikacje, kradzież urządzenia "
                "i nieuprawniony dostęp do wrażliwych danych"),
    "ICT-018": ("Zagrożenia dla bezpieczeństwa API",
                "Wykorzystanie słabo zabezpieczonych API do nieuprawnionego dostępu, wycieku danych "
                "i manipulacji logiką biznesową"),
    "ICT-019": ("Naruszenie i wyciek danych, shadow IT",
                "Nieuprawnione ujawnienie danych w wyniku ataku, błędu albo przez aplikacje i usługi używane "
                "przez pracowników bez zgody organizacji"),
    "ICT-020": ("Zagrożenia fizyczne (manipulacja i kradzież)",
                "Nieuprawniony fizyczny dostęp do sprzętu, ingerencja lub kradzież, prowadzące do naruszenia danych "
                "albo manipulacji sprzętem"),
    "ICT-021": ("Dezinformacja i ataki na reputację",
                "Celowe rozpowszechnianie fałszywych lub wprowadzających w błąd informacji w celu zaszkodzenia "
                "reputacji organizacji, manipulowania opinią publiczną lub wpływania na decyzje"),
    "ICT-022": ("Awaria systemu (usterka, błąd oprogramowania lub pomyłka)",
                "Nieplanowane przerwy w dostępności systemów spowodowane awariami, błędami oprogramowania, błędami "
                "konfiguracji lub pomyłkami ludzi, prowadzące do przestojów i możliwej utraty danych"),
    "ICT-023": ("Niezgodność z przepisami",
                "Niespełnienie wymagań prawnych i regulacyjnych, skutkujące karami, postępowaniami, ograniczeniami "
                "działalności i utratą reputacji"),
}

if __name__ == "__main__":
    lib = yaml.safe_load(open(SRC, encoding="utf-8"))
    lib["version"] = int(lib["version"]) + 1
    lib.setdefault("translations", {})["pl"] = LIBRARY_PL
    threats = lib["objects"]["threats"]
    missing = []
    for t in threats:
        tr = PL.get(t["ref_id"])
        if not tr:
            missing.append(t["ref_id"])
            continue
        t.setdefault("translations", {})["pl"] = {"name": tr[0], "description": tr[1]}
    txt = yaml.safe_dump(lib, allow_unicode=True, sort_keys=False, width=110)
    assert "–" not in txt and "—" not in txt, "dlugi myslnik"
    open(OUT, "w", encoding="utf-8").write(txt)
    print(OUT, "wersja", lib["version"], "zagrozen", len(threats), "bez tlumaczenia:", missing or "brak")
