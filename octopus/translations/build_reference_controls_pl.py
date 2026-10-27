# -*- coding: utf-8 -*-
"""Polskie wzorcowe srodki (reference controls) w CISO Assistant.

Wzorcowe srodki w CISO Assistant pochodza z dwoch bibliotek intuitem:
  - ISO/IEC 27001:2022 (iso27001-2022.yaml): 93 zabezpieczenia zalacznika A i rama ISO 27001,
  - CISO Assistant Key Reference Controls (key-reference-controls.yaml, URN doc-pol): 175 srodkow
    DOC/POL/PROC/TRAIN/TECH/PHYS powiazanych z ISO/IEC 27001, CIS Controls v8, RODO i innymi.

Skrypt dopisuje translations.pl (nazwa, opis, adnotacja, typowe dowody) i zapisuje obie biblioteki
w octopus/libraries z wersja podbita o 1. W adnotacji kazdego srodka jest zrodlo (z jakiego
frameworku wynika) oraz powiazane punkty NIS2 (rozporzadzenie wykonawcze 2024/2690) i ustawy o KSC
(wymagania KSC-xx z biblioteki Octopus Lab). Powiazania z 2024/2690 pochodza z oficjalnego mapowania
intuitem (mapping-annex-technical-and-methodological-requirements-nis2-and-iso27001-2022.yaml),
a przejscie 2024/2690 -> art. 8 ustawy o KSC z mapy wymagan Octopus Lab (40_mapa_wymagan...).
Dla ramy ISO 27001 dopisane sa tez polskie nazwy rozdzialow 4-10 i zalacznika A.

Pliki sa montowane w backendzie w miejsce oryginalow. Na istniejacej instancji biblioteki aktualizuje
sie przyciskiem "Aktualizuj" (najpierw Key Reference Controls, potem ISO 27001) albo skryptem
aktualizuj-istniejaca-instancje.sh. Angielskie teksty zostaja dla uzytkownikow EN.
Po aktualizacji upstream uruchom ponownie: python3 octopus/translations/build_reference_controls_pl.py
Tlumaczenia: octopus/translations/reference_controls_pl.json
"""
import datetime
import json
import os
import re
from collections import defaultdict

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
LIBS = os.path.join(HERE, "..", "..", "backend", "library", "libraries")
OUT = os.path.join(HERE, "..", "libraries")
DATA = json.load(open(os.path.join(HERE, "reference_controls_pl.json"), encoding="utf-8"))
TODAY = datetime.date(2026, 10, 27)

# --- powiazania ISO 27001 -> 2024/2690 (mapowanie intuitem) -----------------------------------------
_map = yaml.safe_load(
    open(
        os.path.join(LIBS, "mapping-annex-technical-and-methodological-requirements-nis2-and-iso27001-2022.yaml"),
        encoding="utf-8",
    )
)
ISO2NIS = defaultdict(set)
for ms in _map["objects"]["requirement_mapping_sets"]:
    if not ms["source_framework_urn"].endswith(":iso27001-2022"):
        continue
    for m in ms["requirement_mappings"]:
        iso = m["source_requirement_urn"].split(":")[-1].lower()
        nis = m["target_requirement_urn"].split(":")[-1]
        sec = ".".join(nis.split(".")[:2])
        if "." in sec:  # pomijamy nieliczne powiazania z calym rozdzialem (np. "1")
            ISO2NIS[iso].add(sec)


def _seckey(s):
    return tuple(int(x) if x.isdigit() else 0 for x in s.split("."))


# Nazwy wymagan z biblioteki "Ustawa o KSC - obowiazki krajowe" (KSC-xx -> "art. ...")
_ksc = yaml.safe_load(open(os.path.join(OUT, "octopus-lab-ksc-obowiazki-krajowe.yaml"), encoding="utf-8"))
KSC_LABEL = {
    n["ref_id"]: n["name"][0].lower() + n["name"][1:]
    for n in _ksc["objects"]["framework"]["requirement_nodes"]
    if (n.get("ref_id") or "").startswith("KSC-") and n.get("name")
}

