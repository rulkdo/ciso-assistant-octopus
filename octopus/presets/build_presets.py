# -*- coding: utf-8 -*-
"""Generator presetow CISO Assistant by Octopus Lab (NIS2/KSC + ISO 27001).

Dwa warianty roznia sie tylko macierza ryzyka:
  - 5x5 P x W zgodna z ISO/IEC 27005 (metodyka DOK-02),
  - 4x4 S x P Octopus Lab (skutek z klasyfikacji CIA).
Wynik: ../libraries/preset-octopus-nis2-ksc-*.yaml (montowane do /code/library/libraries).
Uruchom: python3 octopus/presets/build_presets.py
"""
import os
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "libraries")

LIB_2690 = "urn:intuitem:risk:library:annex-technical-and-methodological-requirements-nis2"
LIB_KSC = "urn:octopuslab:risk:library:ksc-obowiazki-krajowe"
LIB_ISO = "urn:intuitem:risk:library:iso27001-2022"
LIB_MAP = "urn:intuitem:risk:library:mapping-annex-technical-and-methodological-requirements-nis2-and-iso27001-2022"
LIB_CAT = "urn:intuitem:risk:library:intuitem-common-catalog"
T = "urn:intuitem:risk:threat:intuitem-common-catalog:"
OL = "urn:octopuslab:risk:threat:"

VARIANTS = [
    {
        "slug": "iso27005-5x5",
        "matrix": "urn:octopuslab:risk:library:macierz-ryzyka-5x5-pxw",
        "name": "NIS2 i KSC - Octopus Lab (macierz 5x5 ISO 27005)",
        "matrix_txt": "macierz 5x5 prawdopodobieństwo x wpływ zgodna z ISO/IEC 27005",
    },
    {
        "slug": "octopus-4x4",
        "matrix": "urn:octopuslab:risk:library:macierz-ryzyka-4x4-sxp",
        "name": "NIS2 i KSC - Octopus Lab (macierz 4x4 S x P)",
        "matrix_txt": "macierz 4x4 skutek x prawdopodobieństwo, skutek z klasyfikacji CIA aktywa",
    },
]

FLAGS = [
    "compliance", "risk_management", "risk_acceptances", "exceptions", "incidents",
    "tasks", "control_plan", "follow_up", "findings_from_requirements", "tprm", "contracts",
    "reports", "notification_center", "terminologies", "comments",
]

M = lambda n: {"interval": n, "frequency": "MONTHLY"}
Y = lambda n: {"interval": n, "frequency": "YEARLY"}
POTW = (" Czynność może być wykonywana częściej (codziennie, co tydzień); w CISO Assistant oznaczasz ją"
        " raz w miesiącu jako potwierdzenie, że w tym miesiącu była robiona. Ślad (zrzut, notatka, raport)"
        " w folderze miesiąca w archiwum dokumentów.")

