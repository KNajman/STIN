# Dokument specifikace požadavků

## Projekt: Bankovní systém

### 1. Úvod

Cílem semestrální práce je vytvořit bankovní systém, který umožní uživateli vytvářet a spravovat účty, provádět platby a převody mezi účty. 
Systém má být realizován tak, aby byl dostupný z jakéhokoliv zařízení s přístupem na internet.

### 1.1 Zadání projektu z přednášky
DSP - dokument specifikace požadavků, v něm je požadován návrh systému, který bude realizován. Je nutné, specifikovat jak a co bude realizováno, a s jakými prostředky. V DSP by se měl nacházet následující obsah:
- blokové UML schéma čásky a operace které se s ní provádí
- system pro bank. Obyčejný informační systém
- potžebuje klienta, účty, kliets se účty otevírají, posílají peníze
- Klient má účet
- use case: 
    1. Platba (in, out, operations:+, -, měna), měna operaci počet: 1-n (externí zdroj dat), ná zákldadě měny rozhoduje o účtu stržení. 2. Přihlášení (přihlásím se - uvidím pohyby a zůstatek): dvoufázový (osobní číslo v aplikaci a kód do e-mailu)
- jak se realizují platby? (Náhodný generátor pro částku a měnu)
- rozhraní (UI): musí fungovat na PC a mobilu, tlačítko platba, výpisy, (částka a měna)
- historie všech operací pro uživatele 
- vytvoření nového uživatele nebo předvytvořit řučně (2-3 testovací klienti)
- 1 účet, více měn
- na účtu nemůže nastat záporný zůstatek 
- aktuální kurz měn se bere z české národní banky https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt;jsessionid=8BF1C86A067EBBFABDF02CA6291B7538?date=08.03.2023
- zajímá nás pouze aktuální kurz
- soubory: 3 - info o účtu, měně a historii
- backend někde běží + frontend (UI) a jejich komunikace 
- ideální implementací je webová stránka

### 1.2 Bodové zadání:
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

## 2. Realizace
### 2.1. Technologie
- Frontend
	- HTML
	- CSS
	- JavaScript
- Backend
	- Python
	- Flask
	- Docker
	- WSGI

## 3. Funkcionality
 - Registrace uživatele
 - Přihlášení uživatele
 - Práce s účtem viz. tabulka 1
 - Odhlášení uživatele

## 4. Use cases (scénáře použití)

### 4.1. UML diagram

![UML částka](/UML%20castka.png)

### 4.2. Registrace uživatele
1. Uživatel vyplní registrační formulář s údaji
2. Uživatel potvrdí formulář
3. Uživatel je upozorněn na úspěšnou registraci případně upozorněn na chybu a je vyzvák k opravě
4. Uživatel je přesměrován na přihlašovací stránku
   
### 4.3. Přihlášení uživatele
1. Uživatel vyplní příhlašovací údaje
2. Uživatel potvrdí přihlášení
3. Uživatel je upozorněn na úspěšné přihlášení případně upozorněn na chybu a je vyzván k opravě
4. Uživatel je přesměrován na stránku s účtem
   
### 4.4. Práce s účtem
| Požadavek číslo | Popis požadavku                                                   |
| --------------- | ----------------------------------------------------------------- |
| 1               | Vložení peněžních prostředků na účet v zadané měně                |
| 2               | Vybrání peněžních prostředků z účtu v zadané měně                 |
| 3               | Převod peněžních prostředků na jiný účet s možností konverze měny |
| 4               | Konverze měny                                                     |
| 5               | Platba u obchodníka                                               |
| 6               | Přehled účtu                                                      |

### 4.5. Odhlášení uživatele
1. Uživatel potvrdí odhlášení
2. uživatel je odhlášen
3. uživatel je upozorněn na úspěšné odhlášení
4. uživatel je přesměrován na přihlašovací stránku

## 5. Designová a implementační omezení

## 6. Závislosti
- API od ČNB na získání jednotlivých kurzů v podobě, která fungvala k 17.4.2022 na https://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/denni_kurz.txt (ukázka jaký formát je v souboru)

			18.04.2023 #75
		země|měna|množství|kód|kurz
		Austrálie|dolar|1|AUD|14,364
		Brazílie|real|1|BRL|4,330
		Bulharsko|lev|1|BGN|11,952
		Čína|žen-min-pi|1|CNY|3,101
		Dánsko|koruna|1|DKK|3,137
		EMU|euro|1|EUR|23,375
		Filipíny|peso|100|PHP|37,885
		Hongkong|dolar|1|HKD|2,715
		Indie|rupie|100|INR|25,984
		Indonesie|rupie|1000|IDR|1,436
		Island|koruna|100|ISK|15,615
		Izrael|nový šekel|1|ILS|5,855
		Japonsko|jen|100|JPY|15,915
		Jižní Afrika|rand|1|ZAR|1,173
		Kanada|dolar|1|CAD|15,929
		Korejská republika|won|100|KRW|1,618
		Maďarsko|forint|100|HUF|6,290
		Malajsie|ringgit|1|MYR|4,806
		Mexiko|peso|1|MXN|1,186
		MMF|ZPČ|1|XDR|28,757
		Norsko|koruna|1|NOK|2,039
		Nový Zéland|dolar|1|NZD|13,255
		Polsko|zlotý|1|PLN|5,062
		Rumunsko|leu|1|RON|4,735
		Singapur|dolar|1|SGD|15,998
		Švédsko|koruna|1|SEK|2,069
		Švýcarsko|frank|1|CHF|23,770
		Thajsko|baht|100|THB|62,158
		Turecko|lira|1|TRY|1,099
		USA|dolar|1|USD|21,312
		Velká Británie|libra|1|GBP|26,524

- Poskytovatelé služeb GitHub, Render
- 