# Uzupelnienie Octopus Lab dla zabezpieczen, ktorych nie ma w mapowaniu intuitem ISO 27001 <-> 2024/2690
# (na podstawie mapy wymagan KSC - 2024/2690 - ISO 27001 Octopus Lab)
ISO2NIS_EXTRA = {
    "a.5.5": {"3.3", "3.5"},
    "a.5.6": {"6.10"},
    "a.5.8": {"6.1"},
    "a.5.33": {"1.1"},
    "a.5.37": {"1.1"},
    "a.6.6": {"10.1"},
    "a.7.6": {"13.3"},
    "a.7.8": {"13.2"},
    "a.7.9": {"12.2"},
    "a.7.12": {"13.1"},
    "a.7.14": {"12.2"},
    "a.8.1": {"8.1"},
    "a.8.4": {"6.2"},
    "a.8.10": {"12.2"},
    "a.8.19": {"6.9"},
    "a.8.23": {"6.9"},
    "a.8.26": {"6.2"},
    "a.8.27": {"6.2"},
    "a.8.28": {"6.2"},
}
# Obowiazki z ustawy o KSC, ktorych nie ma w 2024/2690 (art. 8c-8f, 9, 10, 15)
ISO2KSC_EXTRA = {
    "5.1": {"KSC-24", "KSC-25"},
    "a.5.4": {"KSC-24", "KSC-25"},
    "9.3.1": {"KSC-25"},
    "9.3.2": {"KSC-25"},
    "9.3.3": {"KSC-25"},
    "7.2": {"KSC-26"},
    "a.6.3": {"KSC-26"},
    "a.6.1": {"KSC-27"},
    "a.5.5": {"KSC-28", "KSC-31"},
    "a.6.8": {"KSC-30"},
    "7.5": {"KSC-32"},
    "7.5.1": {"KSC-32"},
    "7.5.2": {"KSC-32"},
    "7.5.3": {"KSC-32"},
    "a.5.33": {"KSC-32", "KSC-34"},
    "a.5.37": {"KSC-32"},
    "a.8.15": {"KSC-34"},
    "9.2.1": {"KSC-48"},
    "9.2.2": {"KSC-48"},
    "a.5.35": {"KSC-48"},
}


def nis_to_ksc(sec):
    ch, _, sub = sec.partition(".")
    ch = int(ch)
    sub = int(sub) if sub.isdigit() else 0
    if ch == 1:
        return {"KSC-05"}
    if ch == 2:
        return {"KSC-04", "KSC-05"} if sub == 1 else {"KSC-12"}
    if ch == 3:
        return {"KSC-11"} if sub == 2 else {"KSC-20"}
    if ch == 4:
        return {"KSC-10"}
    if ch == 5:
        return {"KSC-09"}
    if ch == 6:
        out = set()
        if sub <= 6 or sub == 10:
            out.add("KSC-06")
        if 6 <= sub <= 9:
            out.add("KSC-21")
        if sub == 10:
            out.add("KSC-19")
        return out
    if ch == 7:
        return {"KSC-12"}
    if ch == 8:
        return {"KSC-14"} if sub == 1 else {"KSC-13"}
    if ch == 9:
        return {"KSC-15"}
    if ch == 10:
        return {"KSC-08"}
    if ch == 11:
        return {"KSC-16"} if sub >= 6 else {"KSC-18"}
    if ch == 12:
        return {"KSC-17"}
    if ch == 13:
        return {"KSC-07"}
    return set()


def _ksc_key(k):
    return int(k[4:])


def nis_ksc_lines(iso_nodes, extra_nis=()):
    nis, ksc_extra, supplemented = set(extra_nis), set(), False
    for n in iso_nodes:
        n = n.lower()
        floor = 3 if n.startswith("a.") else 2  # nie schodzimy do calego rozdzialu (np. 7 albo A.5)
        while n and len(n.split(".")) >= floor:
            if n in ISO2KSC_EXTRA:
                ksc_extra |= ISO2KSC_EXTRA[n]
            if n in ISO2NIS:
                nis |= ISO2NIS[n]
                break
            children = [k for k in ISO2NIS if k.startswith(n + ".")]
            if children:  # np. 9.3 -> 9.3.1, 9.3.2, 9.3.3
                for k in children:
                    nis |= ISO2NIS[k]
                    ksc_extra |= ISO2KSC_EXTRA.get(k, set())
                break
            if n in ISO2NIS_EXTRA:
                nis |= ISO2NIS_EXTRA[n]
                supplemented = True
                break
            n = n.rpartition(".")[0]  # 6.1.2.c -> 6.1.2 -> 6.1
    lines = []
    secs = sorted(nis, key=_seckey)
    if secs:
        lines.append("NIS2, rozporządzenie wykonawcze (UE) 2024/2690, załącznik, pkt: " + ", ".join(secs)
                     + (" (mapowanie uzupełniające Octopus Lab)" if supplemented else ""))
    ksc = sorted({k for s in secs for k in nis_to_ksc(s)} | ksc_extra, key=_ksc_key)
    if ksc:
        lines.append("Ustawa o KSC: " + "; ".join(f"{k} ({KSC_LABEL[k]})" for k in ksc))
    return lines


