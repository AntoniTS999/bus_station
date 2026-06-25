from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from bus_station.models import Bus, Trip, Facility, Order, Ticket


class FacilitySerializer(ModelSerializer):
    class Meta:
        model = Facility
        fields = ["id", "name"]



class BusSerializer(ModelSerializer):
    class Meta:
        model = Bus
        fields = ["id", "name", "number_of_seats", "is_mini", "facilities"]
        read_only_fields = ["id"]

class BusRetrieveSerializer(BusSerializer):
    facilities = FacilitySerializer(many=True, read_only=True)

class BusListSerializer(BusSerializer):
    facilities = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

class TripSerializer(ModelSerializer):

    class Meta:
        model = Trip
        fields = ["id", "source", "destination", "departure", "bus"]

class TripListSerializer(ModelSerializer):
    bus_name = serializers.CharField(source="bus.name", read_only=True)
    bus_number_of_seats = serializers.IntegerField(source="bus.number_of_seats", read_only=True)

    class Meta:
        model = Trip
        fields = ["id", "source", "destination", "departure", "bus_name", "bus_number_of_seats"]

class TripRetrieveSerializer(TripSerializer):
    bus = BusRetrieveSerializer(read_only=True)


class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "seat", "trip"]

class OrderSerializer(ModelSerializer):
    tickets = TicketSerializer(many=True)
    class Meta:
        model = Order
        fields = ["id", "created_at", "tickets"]

    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")
        order = Order.objects.create(**validated_data)
        for ticket in tickets_data:
            Ticket.objects.create(order=order, **ticket)
        return order