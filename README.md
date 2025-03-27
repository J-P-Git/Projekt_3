==================================================  
## VOLBY 2017 > CSV SCRAPER  
==================================================  

Script je určen k získání a uložení výsledků parlamentních voleb v ČR v roce 2017.  
Na adrese https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ  
získá data o výsledcích pro jednotlivé obce a uloží je do souboru.  
Výstupním souborem je přehledná tabulka s výsledky ve formátu CSV.  

__Program vyžaduje nainstalovaný interpret Python 3.__  
K ověření verze zadejte v terminálu : python --version

Pro správnou funkci scriptu vytvořte vlastní virtuální prostředí.  
Spusťte ve složce se scriptem terminál a zapište příkaz : python -m venv myenv
 
Aktivujte virt. prostředí pomocí příkazu. 
* Pro cmd : myenv\Scripts\activate
* Pro PowerShell : .\myenv\Scripts\Activate.ps1
* Pro MacOS/linux : source myenv/bin/activate

Po úspěšné aktivaci virtuálního prostředí se v terminálu zobrazí (myenv) ..cesta k souboru.

Nainstalujte pro správný běh potřebné moduly pomocí requirements.txt    
V terminálu zadejte příkaz: pip install -r requirements.txt

Po instalaci modulů můžete script spustit zadáním příkazu: python main.py  

Pro úspěšné stažení a uložení dat je v terminálu nutné zadat  
dva požadované argumenty ve správném formátu.  
python main.py "url_uzemniho_celku" "Vysledny_soubor.csv"

př. pro výsledky celku Praha zadejte:  
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100" "vysledky_Praha.csv" 

V úvodu je možné využít funkce arghelp.  
Nápověda arghelp zobrazí argumenty pro všechny dostupné url.

Script data z url stáhne a uloží do souboru CSV ve složce kde je script umístěn.  