# --- adnotacje katalogu intuitem ---------------------------------------------------------------------
PREFIX = {
    "cis-v8": "CIS Controls v8",
    "iso-27002": "ISO/IEC 27002:2022",
    "iso-42001": "ISO/IEC 42001",
    "nist-ai-rmf": "NIST AI RMF",
    "scf": "Secure Controls Framework (SCF)",
    "eu-2024-2690": "Rozporządzenie wykonawcze (UE) 2024/2690 (NIS2), pkt",
    "cyfun2025": "CyberFundamentals 2025 (CyFun)",
    "nist-csf-2.0": "NIST CSF 2.0",
    "norea-dora": "NOREA DORA",
    "pcidss-4_0": "PCI DSS 4.0",
    "cra": "Cyber Resilience Act (CRA)",
}
BARE = {
    "iso-27701": "ISO/IEC 27701",
    "iso-29134": "ISO/IEC 29134",
    "iso-22301": "ISO 22301",
    "iso-27017": "ISO/IEC 27017",
    "iso-22361": "ISO 22361",
    "iso-27037": "ISO/IEC 27037",
    "iso-29147": "ISO/IEC 29147",
    "iso-42001": "ISO/IEC 42001",
    "iec-62443": "IEC 62443",
    "iec-62443-3-2": "IEC 62443-3-2",
    "iec-62443-2-1": "IEC 62443-2-1",
    "nist-sp-800-82": "NIST SP 800-82",
    "nist-ai-rmf": "NIST AI RMF",
    "eu-ai-act": "AI Act (rozporządzenie (UE) 2024/1689)",
    "eu-ai-act-art-4": "AI Act (rozporządzenie (UE) 2024/1689), art. 4",
    "dora-rts-tlpt": "DORA, RTS w sprawie testów TLPT",
    "tiber-eu": "TIBER-EU",
}


def iso_clause(ref):
    # 5.1.a -> 5.1 a), 6.1.2.c.2 -> 6.1.2 c) 2)
    parts = ref.split(".")
    nums = []
    for p in parts:
        if not p.isdigit():
            break
        nums.append(p)
    rest = parts[len(nums):]
    return ".".join(nums) + "".join(f" {p})" for p in rest)


