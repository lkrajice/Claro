# Co je tento projekt

Je to rychlá týmová práce pro naši střední školu


## Spuštění projektu

Nejprve je nutné nainstalovat samotné django pro projekt. Ujistěte se, že máte nainstalovaný program
pip. V adresáři projektu, tam, kde je umístěn _manage.py_, proveďte
```
pip install -r requirements.txt
```

Nyní je potřeba stáhnout si všechny CSS, JS blbosti, které používáme a nedáváme blbě do repozitáře.
Ujistěte se, že máte nainstalovaný program bower. V adresáři projektu, tam, kde je umístěn
_bower.json_, proveďte
```
bower update
```

Vše je staženo, je nutno vytvořit lokální databázi a stustit server pomocí
```
./manage.py migrate
./manage.py runserver
```

Defaultně na localhost:8000
