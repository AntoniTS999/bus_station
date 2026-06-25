from django.db import models
from app import settings


class Facility(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Facilities"

class Bus(models.Model):
    name = models.TextField()
    number_of_seats = models.IntegerField()
    facilities = models.ManyToManyField(Facility)

    class Meta:
        verbose_name_plural = "Buses"

    def __str__(self):
        return f"(Bus(id={self.id}, name={self.name})"

    @property
    def is_mini(self):
        return self.number_of_seats <= 10


class Trip(models.Model):
    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    departure = models.DateTimeField()
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name="trips")

    class Meta:
        indexes = [
            models.Index(fields=["source", "destination"]),
            models.Index(fields=["departure"]),
        ]

    def __str__(self):
        return f"{self.source} to {self.destination} at {self.departure}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")

    def __str__(self):
        return f"Order{self.id}, created at {self.created_at}"


class Ticket(models.Model):
    seat = models.PositiveIntegerField()
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["seat", "trip"], name="unique_ticket_seat_trip"),
        ]

    def clean(self):
        if not (1 <= self.seat <= self.trip.bus.number_of_seats):
            raise ValueError(f"Seat must be in range 1 to {self.trip.bus.number_of_seats}")

    def __str__(self):
        return f"Trip: {self.trip} - Seat: {self.seat}"