def parse_annotation(ann):
    """Zwraca (linie_pl, frameworki, wezly_iso_27001, punkty_2690)."""
    groups = {}  # etykieta -> lista refow
    order = []
    iso_nodes, nis = [], []

    def add(label, refs):
        if label not in groups:
            groups[label] = []
            order.append(label)
        for r in refs:
            if r and r not in groups[label]:
                groups[label].append(r)

    for raw in (ann or "").replace(";", "\n").split("\n"):
        tok = raw.strip()
        if not tok:
            continue
        m = re.match(r"^gdpr-arts?-(\d+)(?:-(\d+))?$", tok)
        if m:
            add("RODO", [f"art. {m.group(1)}" + (f"-{m.group(2)}" if m.group(2) else "")])
            continue
        if tok in BARE:
            add(BARE[tok], [])
            continue
        m = re.match(r"^([a-z0-9\-_.]+):\s*(.+)$", tok)
        if m and m.group(1) in PREFIX:
            key, refs = m.group(1), [r.strip() for r in m.group(2).split(",")]
            if key == "cra":
                refs = [r.replace("Articles", "art.").replace("Article", "art.").replace("Annex", "zał.") for r in refs]
            if key == "nist-ai-rmf":
                refs = [r.upper() for r in refs]
            add(PREFIX[key], refs)
            if key == "iso-27002":
                iso_nodes += ["a." + r for r in refs]
            if key == "eu-2024-2690":
                nis += [".".join(r.split(".")[:2]) for r in refs]
            continue
        if m and m.group(1).startswith("iso-42001"):
            add("ISO/IEC 42001", [m.group(2)])
            continue
        # bez prefiksu: ISO/IEC 27001:2022 (rozdzialy 4-10 albo zalacznik A)
        for r in [x.strip() for x in tok.split(",")]:
            if not r:
                continue
            if r.upper().startswith("A."):
                add("ISO/IEC 27001:2022, załącznik A", [r.upper()])
                iso_nodes.append(r.lower())
            elif re.match(r"^\d", r):
                add("ISO/IEC 27001:2022, rozdziały", [iso_clause(r)])
                iso_nodes.append(r.lower())
            else:
                add(r, [])
    lines = []
    for label in order:
        refs = groups[label]
        lines.append(label + (": " + ", ".join(refs) if refs else ""))
    fws = []
    for label in order:
        short = label.split(", ")[0].split(" (")[0]
        if label.startswith("ISO/IEC 27001:2022") or label.startswith("ISO/IEC 27002"):
            short = "ISO/IEC 27001:2022"
        if label.startswith("Rozporządzenie wykonawcze (UE) 2024/2690"):
            short = "NIS2 (2024/2690)"
        if label.startswith("AI Act"):
            short = "AI Act"
        if short not in fws:
            fws.append(short)
    return lines, fws, iso_nodes, nis


