#!/usr/bin/env bash
# CISO Assistant by Octopus Lab: przejscie istniejacej instancji v4.1.5 na wersje Octopus Lab.
# Uruchom na serwerze:
#   curl -fsSLO https://raw.githubusercontent.com/rulkdo/ciso-assistant-octopus/octopus-nis2/octopus/aktualizuj-istniejaca-instancje.sh
#   sudo bash aktualizuj-istniejaca-instancje.sh
# Skrypt sam znajduje katalog docker compose po dzialajacym kontenerze backendu, pobiera obraz frontendu
# Octopus Lab, biblioteki i nakladke compose z GitHuba, robi kopie bazy i restartuje uslugi. Bazy nie zmienia.
set -euo pipefail

REPO_RAW="${REPO_RAW:-https://raw.githubusercontent.com/rulkdo/ciso-assistant-octopus/octopus-nis2/octopus}"
FRONTEND_IMAGE="${FRONTEND_IMAGE:-ghcr.io/rulkdo/ciso-assistant-octopus/frontend:octopus-v4.1.5}"
LIBS="octopus-lab-ksc-obowiazki-krajowe.yaml octopus-lab-macierz-ryzyka-5x5-pxw.yaml octopus-lab-macierz-ryzyka-4x4-sxp.yaml preset-octopus-nis2-ksc-iso27005-5x5.yaml preset-octopus-nis2-ksc-octopus-4x4.yaml intuitem-common-catalog.yaml"
STAMP="$(date +%Y%m%d-%H%M%S)"

say() { printf '\n== %s\n' "$*"; }

CID="$(docker ps -q --filter label=com.docker.compose.service=backend | head -n1)"
if [ -z "$CID" ]; then
  echo "Nie znalazlem dzialajacego kontenera backend (docker compose). Przerywam." >&2
  exit 1
fi
label() { docker inspect -f "{{ index .Config.Labels \"$1\" }}" "$CID"; }
DIR="$(label com.docker.compose.project.working_dir)"
PROJECT="$(label com.docker.compose.project)"
CONFIGS="$(label com.docker.compose.project.config_files)"
if [ -z "$DIR" ] || [ ! -d "$DIR" ] || [ "$DIR" = "/" ] || [ -z "$PROJECT" ] || [ -z "$CONFIGS" ]; then
  echo "Nie udalo sie ustalic katalogu instancji z etykiet kontenera. Przerywam." >&2
  exit 1
fi
IFS=',' read -r -a FILES <<< "$CONFIGS"
BASE=(docker compose -p "$PROJECT")
for f in "${FILES[@]}"; do
  case "$f" in */docker-compose.octopus.yml) ;; *) BASE+=(-f "$f") ;; esac
done
OCTO=("${BASE[@]}" -f "$DIR/docker-compose.octopus.yml")

say "Instancja: projekt $PROJECT, katalog $DIR"
cd "$DIR"
for svc in backend huey frontend; do
  if ! "${BASE[@]}" config --services | grep -qx "$svc"; then
    echo "W konfiguracji brak uslugi '$svc'. Przerywam, nic nie zmienione." >&2
    exit 1
  fi
done
[ -d "$DIR/db" ] || { echo "Brak katalogu $DIR/db. Przerywam, nic nie zmienione." >&2; exit 1; }

say "Pobieranie z GitHuba (biblioteki, nakladka compose) i obrazu frontendu"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/octopus-libraries"
for f in $LIBS; do curl -fsSL "$REPO_RAW/libraries/$f" -o "$TMP/octopus-libraries/$f"; done
curl -fsSL "$REPO_RAW/docker-compose.istniejaca-instancja.yml" -o "$TMP/docker-compose.octopus.yml"
docker pull "$FRONTEND_IMAGE"

say "Kopia bazy: $DIR/db-kopia-$STAMP (backend i huey zatrzymane na czas kopii)"
"${BASE[@]}" stop huey backend
cp -a "$DIR/db" "$DIR/db-kopia-$STAMP"

say "Instalacja plikow Octopus Lab"
mkdir -p "$DIR/octopus-libraries"
cp "$TMP"/octopus-libraries/*.yaml "$DIR/octopus-libraries/"
chmod 755 "$DIR/octopus-libraries"; chmod 644 "$DIR"/octopus-libraries/*.yaml
sed "s#ghcr.io/rulkdo/ciso-assistant-octopus/frontend:octopus-v4.1.5#$FRONTEND_IMAGE#" \
  "$TMP/docker-compose.octopus.yml" > "$DIR/docker-compose.octopus.yml"

say "Start (pierwszy start backendu zapisuje biblioteki, potrwa 1-3 min)"
"${OCTO[@]}" up -d backend huey frontend
st=starting
for i in $(seq 1 72); do
  bid="$(docker ps -q --filter label=com.docker.compose.service=backend | head -n1)"
  st="$(docker inspect -f '{{ if .State.Health }}{{ .State.Health.Status }}{{ else }}{{ .State.Status }}{{ end }}' "$bid" 2>/dev/null || echo starting)"
  [ "$st" = "healthy" ] && break
  sleep 5
done
echo "Backend: $st"

say "Domyslny jezyk instancji: polski"
"${OCTO[@]}" exec -T backend python manage.py shell -c \
  "from global_settings.models import GlobalSettings as G; g=G.objects.get(name='general'); v=dict(g.value or {}); v['default_language']='pl'; g.value=v; g.save(); print('ok')" \
  || echo "Nie udalo sie ustawic jezyka, ustaw recznie: Ustawienia, Ogolne, Domyslny jezyk."

say "Aktualizacja bibliotek podmienionych przez Octopus Lab (polskie tlumaczenia)"
"${OCTO[@]}" exec -T backend python manage.py shell -c "from core.models import LoadedLibrary as L
for urn in ['urn:intuitem:risk:library:intuitem-common-catalog']:
    lib = L.objects.filter(urn=urn).first()
    print(urn, (lib.update() or 'zaktualizowana') if lib and lib.has_update else 'bez zmian')" \
  || echo "Nie udalo sie zaktualizowac bibliotek, zrob to recznie: Biblioteki, Aktualizuj."

"${OCTO[@]}" ps

QF="$(printf -- '-f %s ' "${FILES[@]}")"
cat <<EOF

Gotowe. Odswiez przegladarke (Ctrl+F5).
Kopia bazy: $DIR/db-kopia-$STAMP

Uruchamianie z nakladka Octopus Lab (np. po zmianach w compose):
  docker compose -p $PROJECT ${QF}-f $DIR/docker-compose.octopus.yml up -d
Nowsza wersja frontendu Octopus Lab (nakladka ma pull_policy: missing, wiec obraz pobierasz recznie):
  docker pull $FRONTEND_IMAGE && docker compose -p $PROJECT ${QF}-f $DIR/docker-compose.octopus.yml up -d frontend
Powrot do wygladu intuitem (baza bez zmian):
  docker compose -p $PROJECT ${QF}up -d backend huey frontend
EOF
