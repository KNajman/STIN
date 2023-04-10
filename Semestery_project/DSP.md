# Dokument specifikace požadavků

## Projekt: Bankovní systém

### 1. Úvod

Cílem semestrální práce je vytvořit bankovní systém, který bude umožňovat uživatelům vytvářet a spravovat účty, provádět platby a převody mezi účty. Systém má být realizován tak, aby byl dostupný z jakéhokoliv zařízení s přístupem na internet. Z toho vyplývá rozdělení na frontend a backend. Frontend bude realizován pomocí HTML, CSS a JavaScriptu. Backend bude realizován pomocí Pythonu a Flasku.


DSP
	- blokově: “částka: všechno se se s ni provádí”
Zadání:
	- co řeším, jak, dokument, pomoci jakých textologii
	
	- system pro bank. Obyčejný informační systém
	- potžebuje klienta, účty, kliets se účty otevírají, posílají peníze
	- Klient má účet
	- use case: 1. Platba (in, out, operations:+, -, měna), měna operaci počet: 1-n (externí zdroj dat), ná zákldadě měny rozhoduje o účtu stržení. 2. Přihlášení (přihlásím se - uvidím pohyby a zůstatek): dvoufázový (osobní číslo v aplikaci a kód do e-mailu)
	- jak se realizují platby? (Náhodný generátor pro částku a měnu)
	- rozhraní (UI): musí fungovat na PC a mobilu, tlačítko platba, výpisy, (částka a měna)
	- historie všech operací pro uživatele 
	- vytvoření nového uživatele - může být vytvořen ručně (2-3 testovacích klienta)
	- 1 účet, více měn
	- záporný zůstatek nemůže nastat
	- aktuální kurz 🙂 česká národní banka https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt;jsessionid=8BF1C86A067EBBFABDF02CA6291B7538?date=08.03.2023
	- pouze aktuální kurz
	- soubory: 3 - info o účtu, měně a historii
	- backend někde běží + frontend (UI) a jejich komunikace 
	- může být webowka

## Bodové zadání:
1. Bankovní informační systém
2. základní stavební bloky
   1. účet (číslo, měna)
   2. měna účtu
   3. platba
   4. vložení peněz na účet
3. data:
   1. uživatel (jméno a příjmení, email)
   2. účet (číslo, vlastník, měna)
4. Use cases:
   1. vlož peníze
   2. vlož peníze + převod pokud se jedná o jinou měnu ve které nemá klient vedený účet
   3. platba u obchodníka
   4. platba u obchodníka + převod mezi měnou
   5. přehlášení k účtu (uživatelské jmeno, PIN)
   6. dvoufázové ověření uživatele při přihlášení (email, osobní číslo)
   7. výpis účtu (pohyby, zůstatky, dle měn)
5. UI:
	1. musí běžet na PC i mobilním telefonu
	2. bez omezení na technologie, oddělený backend a frontend
6. Podmínky odevzdání:
   1. DSP (odevzdání do 22. 4. včetně emailem na roman.spanek@tul.cz)
   2. ukázka repo + commits + PULL REQUESTs 
   3. funkční CI/CD pro testování a nasazení
   4. pokrytí kódy testy na 70%, získané z CI/CD, tedy na přímo v IDE
   5. ukázka je aplikace funguje

-------


## množina všech požadavků

<!-- tabulka -->

## 2. Funkcionality
 - Registrace uživatele
 - Přihlášení uživatele
 - Práce s účtem viz. tabulka 1
 - Odhlášení uživatele

## 3. Use cases (scénáře použití)
### 3.1. Registrace uživatele
1. Uživatel vyplní registrační formulář s údaji
2. Uživatel potvrdí formulář
3. Uživatel je upozorněn na úspěšnou registraci případně upozorněn na chybu a je vyzvák k opravě
4. Uživatel je přesměrován na přihlašovací stránku
   
### 3.2. Přihlášení uživatele
1. Uživatel vyplní příhlašovací údaje
2. Uživatel potvrdí přihlášení
3. Uživatel je upozorněn na úspěšné přihlášení případně upozorněn na chybu a je vyzván k opravě
4. Uživatel je přesměrován na stránku s účtem
   
### 3.3. Práce s účtem
| Požadavek číslo | Popis požadavku                                                   |
| --------------- | ----------------------------------------------------------------- |
| 1               | Vložení peněžních prostředků na účet v zadané měně                |
| 2               | Vybrání peněžních prostředků z účtu v zadané měně                 |
| 3               | Převod peněžních prostředků na jiný účet s možností konverze měny |
| 4               | Konverze měny                                                     |
| 5               | Platba u obchodníka                                               |

### 3.3.1. Připsání peněžních prostředků na účet v zadané měně

Účet []