TASKS = [
    ("Z-01", "Przegląd alertów monitoringu i dzienników zdarzeń", M(1),
     "Przegląd alertów z monitoringu dostępności, SIEM/EDR i dzienników zdarzeń. Zdarzenia wymagające oceny"
     " rejestrujesz jako incydenty." + POTW),
    ("Z-02", "Przegląd i instalacja aktualizacji bezpieczeństwa", M(1),
     "Sprawdzenie oczekujących aktualizacji systemów, aplikacji i urządzeń sieciowych oraz ich instalacja"
     " w terminach z procesu zarządzania podatnościami (2024/2690 pkt 6.6)." + POTW),
    ("Z-03", "Skan podatności systemów z rejestru aktywów", M(1),
     "Skan podatności wszystkich systemów wspierających usługi. Wynik jako dowód, istotne pozycje"
     " jako ustalenia w zbiorze ustaleń Skany podatności (2024/2690 pkt 6.10)."),
    ("Z-04", "Kontrola wykonania kopii zapasowych", M(1),
     "Sprawdzenie, czy wszystkie zadania kopii zakończyły się poprawnie i czy kopia odporna na usunięcie"
     " jest aktualna (2024/2690 pkt 4.2)."),
    ("Z-05", "Kontrola terminów certyfikatów, domen, licencji i umów wsparcia", M(1),
     "Przegląd dat wygaśnięcia certyfikatów, domen, licencji i umów serwisowych na najbliższe 60 dni."),
    ("Z-06", "Comiesięczny przegląd SZBI", M(1),
     "Przegląd ryzyk, incydentów, ustaleń i środków z terminami. Zaległości zgłaszasz kierownikowi podmiotu."),
    ("Z-07", "Test odtworzenia kopii (wybrany system)", M(3),
     "Odtworzenie wybranego systemu lub zbioru danych z kopii i pomiar czasu względem RTO. Protokół jako dowód"
     " (2024/2690 pkt 4.2)."),
    ("Z-08", "Przegląd kont, uprawnień i MFA", M(3),
     "Przegląd kont użytkowników, kont uprzywilejowanych i serwisowych, MFA, kluczy i tokenów API. Usunięcie"
     " zbędnych dostępów (2024/2690 pkt 11)."),
    ("Z-09", "Przegląd rejestru aktywów", M(3),
     "Aktualizacja rejestru aktywów: nowe i wycofane systemy, właściciele, klasyfikacja CIA, zależności"
     " (2024/2690 pkt 12.4)."),
    ("Z-10", "Ocena incydentów powtarzających się", M(3),
     "Przegląd incydentów z kwartału pod kątem powtarzalności, która może czynić je poważnymi"
     " (2024/2690 art. 4)."),
    ("Z-11", "Pełny test odtworzenia i ćwiczenie planu ciągłości działania", Y(1),
     "Ćwiczenie scenariusza z planu ciągłości działania z pełnym odtworzeniem kluczowej usługi. Protokół i wnioski"
     " jako dowód (2024/2690 pkt 4.1)."),
    ("Z-12", "Ćwiczenie obsługi i zgłoszenia incydentu (S46)", Y(1),
     "Ćwiczenie procedury obsługi incydentu z przygotowaniem wczesnego ostrzeżenia i zgłoszenia w terminach"
     " 24 h / 72 h. Rejestruj jako incydent z etykietą cwiczenie."),
    ("Z-13", "Szkolenie kierownika podmiotu", Y(1),
     "Szkolenie z cyberbezpieczeństwa kierownika podmiotu i osoby, której powierzono obowiązki, raz w roku"
     " kalendarzowym (ustawa o KSC, art. 8e). Zaświadczenie jako dowód."),
    ("Z-14", "Szkolenie pracowników z cyberbezpieczeństwa", Y(1),
     "Szkolenie świadomościowe pracowników i współpracowników z listą obecności (2024/2690 pkt 8)."),
    ("Z-15", "Przegląd szacowania ryzyka i planu postępowania z ryzykiem", Y(1),
     "Ponowne szacowanie ryzyka i aktualizacja planu postępowania; także po istotnej zmianie lub incydencie"
     " poważnym (2024/2690 pkt 2.1)."),
    ("Z-16", "Ocena dostawców krytycznych", Y(1),
     "Ocena bezpieczeństwa dostawców usług ICT i ich umów, plan wyjścia dla dostawców krytycznych"
     " (2024/2690 pkt 5)."),
    ("Z-17", "Przegląd polityk i procedur SZBI", Y(1),
     "Przegląd dokumentacji SZBI pod kątem aktualności i zgodności ze stanem faktycznym, nowe wersje"
     " do zatwierdzenia przez kierownika (ustawa o KSC, art. 10)."),
    ("Z-18", "Przegląd SZBI przez kierownictwo", Y(1),
     "Roczny przegląd skuteczności SZBI: wyniki audytów, incydenty, ryzyka, cele, decyzje kierownika"
     " (2024/2690 pkt 2.2, ISO/IEC 27001 rozdz. 9.3)."),
    ("Z-19", "Weryfikacja danych w wykazie podmiotów i S46", Y(1),
     "Sprawdzenie aktualności danych podmiotu, usług i osób do kontaktów w wykazie i systemie S46."),
    ("Z-20", "Audyt bezpieczeństwa systemu informacyjnego (podmiot kluczowy)", Y(3),
     "Audyt z art. 15 ustawy o KSC co najmniej raz na 3 lata, przez audytora niezaangażowanego w SZBI"
     " w roku przed audytem. Podmiot ważny może zadanie wyłączyć."),
]

