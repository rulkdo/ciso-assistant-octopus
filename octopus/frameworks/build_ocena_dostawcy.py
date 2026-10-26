# -*- coding: utf-8 -*-
"""Biblioteka CISO Assistant: Ocena dostawcy ICT (NIS2/KSC) - Octopus Lab.

Polski odpowiednik "Vendor Due Diligence" intuitem, zbudowany na wzorcu "Polityka bezpieczenstwa lancucha dostaw"
(kryteria w skali 0-2, wymagania umowne, czynniki z art. 8 ust. 2 i art. 67b ustawy o KSC, pkt 5 zalacznika 2024/2690).
Uzywany w ocenach podmiotow zewnetrznych (Podmioty zewnetrzne, Oceny podmiotow) i w audycie dostawcy.
Wynik: ../libraries/octopus-lab-ocena-dostawcy-ict.yaml
Uruchom: python3 octopus/frameworks/build_ocena_dostawcy.py
"""
import datetime
import os
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "libraries", "octopus-lab-ocena-dostawcy-ict.yaml")
FW = "urn:octopuslab:risk:framework:ocena-dostawcy-ict"
NODE = "urn:octopuslab:risk:req_node:ocena-dostawcy-ict:"
P, PO = "PEL", "POD"

# grupa, nazwa grupy, [(ref, nazwa, kryterium, skala 0/1/2, podstawa, typowy dowod, grupy wdrozeniowe)]
GROUPS = [
    ("A", "Dostęp i konta", [
        ("OD-01", "Bezpieczeństwo kont klienta u dostawcy",
         "Konta podmiotu w panelu dostawcy są chronione uwierzytelnianiem wieloskładnikowym, a dostawca powiadamia "
         "o logowaniach i zmianach.",
         ("brak MFA", "MFA bez powiadomień o logowaniach i zmianach",
          "MFA odporne na phishing (klucz FIDO2), powiadomienia i dziennik zdarzeń"),
         "2024/2690 pkt 11.6, 11.7; ISO/IEC 27001:2022 A.5.17, A.8.5",
         "Zrzut ustawień bezpieczeństwa konta (rodzaj MFA, powiadomienia, dziennik).", [PO, P]),
        ("OD-02", "Dostęp personelu dostawcy",
         "Personel dostawcy ma dostęp do systemów i danych podmiotu tylko w niezbędnym zakresie, z MFA i z rejestrowaniem "
         "działań.",
         ("dostęp bez ograniczeń albo brak informacji", "zasady opisane, bez potwierdzenia",
          "minimalne uprawnienia, MFA i rejestrowanie potwierdzone w umowie lub raporcie"),
         "2024/2690 pkt 5.1.4; ISO/IEC 27001:2022 A.5.20, A.8.2",
         "Umowa lub regulamin, opis dostępu personelu dostawcy, raport z audytu.", [P]),
        ("OD-03", "Weryfikacja osób dostawcy (art. 8f)",
         "Osoby dostawcy realizujące w podmiocie zadania z art. 8 lub 11 ustawy o KSC zostały sprawdzone w Krajowym "
         "Rejestrze Karnym i zobowiązane do poufności. Nie dotyczy dostawców bez takich zadań.",
         ("brak weryfikacji", "zobowiązanie do poufności bez informacji z KRK",
          "informacja z KRK i zobowiązanie do poufności dla każdej osoby"),
         "Art. 8f ustawy o KSC; ISO/IEC 27001:2022 A.6.1, A.6.6",
         "Informacja z KRK, podpisane zobowiązania do poufności.", [P]),
    ]),
    ("B", "Incydenty", [
        ("OD-04", "Informowanie o incydentach",
         "Dostawca informuje podmiot o incydentach dotyczących jego usług w ustalonym terminie i wskazuje kontakt.",
         ("brak zobowiązania", "tylko strona statusu", "zobowiązanie umowne z terminem (np. 24 h) i kontaktem"),
         "Art. 8 ust. 1 pkt 4 ustawy o KSC; 2024/2690 pkt 5.1.4; ISO/IEC 27001:2022 A.5.20, A.5.24",
         "Klauzula umowy lub regulaminu, adres strony statusu, kontakt awaryjny.", [PO, P]),
        ("OD-05", "Współpraca przy obsłudze incydentu",
         "Dostawca przekazuje informacje i logi potrzebne do obsługi incydentu i do zgłoszenia do CSIRT w terminach "
         "24 h i 72 h.",
         ("brak współpracy", "współpraca deklarowana bez szczegółów", "zakres, terminy i kanał współpracy opisane w umowie"),
         "Art. 11 ustawy o KSC; 2024/2690 pkt 3.5, 5.1.4",
         "Klauzula umowy, procedura dostawcy.", [P]),
    ]),
    ("C", "Ciągłość i wyjście", [
        ("OD-06", "Dostępność i wsparcie",
         "Dostawca gwarantuje dostępność usługi i wsparcie odpowiednie do jej krytyczności.",
         ("brak SLA", "SLA bez kar umownych", "SLA z karami i wsparcie 24/7 dla usług krytycznych"),
         "Art. 8 ust. 1 pkt 2 lit. e i f ustawy o KSC; ISO/IEC 27001:2022 A.5.20, A.5.30",
         "SLA, regulamin, cennik wsparcia.", [PO, P]),
        ("OD-07", "Kopie i odtwarzanie po stronie dostawcy",
         "Dostawca wykonuje kopie danych podmiotu i potrafi je odtworzyć.",
         ("brak kopii", "kopie bez testów i bez odtworzenia na żądanie", "kopie z testami i odtworzenie na żądanie"),
         "2024/2690 pkt 4.2; ISO/IEC 27001:2022 A.8.13",
         "Opis kopii w regulaminie lub umowie, wynik odtworzenia.", [PO, P]),
        ("OD-08", "Możliwość wyjścia",
         "Dane i konfiguracje (np. domeny, strefy DNS, certyfikaty) można wyeksportować i przenieść do innego dostawcy.",
         ("brak eksportu", "eksport ręczny lub niepełny", "eksport w standardowych formatach i wsparcie transferu"),
         "Art. 8 ust. 1 pkt 2 lit. e ustawy o KSC; ISO/IEC 27001:2022 A.5.23",
         "Opis eksportu, wykonany eksport testowy.", [PO, P]),
        ("OD-09", "Plan wyjścia od dostawcy",
         "Podmiot ma plan wyjścia: dostawcę zastępczego, aktualne eksporty i kopie poza dostawcą, szacowany czas "
         "przeniesienia i wynik testu wykonalności.",
         ("brak planu", "plan bez testu", "plan z aktualnym eksportem i testem wykonalności w ostatnim roku"),
         "2024/2690 pkt 4.1, 5.1; ISO/IEC 27001:2022 A.5.23, A.5.30",
         "Plan wyjścia, protokół testu przeniesienia.", [P]),
    ]),
    ("D", "Ochrona danych", [
        ("OD-10", "Powierzenie i lokalizacja danych",
         "Przetwarzanie danych osobowych przez dostawcę ma podstawę (umowa powierzenia), a dane są przetwarzane w UE "
         "albo z właściwą podstawą transferu.",
         ("brak umowy powierzenia albo transfer bez podstawy", "umowa powierzenia", "umowa powierzenia i przetwarzanie w UE"),
         "RODO art. 28, art. 44-49; ISO/IEC 27001:2022 A.5.34",
         "Umowa powierzenia (DPA), informacja o lokalizacji danych.", [PO, P]),
        ("OD-11", "Szyfrowanie, zwrot i usunięcie danych",
         "Dane są szyfrowane w transmisji i w spoczynku, a po zakończeniu umowy zwracane i usuwane.",
         ("brak informacji", "szyfrowanie w transmisji, bez zasad usunięcia",
          "szyfrowanie w transmisji i w spoczynku oraz potwierdzenie usunięcia po zakończeniu"),
         "2024/2690 pkt 9, 12.5; ISO/IEC 27001:2022 A.8.10, A.8.24",
         "Dokumentacja bezpieczeństwa dostawcy, klauzula o usunięciu danych.", [P]),
    ]),
    ("E", "Wiarygodność dostawcy (art. 8 ust. 2)", [
        ("OD-12", "Certyfikaty i niezależne potwierdzenia",
         "Praktyki bezpieczeństwa dostawcy są potwierdzone przez niezależną stronę, a zakres obejmuje usługę "
         "świadczoną podmiotowi.",
         ("brak informacji", "publiczne zasady bezpieczeństwa", "ISO/IEC 27001, SOC 2 lub równoważne z zakresem obejmującym usługę"),
         "Art. 8 ust. 2 ustawy o KSC; 2024/2690 pkt 5.1.2; ISO/IEC 27001:2022 A.5.19",
         "Certyfikat z zakresem, raport SOC 2, strona z zasadami bezpieczeństwa.", [PO, P]),
        ("OD-13", "Podatności i aktualizacje produktów",
         "Dostawca publikuje biuletyny bezpieczeństwa, usuwa podatności w określonych terminach i stosuje bezpieczny "
         "rozwój oprogramowania.",
         ("brak informacji o podatnościach", "biuletyny bez terminów", "biuletyny, terminy poprawek i opisany bezpieczny rozwój"),
         "Art. 8 ust. 2 ustawy o KSC; 2024/2690 pkt 5.1.2, 6.10; ISO/IEC 27001:2022 A.5.21, A.8.8",
         "Strona biuletynów bezpieczeństwa, polityka zgłaszania podatności.", [P]),
        ("OD-14", "Podwykonawcy dostawcy",
         "Dostawca ujawnia podwykonawców mających dostęp do usługi lub danych i stawia im te same wymagania.",
         ("brak informacji", "lista podwykonawców bez wymagań", "lista, zgoda podmiotu i te same wymagania wobec podwykonawców"),
         "2024/2690 pkt 5.1.4; ISO/IEC 27001:2022 A.5.21",
         "Lista podwykonawców, klauzula umowy.", [P]),
        ("OD-15", "Dostawca wysokiego ryzyka",
         "Sprawdzono skoordynowane oceny ryzyka Grupy Współpracy NIS i decyzje o uznaniu za dostawcę wysokiego ryzyka "
         "(art. 67b ustawy o KSC).",
         ("nie sprawdzono", "sprawdzono jednorazowo", "sprawdzane przy ocenie i raz w roku, z notatką"),
         "Art. 8 ust. 2 i art. 67b ustawy o KSC",
         "Notatka ze sprawdzenia z datą.", [PO, P]),
    ]),
    ("F", "Umowa i środki kompensujące", [
        ("OD-16", "Wymagania bezpieczeństwa w umowie",
         "Umowa zawiera: poufność, zgłaszanie incydentów, MFA i minimalne uprawnienia personelu, prawo do audytu lub "
         "raportów, zasady dla podwykonawców, zwrot i usunięcie danych.",
         ("brak wymagań", "regulamin przeczytany i porównany z wymaganiami, braki opisane",
          "wymagania zapisane w umowie lub aneksie bezpieczeństwa"),
         "Art. 8 ust. 1 pkt 2 lit. e ustawy o KSC; 2024/2690 pkt 5.1.4; ISO/IEC 27001:2022 A.5.20",
         "Umowa, aneks bezpieczeństwa albo porównanie regulaminu z wymaganiami.", [PO, P]),
        ("OD-17", "Środki kompensujące i akceptacja ryzyka",
         "Gdy dostawca nie spełnia wymagań, braki są skompensowane własnymi środkami (kopie poza dostawcą, eksporty, "
         "MFA, monitorowanie), a ryzyko jest wpisane i zaakceptowane.",
         ("braki bez reakcji", "środki kompensujące bez wpisu ryzyka", "środki kompensujące, wpis ryzyka i akceptacja kierownika"),
         "Art. 8 ust. 1 pkt 1 ustawy o KSC; 2024/2690 pkt 2.1, 5.1",
         "Rejestr ryzyka, decyzja o akceptacji, lista środków kompensujących.", [PO, P]),
    ]),
]


