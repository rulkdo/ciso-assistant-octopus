# CISO Assistant by Octopus Lab

Wersja CISO Assistant Community Edition (intuitem, AGPL v3) przygotowana przez Octopus Lab dla podmiotów
kluczowych i ważnych według ustawy o KSC (NIS2), z odniesieniem do ISO/IEC 27001:2022.

Bazą jest wydanie upstream **v4.1.5**. Backend i baza danych są bez zmian (oryginalny obraz intuitem),
zmieniony jest frontend i dołożone są biblioteki z presetami.

## Co zmieniliśmy względem upstream

| Obszar | Zmiana | Pliki |
|---|---|---|
| Branding | Logo "CISO Assistant by Octopus Lab" (jasne i ciemne), favicon, kolory i fonty z octopus-lab.pl (granat #0a0d1a / #141937, akcent #4f63ff, Sora + Manrope), tytuły kart, nazwa w aplikacji MFA | `frontend/octopus-brand.css`, `frontend/src/lib/brand.ts`, `frontend/src/lib/assets/octopus-logo-*.svg`, `frontend/static/` |
| Menu | Trzy kategorie na górze (Zgodność i dokumentacja, Centrum operacyjne, Administracja), reszta w "Dodatkowe" | `frontend/src/lib/components/SideBar/octopusNav.ts` |
| Teksty | Polski jako język domyślny i pierwszy na liście, poprawione nazwy (Środki zabezpieczające, Podmioty zewnętrzne, Dowody audytowe, Dashboard) | `frontend/messages/pl.json`, `en.json` |
| AGPL | W menu użytkownika link "Kod źródłowy (AGPL v3)" i "Wsparcie Octopus Lab", w oknie "O aplikacji" informacja o wersji bazowej | `SideBarFooter.svelte` |
| Biblioteki | Obowiązki krajowe z ustawy o KSC (54 wymagania, grupy PK / PW / DOM, zagrożenia OL-001..OL-005), macierze 5x5 P x W (ISO 27005) i 4x4 S x P | `octopus/libraries/` |
| Presety | "NIS2 i KSC - Octopus Lab" w dwóch wariantach macierzy: flagi funkcji, audyty 2024/2690 i KSC, szacowanie ryzyka z 10 scenariuszami, zbiory ustaleń, harmonogram Z-01..Z-20, ścieżka wdrożenia | `octopus/libraries/preset-*.yaml`, generator `octopus/presets/build_presets.py` |
| CI | Workflow budujący obraz frontendu do GHCR; workflowy upstream usunięte z tej gałęzi | `.github/workflows/octopus-frontend-image.yml` |

## Nowa instancja dla klienta

Wymagania: serwer z Dockerem i docker compose v2.24+, 2 vCPU, 4 GB RAM, domena z rekordem A na serwer, otwarte porty 80 i 443.

```bash
git clone --depth 1 --branch octopus-v4.1.5-1 https://github.com/rulkdo/ciso-assistant-octopus.git
cd ciso-assistant-octopus/octopus
cp .env.example .env            # uzupełnij CISO_DOMAIN i ACME_EMAIL
cp mail.env.example mail.env    # opcjonalnie: poczta wychodząca
mkdir -p db && sudo chown 1001:1001 db
docker compose pull
docker compose up -d
docker compose exec backend python manage.py createsuperuser
```

Pierwszy start trwa kilka minut (migracje i zapis bibliotek). Przy pierwszym starcie kontener `huey` ustawia
polski jako język domyślny i walutę zł (skrypt `octopus_init.py`, znacznik `db/.octopus-init`).

Następnie w aplikacji: **Administracja → Ścieżki** → wybierz "NIS2 i KSC - Octopus Lab" z macierzą 5x5 (ISO 27005)
albo 4x4 → nazwa domeny = nazwa klienta → zaznacz tworzenie obiektów i flagi funkcji → zastosuj.
Preset ładuje biblioteki, włącza potrzebne moduły i tworzy:

- audyt "Audyt NIS2: rozporządzenie 2024/2690" i "Audyt KSC: obowiązki krajowe" (w audycie KSC wybierz grupę PK albo PW, dla rejestratorów domen także DOM),
- "Szacowanie ryzyka SZBI" z 10 scenariuszami startowymi (przypisz aktywa i oceń),
- zbiory ustaleń "Analiza luk (audyt zerowy)" i "Skany podatności",
- 20 zadań cyklicznych Z-01..Z-20 (miesięczne, kwartalne, roczne; audyt z art. 15 co 3 lata),
- ścieżkę wdrożenia z 9 krokami.

## Istniejąca instancja (np. testowa cisorisk)

Dotyczy instancji postawionej z oryginalnego `docker-compose.yml` intuitem w wersji **v4.1.5** (sprawdź: menu
użytkownika → O aplikacji). Baza zostaje ta sama, migracji nie ma.

1. Kopia bazy: `docker compose stop backend huey && cp -a db db-kopia-$(date +%F) && docker compose start backend huey`
2. Obok `docker-compose.yml` skopiuj `octopus/docker-compose.istniejaca-instancja.yml` i katalog `octopus/libraries` jako `octopus-libraries`.
3. `docker compose -f docker-compose.yml -f docker-compose.istniejaca-instancja.yml pull frontend`
4. `docker compose -f docker-compose.yml -f docker-compose.istniejaca-instancja.yml up -d`
5. W aplikacji: Ustawienia → Ogólne → Domyślny język: polski.

Powrót do wersji intuitem: `docker compose -f docker-compose.yml up -d` (bez pliku nakładki).

Uwaga dla instancji testowej: ma wgraną starą bibliotekę "Macierze ryzyka Octopus Lab" (obie macierze w jednej).
Nowe biblioteki macierzy mają te same identyfikatory macierzy, więc na tej instancji nie stosuj presetów Octopus Lab.
Na nowych instancjach problem nie występuje.

## Wydanie nowego obrazu frontendu

Obraz buduje GitHub Actions po wypchnięciu tagu `octopus-*`:

```bash
git tag octopus-v4.1.5-2
git push origin octopus-v4.1.5-2
```

Wynik: `ghcr.io/rulkdo/ciso-assistant-octopus/frontend:octopus-v4.1.5-2`. Jeśli serwer nie może pobrać obrazu
(błąd unauthorized), ustaw w GitHub → Packages → frontend → Package settings widoczność Public.
Na serwerze zmień `OCTOPUS_FRONTEND_TAG` w `.env` i wykonaj `docker compose pull && docker compose up -d`.

## Aktualizacja do nowej wersji upstream

Backend i frontend muszą pochodzić z tej samej wersji upstream.

```bash
git remote add upstream https://github.com/intuitem/ciso-assistant-community.git   # raz
git fetch upstream --tags
git checkout -b octopus-v4.2.0 octopus-nis2
git rebase --onto v4.2.0 v4.1.5
# konflikty w .github/workflows rozwiązuj przez git rm (workflowy upstream nie są używane)
# konflikty w messages/*.json: zostaw nowe klucze upstream i nasze wartości
```

Potem: build i test lokalnie albo w Actions, tag `octopus-v4.2.0-1`, kopia bazy, zmiana `CISO_BACKEND_TAG`
i `OCTOPUS_FRONTEND_TAG` w `.env`, `docker compose pull && docker compose up -d`.

## Branding i presety: skąd się biorą

- Nazwa, linki, e-mail wsparcia, adres kodu źródłowego: `frontend/src/lib/brand.ts`.
- Logo i favicon: `python3 octopus/brand/make_brand.py` (wektor ośmiornicy z `octopus/brand/trace.py`, tekst fontem Sora zamieniony na krzywe).
- Kolory i fonty: `python3 octopus/brand/gen_theme.py > frontend/octopus-brand.css`. Fiolety i róże Tailwinda użyte na sztywno w komponentach są przemapowane na kolory marki w tym samym pliku.
- Presety: `python3 octopus/presets/build_presets.py` (nazwy zadań, scenariusze, kroki ścieżki).
- Menu: `frontend/src/lib/components/SideBar/octopusNav.ts`.

Lokalny build frontendu potrzebuje ok. 10 GB RAM, a kompilator tłumaczeń pobiera wtyczki z cdn.jsdelivr.net.

## Licencja i znak

Kod jest na licencji AGPL v3, jak upstream (`LICENSE-AGPL.txt`). Użytkownicy instancji muszą mieć dostęp do kodu
źródłowego zmienionej wersji: to repozytorium jest publiczne, a link jest w menu użytkownika. Pliki z katalogu
`enterprise/` (licencja komercyjna intuitem) nie są używane.

"CISO Assistant" to produkt intuitem. Dopisek "by Octopus Lab" oznacza konfigurację i wsparcie Octopus Lab,
a informacja o wersji bazowej intuitem jest w oknie "O aplikacji". Nazwę zmienisz w jednym miejscu (`brand.ts`).