SCENARIOS = [
    ("Ransomware szyfrujący systemy i kopie zapasowe",
     "Złośliwe oprogramowanie szyfruje systemy wspierające usługę oraz dostępne z sieci kopie. Usługa staje,"
     " powstaje obowiązek zgłoszenia incydentu poważnego.", [T + "ict-001", T + "ict-009"]),
    ("Przejęcie konta przez phishing lub wyciek hasła",
     "Atakujący zdobywa dane logowania pracownika lub administratora i loguje się do poczty, paneli"
     " administracyjnych lub VPN; brak MFA ułatwia atak.", [T + "ict-002", T + "ict-012"]),
    ("Atak przez dostawcę albo jego awaria",
     "Kompromitacja, awaria lub upadłość dostawcy usług ICT (chmura, hosting, MSP, oprogramowanie) przenosi się"
     " na usługi podmiotu.", [T + "ict-003", OL + "ol-004"]),
    ("Wykorzystanie niezałatanej podatności",
     "Podatność w systemie dostępnym z internetu zostaje wykorzystana przed instalacją poprawki.",
     [T + "ict-004"]),
    ("Atak DDoS i niedostępność usługi",
     "Przeciążenie łącza lub usługi powoduje niedostępność dla odbiorców.", [T + "ict-007"]),
    ("Wyciek danych",
     "Nieuprawnione ujawnienie danych klientów, kontrahentów lub pracowników, także przez nieautoryzowane"
     " usługi (shadow IT).", [T + "ict-019"]),
    ("Awaria systemu lub błąd przy zmianie konfiguracji",
     "Awaria sprzętu lub oprogramowania albo pomyłka administratora powoduje przerwę w usłudze lub osłabienie"
     " zabezpieczeń.", [T + "ict-022", OL + "ol-002"]),
    ("Niedostępność kluczowej osoby",
     "Jedyna osoba z wiedzą i dostępem do systemów jest długotrwale niedostępna.", [OL + "ol-001"]),
    ("Zdarzenie fizyczne lub środowiskowe",
     "Pożar, zalanie, brak zasilania lub kradzież sprzętu w biurze albo serwerowni.",
     [T + "ict-020", OL + "ol-005"]),
    ("Niedotrzymanie obowiązków z ustawy o KSC",
     "Spóźnione zgłoszenie incydentu, brak audytu lub dokumentacji; ryzyko kar i nakazów organu nadzoru.",
     [T + "ict-023"]),
]