def build():
    nodes = []
    for gref, gname, reqs in GROUPS:
        g_urn = NODE + gref.lower()
        nodes.append({"urn": g_urn, "assessable": False, "depth": 1, "ref_id": gref, "name": gname,
                      "implementation_groups": [PO, P]})
        for ref, name, desc, (s0, s1, s2), basis, evid, igs in reqs:
            nodes.append({
                "urn": NODE + ref.lower(), "assessable": True, "depth": 2, "parent_urn": g_urn, "ref_id": ref,
                "name": name, "description": desc,
                "annotation": f"Ocena: 0 - {s0}; 1 - {s1}; 2 - {s2}.\nPodstawa: {basis}.",
                "typical_evidence": f"- {evid}",
                "implementation_groups": igs,
            })
    lib = {
        "urn": "urn:octopuslab:risk:library:ocena-dostawcy-ict",
        "locale": "pl",
        "ref_id": "ocena-dostawcy-ict",
        "name": "Ocena dostawcy ICT - NIS2/KSC (Octopus Lab)",
        "description": "Ocena bezpieczeństwa dostawcy produktów, usług i procesów ICT według polityki łańcucha dostaw "
                       "Octopus Lab: 17 kryteriów w skali 0-2, czynniki z art. 8 ust. 2 i art. 67b ustawy o KSC, pkt 5 "
                       "załącznika do rozporządzenia 2024/2690, ISO/IEC 27001:2022 A.5.19-A.5.23.",
        "copyright": "Octopus Lab",
        "version": 1,
        "publication_date": datetime.date(2026, 10, 27),
        "provider": "Octopus Lab",
        "packager": "octopuslab",
        "objects": {"framework": {
            "urn": FW, "ref_id": "ocena-dostawcy-ict", "name": "Ocena dostawcy ICT - NIS2/KSC",
            "description": "Grupy wdrożeniowe: POD - ocena podstawowa (dostawca średni lub niski, 10 kryteriów), PEL - "
                           "ocena pełna (dostawca krytyczny lub wysoki, 17 kryteriów). Dostawca krytyczny z niskim "
                           "wynikiem wymaga środków kompensujących i wpisu ryzyka.",
            "min_score": 0, "max_score": 2,
            "scores_definition": [
                {"score": 0, "name": "Nie spełnia", "description": "Brak zabezpieczenia albo brak informacji."},
                {"score": 1, "name": "Częściowo", "description": "Zabezpieczenie częściowe albo bez potwierdzenia."},
                {"score": 2, "name": "Spełnia", "description": "Zabezpieczenie pełne i potwierdzone."},
            ],
            "implementation_groups_definition": [
                {"ref_id": PO, "name": "Ocena podstawowa", "description": "Dostawca średni lub niski: 10 kryteriów."},
                {"ref_id": P, "name": "Ocena pełna", "description": "Dostawca krytyczny lub wysoki: wszystkie 17 kryteriów."},
            ],
            "requirement_nodes": nodes,
        }},
    }
    return lib


if __name__ == "__main__":
    lib = build()
    txt = yaml.safe_dump(lib, allow_unicode=True, sort_keys=False, width=110)
    assert "–" not in txt and "—" not in txt, "dlugi myslnik"
    n = [x for x in lib["objects"]["framework"]["requirement_nodes"] if x["assessable"]]
    assert len(n) == 17 and sum(1 for x in n if PO in x["implementation_groups"]) == 10
    open(OUT, "w", encoding="utf-8").write(txt)
    print(OUT, len(txt), "kryteriow", len(n))
