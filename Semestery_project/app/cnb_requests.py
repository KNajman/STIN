import requests


def get_currency_exchange_rate(currency_code, date=None):
    try:
        if date:
            url = f"https://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_ostatnich_men/kurzy.txt?date={date}"
        else:
            url = "https://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/denni_kurz.txt"
        if currency_code == "CZK":
            return 1.0
        r = requests.get(url)
        r.raise_for_status()
        lines = r.text.splitlines()
        # line format: country|currency|amount|code|rate
        for line in lines:
            fields = line.split("|")
            if len(fields) < 5:
                continue
            if fields[3] == currency_code:
                amount = float(fields[2].replace(",", "."))
                rate = float(fields[4].replace(",", "."))
                return rate / amount
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def get_currency_list():
    try:
        url = "https://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/denni_kurz.txt"
        r = requests.get(url)
        r.raise_for_status()
        lines = r.text.splitlines()
        # line format: country|currency|amount|code|rate
        currency_list = []
        for line in lines:
            fields = line.split("|")
            if len(fields) < 5:
                continue
            currency_list.append(fields[3])

        currency_list.remove("kód")
        currency_list.insert(0, "CZK")
        return currency_list

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return [
            "AUD",
            "BRL",
            "BGN",
            "CNY",
            "DKK",
            "EUR",
            "PHP",
            "HKD",
            "INR",
            "IDR",
            "ISK",
            "ILS",
            "JPY",
            "ZAR",
            "CAD",
            "KRW",
            "HUF",
            "MYR",
            "MXN",
            "XDR",
            "NOK",
            "NZD",
            "PLN",
            "RON",
            "SGD",
            "SEK",
            "CHF",
            "THB",
            "TRY",
            "USD",
            "GBP",
        ]


if __name__ == "__main__":
    print(get_currency_list())