def preset(v):
    scaff = [
        {"type": "risk_assessment", "name": "Szacowanie ryzyka SZBI", "risk_matrix": v["matrix"], "ref": "main_ra"},
        {"type": "compliance_assessment", "name": "Audyt NIS2: rozporządzenie 2024/2690",
         "framework": LIB_2690, "create_suggested_controls": False, "ref": "nis2_audit"},
        {"type": "compliance_assessment", "name": "Audyt KSC: obowiązki krajowe",
         "framework": LIB_KSC, "ref": "ksc_audit"},
        {"type": "findings_assessment", "name": "Analiza luk (audyt zerowy)", "category": "audit", "ref": "gap_findings"},
        {"type": "findings_assessment", "name": "Skany podatności", "category": "self_identified", "ref": "vuln_findings"},
    ]
    for ref_id, name, sched, desc in TASKS:
        scaff.append({"type": "task_template", "name": f"{ref_id} {name}", "description": desc,
                      "is_recurrent": True, "schedule": sched})
    for i, (name, desc, threats) in enumerate(SCENARIOS, 1):
        scaff.append({"type": "risk_scenario", "name": name,
                      "description": desc + " Przypisz aktywa, których dotyczy scenariusz, i oceń ryzyko.",
                      "risk_assessment_ref": "main_ra", "threat_urns": threats, "ref": f"rs_{i:02d}"})
    steps = [
        ("scope", "Kwalifikacja i zakres",
         "Ustal, czy podmiot jest kluczowy czy ważny, i wybierz grupy PK albo PW (oraz DOM dla rejestracji domen)"
         " w audycie KSC.", "compliance-assessments", "ksc_audit"),
        ("assets", "Rejestr aktywów",
         "Wpisz usługi objęte ustawą jako aktywa główne i systemy, które je wspierają, jako aktywa wspierające."
         " Nadaj klasyfikację CIA i właściciela.", "assets", None),
        ("suppliers", "Dostawcy",
         "Dodaj dostawców usług ICT i oceń krytycznych (łańcuch dostaw, 2024/2690 pkt 5).", "entities", None),
        ("gap", "Analiza luk 2024/2690",
         "Przejdź wymagania rozporządzenia i oceń stan każdego z nich. Luki zapisz jako ustalenia.",
         "compliance-assessments", "nis2_audit"),
        ("risk", "Szacowanie ryzyka",
         f"Oceń scenariusze startowe i dodaj własne. Metoda: {v['matrix_txt']}.", "risk-assessments", "main_ra"),
        ("controls", "Plan postępowania z ryzykiem",
         "Dla każdej luki i ryzyka wpisz środek bezpieczeństwa z właścicielem i terminem.", "applied-controls", None),
        ("tasks", "Harmonogram czynności",
         "Ustaw osoby odpowiedzialne w zadaniach Z-01..Z-20. Czynności częste oznaczasz raz w miesiącu.",
         "task-templates", None),
        ("incidents", "Rejestr incydentów",
         "Incydenty rejestruj w CISO Assistant; poważne zgłaszasz przez S46: 24 h, 72 h, sprawozdanie po miesiącu.",
         "incidents", None),
        ("acceptance", "Akceptacja ryzyka szczątkowego",
         "Kierownik podmiotu akceptuje ryzyko szczątkowe (ustawa o KSC, art. 8d).", "risk-acceptances", None),
    ]
    jsteps = []
    for key, title, desc, model, ref in steps:
        s = {"key": key, "title": title, "description": desc, "target_model": model}
        if ref:
            s["target_ref"] = ref
        jsteps.append(s)
    return {
        "urn": f"urn:octopuslab:risk:preset:nis2-ksc-{v['slug']}",
        "locale": "pl",
        "ref_id": f"preset-octopus-nis2-ksc-{v['slug']}",
        "name": v["name"],
        "description": (
            "Konfiguracja Octopus Lab dla podmiotów kluczowych i ważnych według ustawy o KSC (NIS2) z odniesieniem"
            " do ISO/IEC 27001:2022. Ładuje załącznik do rozporządzenia 2024/2690, obowiązki krajowe z ustawy o KSC,"
            f" ISO 27001 z mapowaniem i {v['matrix_txt']}. Tworzy audyty, szacowanie ryzyka ze scenariuszami"
            " startowymi, zbiory ustaleń, harmonogram czynności Z-01..Z-20 i ścieżkę wdrożenia."),
        "version": 1,
        "provider": "Octopus Lab",
        "packager": "octopuslab",
        "dependencies": [LIB_2690, LIB_KSC, LIB_ISO, LIB_MAP, LIB_CAT, v["matrix"]],
        "objects": {"preset": {
            "profile": {"company_size": ["micro", "sme", "large"], "industry": ["general", "critical-infrastructure"],
                        "region": ["eu"], "goal": "nis2-compliance"},
            "feature_flags": {"enable": FLAGS},
            "scaffolded_objects": scaff,
            "journey": {"steps": jsteps},
        }},
    }


if __name__ == "__main__":
    for v in VARIANTS:
        data = preset(v)
        txt = yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=110)
        assert "\u2013" not in txt and "\u2014" not in txt, "dlugi myslnik w presecie"
        fn = os.path.join(OUT, f"preset-octopus-nis2-ksc-{v['slug']}.yaml")
        open(fn, "w", encoding="utf-8").write(txt)
        print(fn, len(data["objects"]["preset"]["scaffolded_objects"]), "obiektow")
