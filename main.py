import pandas as pd

df = pd.read_csv("hotels.csv", dtype={"id": str})
df_cards = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cards_security = pd.read_csv("card_security.csv", dtype=str)


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
        """Book a hotel by changing its availability to NO"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Check if the hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False


class SpaHotel(Hotel):
    def book_spa_package(self):
        pass


class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here is your booking data.
        Name: {self.customer_name}
        Hotel name: {self.hotel.name}
        """
        return content


class SpaTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your SPA reservation!
        Here are your SPA booking data.
        Name: {self.customer_name}
        Hotel name: {self.hotel.name}
        """
        return content


class CreditCard:
    def __init__(self, number, expiration, holder):
        # self.number = input("Enter the credit card number: ")
        # self.expiration = input("Enter the expiration date of the credit card: ")
        # self.holder = input("Enter the cardholder of the credit card: ")
        # self.cvc = input("Enter the CVC of the credit card: ")
        self.cvc = None
        self.number = number
        self.expiration = expiration
        self.holder = holder
        self.card_data = {"number": self.number,
                          "expiration": self.expiration,
                          "holder": self.holder,
                          "cvc": self.cvc}

    def validate(self, cvc):
        self.cvc = cvc
        self.card_data["cvc"] = self.cvc

        if self.card_data in df_cards:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_cards_security.loc[df_cards_security["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False


print(df)
hotel_ID = input("Enter the ID of the Hotel: ")
hotel = SpaHotel(hotel_ID)

if hotel.available():
    credit_card = SecureCreditCard("1234", "12/26", "JOHN SMITH")
    if credit_card.validate("123"):
        if credit_card.authenticate(given_password="mypass"):
            hotel.book()
            name = input("Enter a name for the reservation: ")
            reservation_ticket = ReservationTicket(customer_name=name, hotel_object=hotel)
            print(reservation_ticket.generate())

            spa = input("Would you like to book a spa package as well? ").lower()
            if spa in ["yes", "y"]:
                hotel.book_spa_package()
                spa_ticket = SpaTicket(customer_name=name, hotel_object=hotel)
                print(spa_ticket.generate())
        else:
            print("Credit card authentication failed")
    else:
        print("There was a problem with your payment")
else:
    print("The Hotel is not available")
