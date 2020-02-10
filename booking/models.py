from django.db import models


# Create your models here.
class ItemOwner(models.Model):
    pass


class BookingItem(models.Model):
    """
    Model to connect a booking with a related object.

    :quantity: Quantity of booked items.
    :subtotal (optional): Field for storing the price of each individual item.
    :booked_item: Connection to related booked item.
    :booking: Connection to related booking.

    properties:
    :price: Returns the full price for subtotal * quantity.
    """
    pass


class Booking(models.Model):
    """
    Model to contain information about a booking.

    :forename (optional): First name of the user.
    :surname (optional): Last name of the user.
    :email: Email of the user.
    :date_from (optional): From when the booking is active.
    :date_until (optional): Until when the booking is active.
    :time_period (optional): How long the period from date_from will be.
    :creation_date: Date of the booking.
    :total (optional): Field for storing a total of all items.
    :currency (optional): If total is uses, we usually also need a currency.

    """
    pass
