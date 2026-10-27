# CISO Assistant by Octopus Lab: jednorazowe ustawienia nowej instancji.
# Uruchamiane przez kontener huey przy pierwszym starcie (znacznik db/.octopus-init),
# pozniejsze zmiany w Ustawieniach nie sa nadpisywane.
from global_settings.models import GlobalSettings

g, _ = GlobalSettings.objects.get_or_create(name="general", defaults={"value": dict(GlobalSettings.GENERAL_DEFAULT_VALUE)})
value = dict(g.value or {})
value["default_language"] = "pl"
# PLN, bo formularz Ustawien akceptuje tylko waluty z listy (symbol "zł" blokowal zapis ustawien)
value["currency"] = "PLN"
g.value = value
g.save()
print("octopus-init: domyslny jezyk pl, waluta PLN")
