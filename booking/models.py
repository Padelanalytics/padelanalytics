from django.db import models


# Create your models here.
CURRENCY_CHOICES = (("EURO", "EURO"), ("DOLLAR", "DOLLAR"))


class Merchant(models.Model):
    """
    Model to contain information about the merchant

    :name: Name of the merchant.
    :address: Address of the merchant.
    :phone: Phone contact of the merchant.
    :email: Email of the merchant.
    :active: if is available to be booked.
    """
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=60)
    phone = models.CharField(max_length=22)
    email = models.EmailField()
    active = models.BooleanField(default=True)


class BookingItem(models.Model):
    """
    Model to contain information about an available Item to be booked.

    :items: Quantity of available items.
    :price: Field for storing the price of each individual item.
    :currency: If total is uses, we usually also need a currency.
    :email: Email of contact when the Item is booked.
    :active: if is available to be booked.
    :merchant: Connection to related merchant
    :bookingConfig: Connection to related booking configuration.
    :booking: Connection to related booking.
    """
    items = models.PositiveSmallIntegerField()
    price = models.PositiveSmallIntegerField()
    currency = models.CharField(
        max_length=10,
        choices=CURRENCY_CHOICES,
        default="EURO")
    email = models.EmailField()
    active = models.BooleanField(default=True)


class BookingConfig(models.Model):
    """
    Model to contain information about the configuration of a bookingItem.

    :bookingItem: Connection to related bookingItem.
    :date_from: From when the item is available.
    :date_until: Until when the item is available.
    :time_slot: slots to be displayed to the user when booking.
    :max_slots: max number of consecutive slots to be booked.
    :min_slots: min number of consevutive slots to be booked.
    """
    booking_item = models.ForeignKey(BookingItem, on_delete=models.CASCADE)
    time_from = models.TimeField()
    time_until = models.TimeField()
    time_slot = models.TimeField()
    max_slots = models.PositiveSmallIntegerField()
    min_slots = models.PositiveSmallIntegerField()


class Booking(models.Model):
    """
    Model to contain information about the booking.

    :forename: First name of the user.
    :surname: Last name of the user.
    :email: Email of the user.
    :creation_date: Date of the booking.
    :date_from: From when the booking is active.
    :slots: How many slots.
    :price: Total price of the booking.
    """
    creation_date = models.DateTimeField(auto_now_add=True)
    forename = models.CharField(max_length=20)
    surename = models.CharField(max_length=20)
    email = models.EmailField()
    date_from = models.DateTimeField()
    slots = models.PositiveSmallIntegerField()
    price = models.PositiveSmallIntegerField()
