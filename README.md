==================================================  
## VOLBY 2017 > CSV SCRAPER  
==================================================  

Script je určen k získání a uložení výsledků parlamentních voleb v ČR v roce 2017.  
Na adrese https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ  
získá data o výsledcích pro obce a uloží je do přehledné tabulky.  
Výstupním souborem je tabulka ve formátu CSV.  

__Program vyžaduje nainstalovaný interpret Python.__  
K ověření dostupné verze python zadejte v terminálu:
```bash
python --version
```


## Návod ke spuštění  

Pro správnou funkci vytvořte pro script vlastní virtuální prostředí a nainstalujte potřebné knihovny.  

Pro vytvoření vlastního virtuálního prostředí spusťte ve složce se scriptem terminál a zapište příkaz : 
```bash
python -m venv myenv
```
 
Následně aktivujte vlastní virt. prostředí pomocí příkazu.
```bash
myenv\Scripts\activate             # pro CMD
.\myenv\Scripts\Activate.ps1       # pro PowerShell
source myenv/bin/activate          # pro MacOS/Linux
```

Po úspěšné aktivaci virtuálního prostředí se v terminálu zobrazí `(myenv) cesta k souboru.`  

### Instalace knihoven  

Nainstalujte pro správný běh potřebné moduly s pomocí requirements.txt    
V terminálu zadejte příkaz: 
```bash
pip install -r requirements.txt
```

Po instalaci modulů můžete script spustit zadáním příkazu: `python main.py`  
a využít funkce arghelp, která zobrazí vhodné a dostupné argumenty

Pro úspěšné stažení a uložení dat s výsledky je v terminálu nutno 
zadat dva požadované argumenty ve správném formátu.
```bash
python main.py "url_uzemniho_celku" "Vysledny_soubor.csv"
```

př. pro výsledky celku Praha zadejte:  
```bash
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100" "vysledky_Praha.csv" 
```
Script data z url stáhne a uloží do souboru CSV ve složce kde je script umístěn.  


  