# --- rama ISO 27001: rozdzialy 4-10 ---------------------------------------------------------------------
ISO_CLAUSES = {
    "core": ("Rozdziały 4-10 (wymagania)", None),
    "4": ("Kontekst organizacji", None),
    "4.1": ("Zrozumienie organizacji i jej kontekstu",
            "Określenie czynników wewnętrznych i zewnętrznych, które wpływają na zdolność organizacji do osiągnięcia celów "
            "bezpieczeństwa informacji, tak aby SZBI był dopasowany do jej kontekstu."),
    "4.2": ("Zrozumienie potrzeb i oczekiwań stron zainteresowanych",
            "Analiza potrzeb i oczekiwań stron zainteresowanych w celu uwzględnienia ich w SZBI i odniesienia się do istotnych "
            "wymagań bezpieczeństwa informacji."),
    "4.3": ("Określenie zakresu systemu zarządzania bezpieczeństwem informacji",
            "Określenie zakresu SZBI z uwzględnieniem czynników wewnętrznych i zewnętrznych, potrzeb stron zainteresowanych "
            "i zależności w środowisku działania."),
    "4.4": ("System zarządzania bezpieczeństwem informacji",
            "Ustanowienie, wdrożenie, utrzymywanie i ciągłe doskonalenie SZBI w celu skutecznego zarządzania ryzykiem "
            "bezpieczeństwa informacji i realizacji celów organizacji."),
    "5": ("Przywództwo", None),
    "5.1": ("Przywództwo i zaangażowanie",
            "Wykazanie przywództwa i zaangażowania przez wspieranie SZBI, zgodność z celami organizacji, zapewnienie zasobów, "
            "budowanie kultury bezpieczeństwa i ciągłe doskonalenie."),
    "5.2": ("Polityka",
            "Ustanowienie polityki bezpieczeństwa informacji zgodnej z celami i kierunkiem strategicznym organizacji, "
            "zawierającej zobowiązanie do spełniania wymagań, ciągłego doskonalenia i promowania bezpieczeństwa informacji."),
    "5.3": ("Role, odpowiedzialności i uprawnienia w organizacji",
            "Określenie, przypisanie i zakomunikowanie ról, odpowiedzialności i uprawnień, tak aby SZBI był skutecznie "
            "wdrożony i funkcjonował, z rozliczalnością zgodną z celami organizacji."),
    "6": ("Planowanie", None),
    "6.1": ("Działania dotyczące ryzyk i szans", None),
    "6.1.1": ("Postanowienia ogólne",
              "Ustanowienie procesu identyfikowania ryzyk i szans w obszarze bezpieczeństwa informacji z uwzględnieniem "
              "czynników wewnętrznych i zewnętrznych, potrzeb stron zainteresowanych i mających zastosowanie wymagań."),
    "6.1.2": ("Szacowanie ryzyka w bezpieczeństwie informacji",
              "Ustanowienie procesu szacowania ryzyka w zaplanowanych odstępach czasu, z określonymi kryteriami oceny "
              "zagrożeń dla poufności, integralności i dostępności, dającego spójne i porównywalne wyniki."),
    "6.1.3": ("Postępowanie z ryzykiem w bezpieczeństwie informacji",
              "Określenie procesu postępowania z ryzykiem przez dobór odpowiednich zabezpieczeń, zgodnie z kryteriami "
              "akceptacji ryzyka, i udokumentowanie go w planie postępowania z ryzykiem."),
    "6.2": ("Cele bezpieczeństwa informacji i planowanie ich osiągnięcia",
            "Ustalenie mierzalnych celów bezpieczeństwa informacji zgodnych z SZBI i celami strategicznymi oraz zaplanowanie "
            "działań z określeniem odpowiedzialności, zasobów, terminów i sposobu oceny wyników."),
    "6.3": ("Planowanie zmian",
            "Planowe wprowadzanie zmian w SZBI, tak aby były zgodne z wymaganiami bezpieczeństwa informacji, wpisywały się "
            "w istniejące procesy i uwzględniały ryzyko."),
    "7": ("Wsparcie", None),
    "7.1": ("Zasoby",
            "Zapewnienie zasobów potrzebnych do ustanowienia, wdrożenia, utrzymywania i ciągłego doskonalenia SZBI."),
    "7.2": ("Kompetencje",
            "Zapewnienie, że osoby wykonujące zadania w SZBI mają potrzebne kompetencje dzięki wykształceniu, szkoleniom "
            "lub doświadczeniu."),
    "7.3": ("Świadomość",
            "Budowanie świadomości osób na temat SZBI, ich roli w bezpieczeństwie informacji i znaczenia przestrzegania "
            "polityk i wymagań bezpieczeństwa."),
    "7.4": ("Komunikacja",
            "Ustanowienie komunikacji wewnętrznej i zewnętrznej zapewniającej terminową wymianę informacji istotnych dla SZBI "
            "i jego celów."),
    "7.5": ("Udokumentowane informacje", None),
    "7.5.1": ("Postanowienia ogólne",
              "Dokumentowanie SZBI w zakresie potrzebnym do skutecznego planowania, działania i nadzoru nad procesami."),
    "7.5.2": ("Tworzenie i aktualizowanie",
              "Właściwe tworzenie, aktualizowanie i zatwierdzanie dokumentacji SZBI wraz z nadzorem nad wersjami."),
    "7.5.3": ("Nadzór nad udokumentowanymi informacjami",
              "Zapewnienie dostępności dokumentacji SZBI dla osób, które jej potrzebują, oraz jej ochrona przed "
              "nieuprawnionym dostępem lub utratą."),
    "8": ("Działania operacyjne", None),
    "8.1": ("Planowanie i nadzór nad działaniami operacyjnymi",
            "Planowanie i nadzorowanie procesów SZBI zgodnie z wymaganiami oraz wprowadzanie korekt w odpowiedzi na ryzyka "
            "i szanse."),
    "8.2": ("Szacowanie ryzyka w bezpieczeństwie informacji",
            "Przeprowadzanie szacowania ryzyka zgodnie z przyjętym procesem: identyfikacja, ocena i ustalenie priorytetów "
            "ryzyk bezpieczeństwa informacji."),
    "8.3": ("Postępowanie z ryzykiem w bezpieczeństwie informacji",
            "Realizacja planu postępowania z ryzykiem przez wdrożenie dobranych zabezpieczeń zgodnie z kryteriami "
            "akceptacji ryzyka."),
    "9": ("Ocena efektów działania", None),
    "9.1": ("Monitorowanie, pomiary, analiza i ocena",
            "Monitorowanie, mierzenie, analizowanie i ocena działania i skuteczności SZBI odpowiednimi metodami."),
    "9.2": ("Audyt wewnętrzny", None),
    "9.2.1": ("Postanowienia ogólne",
              "Przeprowadzanie audytów wewnętrznych w zaplanowanych odstępach czasu w celu sprawdzenia, czy SZBI spełnia "
              "wymagania ISO/IEC 27001 i jest skutecznie wdrożony i utrzymywany."),
    "9.2.2": ("Program audytów wewnętrznych",
              "Planowanie i prowadzenie audytów wewnętrznych z określeniem kryteriów, zakresu, metod i odpowiedzialności "
              "oraz przekazywanie wyników właściwemu kierownictwu."),
    "9.3": ("Przegląd zarządzania", None),
    "9.3.1": ("Postanowienia ogólne",
              "Okresowy przegląd SZBI przez najwyższe kierownictwo w celu potwierdzenia jego przydatności, adekwatności "
              "i skuteczności."),
    "9.3.2": ("Dane wejściowe do przeglądu zarządzania",
              "Uwzględnienie w przeglądzie m.in. wyników audytów, efektów działania SZBI, stanu ryzyka, możliwości "
              "doskonalenia i potrzebnych zmian."),
    "9.3.3": ("Wyniki przeglądu zarządzania",
              "Udokumentowanie wyników przeglądu, w tym decyzji dotyczących doskonalenia, zmian w SZBI i potrzebnych zasobów."),
    "10": ("Doskonalenie", None),
    "10.1": ("Ciągłe doskonalenie",
             "Identyfikowanie i wykorzystywanie możliwości ciągłego doskonalenia skuteczności SZBI."),
    "10.2": ("Niezgodność i działania korygujące",
             "Reagowanie na niezgodności przez działania korygujące, ustalenie przyczyn źródłowych i działania zapobiegające "
             "powtórzeniu, z udokumentowaniem przebiegu."),
    "annex-a": ("Deklaracja stosowania (zabezpieczenia z załącznika A)", None),
    "a.5": ("Zabezpieczenia organizacyjne", None),
    "a.6": ("Zabezpieczenia osobowe", None),
    "a.7": ("Zabezpieczenia fizyczne", None),
    "a.8": ("Zabezpieczenia technologiczne", None),
}
ISO_IG = {"Clauses": "Rozdziały 4-10 (wymagania)", "SoA": "Deklaracja stosowania (załącznik A)"}


