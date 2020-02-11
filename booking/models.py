from django.db import models


# Create your models here.
class Merchant(models.Model):
    """
    Model to contain information about the merchant

    :name: Name of the merchant.
    :address: Address of the merchant.
    :phone: Phone contact of the merchant.
    :email: Emais of the merchant.
    """
    pass


class BookingItem(models.Model):
    """
    Model to contain information about an available Item to be booked.

    :quantity: Quantity of available items.
    :price: Field for storing the price of each individual item.
    :currency (optional): If total is uses, we usually also need a currency.
    :email: Email of contact when the Item is booked.
    :active: if is available to be booked.
    :merchant: Connection to related merchant
    :bookingConfig: Connection to related booking configuration.
    :booking: Connection to related booking.

    properties:
    :price: Returns the full price for subtotal * quantity.
    """
    pass


class BookingConfig(models.Model):
    """
    Model to contain information about the configuration of a bookingItem.

    :bookingItem: Connection to related bookingItem.
    :date_from: From when the item is available.
    :date_until: Until when the item is available.
    :time_slot: slots to be displayed to the user when booking.
    :max_slot: max number of consecutive slots to be booked.
    :min_slot: min number of consevutive slots to be booked.
    """
    pass


class Booking(models.Model):
    """
    Model to contain information about the booking.

    :forename (optional): First name of the user.
    :surname (optional): Last name of the user.
    :email: Email of the user.
    :creation_date: Date of the booking.
    :date_from (optional): From when the booking is active.
    :date_until (optional): Until when the booking is active.
    :time_period (optional): How long the period from date_from will be.
    :slots: How many slots.
    :price: Total price of the booking.
    """
    pass
