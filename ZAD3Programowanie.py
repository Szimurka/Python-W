import requests
import json

class InvoiceProgram:
    def __init__(self):
        self.invoices = []
        self.payments = []

    def add_invoice(self, amount, currency, date):
        self.invoices.append({"amount": amount, "currency": currency, "date": date})

    def add_payment(self, amount, currency, date):
        self.payments.append({"amount": amount, "currency": currency, "date": date})

    def get_exchange_rate(self, currency, date):
        response = requests.get(f"http://api.nbp.pl/api/exchangerates/rates/a/{currency}/{date}/")
        data = json.loads(response.text)
        return data["rates"][0]["mid"]

    def calculate_difference(self, invoice, payment):
        invoice_exchange_rate = self.get_exchange_rate(invoice["currency"], invoice["date"])
        payment_exchange_rate = self.get_exchange_rate(payment["currency"], payment["date"])
        difference = payment["amount"] * payment_exchange_rate - invoice["amount"] * invoice_exchange_rate
        return difference

    def save_to_file(self, filename):
        data = {
            "invoices": self.invoices,
            "payments": self.payments
        }

        with open(filename, 'w') as f:
            json.dump(data, f)

        print(f"Dane zostały zapisane do pliku {filename}")

    def run_interactive(self):
        while True:
            print("1. Dodaj fakturę")
            print("2. Dodaj płatność")
            print("3. Oblicz różnicę kursową")
            print("4. Zapisz dane do pliku")
            print("5. Wyjdź")

            option = input("Wybierz opcję: ")

            if option == "1":
                amount = float(input("Podaj kwotę faktury: "))
                currency = input("Podaj walutę faktury: ")
                date = input("Podaj datę wystawienia faktury (YYYY-MM-DD): ")
                self.add_invoice(amount, currency, date)
            elif option == "2":
                amount = float(input("Podaj kwotę płatności: "))
                currency = input("Podaj walutę płatności: ")
                date = input("Podaj datę płatności (YYYY-MM-DD): ")
                self.add_payment(amount, currency, date)
            elif option == "3":
                invoice_index = int(input("Wybierz indeks faktury: "))
                payment_index = int(input("Wybierz indeks płatności: "))
                difference = self.calculate_difference(self.invoices[invoice_index], self.payments[payment_index])
                print(f"Różnica kursowa: {difference}")
            elif option == "4":
                filename = input("Podaj nazwę pliku: ")
                self.save_to_file(filename)
            elif option == "5":
                break
            else:
                print("Nieznana opcja, spróbuj ponownie.")

    def run_batch(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)

        for invoice in data["invoices"]:
            self.add_invoice(invoice["amount"], invoice["currency"], invoice["date"])

        for payment in data["payments"]:
            self.add_payment(payment["amount"], payment["currency"], payment["date"])

        for i in range(len(self.invoices)):
            difference = self.calculate_difference(self.invoices[i], self.payments[i])
            print(f"Różnica kursowa dla faktury {i}: {difference}")

        self.save_to_file("output.json")

if __name__ == "__main__":
    program = InvoiceProgram()
    mode = input("Wybierz tryb działania programu (interaktywny/wsadowy): ")

    if mode.lower() == "interaktywny":
        program.run_interactive()
    elif mode.lower() == "wsadowy":
        filename = input("Podaj nazwę pliku z danymi: ")
        program.run_batch(filename)
    else:
        print("Nieznany tryb, spróbuj ponownie.")