def tr(obj, pl):
    obj.setdefault("translations", {})["pl"] = {k: v for k, v in pl.items() if v is not None}


def check(txt_pl):
    assert "–" not in txt_pl and "—" not in txt_pl, "dlugi myslnik w tlumaczeniu"


def build_key_reference_controls():
    src = os.path.join(LIBS, "key-reference-controls.yaml")
    lib = yaml.safe_load(open(src, encoding="utf-8"))
    lib["version"] = int(lib["version"]) + 1
    lib["publication_date"] = TODAY
    tr(lib, {
        "name": "Wzorcowe środki kluczowe CISO Assistant (katalog intuitem)",
        "description": "Katalog wzorcowych środków prowadzony przez intuitem: polityki, procedury, dokumenty i rejestry, "
                       "szkolenia, zdolności techniczne i fizyczne. Obejmuje zarządzanie, dostęp, ochronę danych, "
                       "odporność, prywatność, AI, chmurę i bezpieczeństwo fizyczne. Każdy środek ma w adnotacji "
                       "powiązania z ISO/IEC 27001:2022, CIS Controls v8 i innymi frameworkami oraz, gdzie to możliwe, "
                       "z NIS2 (rozporządzenie 2024/2690) i ustawą o KSC. Polskie tłumaczenie: Octopus Lab.",
    })
    pl_all, missing = [], []
    for rc in lib["objects"]["reference_controls"]:
        t = DATA["intuitem"].get(rc["ref_id"])
        if not t:
            missing.append(rc["ref_id"])
            continue
        lines, fws, iso_nodes, nis = parse_annotation(rc.get("annotation"))
        ann = ["Źródło: katalog wzorcowych środków intuitem (CISO Assistant Key Reference Controls)."]
        if lines:
            ann.append("Powiązania w katalogu:")
            ann += ["- " + ln for ln in lines]
        ann += nis_ksc_lines(iso_nodes, nis)
        footer = "Źródło: katalog intuitem" + (", powiązany z: " + ", ".join(fws) if fws else "") + "."
        desc = (t["description"].rstrip() + "\n\n" + footer) if t.get("description") else footer
        pl = {"name": t["name"], "description": desc, "annotation": "\n".join(ann)}
        if rc.get("typical_evidence"):
            pl["typical_evidence"] = [DATA["typical_evidence"].get(e, e) for e in rc["typical_evidence"]]
        tr(rc, pl)
        pl_all.append(json.dumps(pl, ensure_ascii=False))
    check("\n".join(pl_all) + json.dumps(lib["translations"]["pl"], ensure_ascii=False))
    out = os.path.join(OUT, "key-reference-controls.yaml")
    open(out, "w", encoding="utf-8").write(yaml.safe_dump(lib, allow_unicode=True, sort_keys=False, width=110))
    print(out, "wersja", lib["version"], "srodkow", len(lib["objects"]["reference_controls"]),
          "bez tlumaczenia:", missing or "brak")


def build_iso27001():
    src = os.path.join(LIBS, "iso27001-2022.yaml")
    lib = yaml.safe_load(open(src, encoding="utf-8"))
    lib["version"] = int(lib["version"]) + 1
    lib["publication_date"] = TODAY
    lib_pl = {
        "name": "Norma międzynarodowa ISO/IEC 27001:2022",
        "description": "Bezpieczeństwo informacji, cyberbezpieczeństwo i ochrona prywatności - Systemy zarządzania "
                       "bezpieczeństwem informacji - Wymagania (wersja polska: PN-EN ISO/IEC 27001:2023-08). "
                       "Polskie tłumaczenie zabezpieczeń i rozdziałów: Octopus Lab.",
        "copyright": "To jest zarys normy ISO/IEC 27001:2022. Pełną normę można kupić na https://www.iso.org/standard/27001, "
                     "a wersję polską w Polskim Komitecie Normalizacyjnym.",
    }
    tr(lib, lib_pl)
    pl_all = [json.dumps(lib_pl, ensure_ascii=False)]
    missing = []
    iso = DATA["iso27001_annex_a"]
    for rc in lib["objects"]["reference_controls"]:
        t = iso.get(rc["ref_id"])
        if not t:
            missing.append(rc["ref_id"])
            continue
        num = rc["ref_id"][2:]
        ann = [f"Źródło: ISO/IEC 27001:2022, załącznik A, zabezpieczenie {rc['ref_id']} "
               f"(wytyczne wdrożenia: ISO/IEC 27002:2022, pkt {num})."]
        ann += nis_ksc_lines([rc["ref_id"].lower()])
        pl = {"name": t["name"],
              "description": t["description"].rstrip() + "\n\nŹródło: ISO/IEC 27001:2022, załącznik A.",
              "annotation": "\n".join(ann)}
        tr(rc, pl)
        pl_all.append(json.dumps(pl, ensure_ascii=False))
    fw = lib["objects"]["framework"]
    tr(fw, {"name": lib_pl["name"], "description": lib_pl["description"]})
    for ig in fw.get("implementation_groups_definition") or []:
        if ig["ref_id"] in ISO_IG:
            tr(ig, {"name": ISO_IG[ig["ref_id"]]})
    for node in fw["requirement_nodes"]:
        key = node["urn"].split(":")[-1]
        ref = node.get("ref_id") or ""
        if ref in iso:
            t = iso[ref]
            pl = {"name": t["name"], "description": t["description"] if node.get("description") else None}
        elif key in ISO_CLAUSES:
            name, desc = ISO_CLAUSES[key]
            pl = {"name": name, "description": desc if node.get("description") else None}
        else:
            missing.append(key)
            continue
        if node.get("assessable"):
            extra = nis_ksc_lines([ref.lower() or key])
            if extra:
                pl["annotation"] = "\n".join(extra)
        tr(node, pl)
        pl_all.append(json.dumps(pl, ensure_ascii=False))
    check("\n".join(pl_all))
    out = os.path.join(OUT, "iso27001-2022.yaml")
    open(out, "w", encoding="utf-8").write(yaml.safe_dump(lib, allow_unicode=True, sort_keys=False, width=110))
    print(out, "wersja", lib["version"], "zabezpieczen", len(lib["objects"]["reference_controls"]),
          "wezlow", len(fw["requirement_nodes"]), "bez tlumaczenia:", missing or "brak")


if __name__ == "__main__":
    build_key_reference_controls()
    build_iso27001()
