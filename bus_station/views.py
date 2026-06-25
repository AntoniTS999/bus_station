from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet
from bus_station.models import Bus, Trip, Facility, Order
from bus_station.serializers import BusSerializer, TripSerializer, TripListSerializer, BusListSerializer, \
    FacilitySerializer, BusRetrieveSerializer, TripRetrieveSerializer, OrderSerializer


class BusViewSet(ModelViewSet):
    queryset = Bus.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BusListSerializer
        elif self.action == "retrieve":
            return BusRetrieveSerializer
        else:
            return BusSerializer

    def get_queryset(self):
        if self.action in ("list", "retrieve"):
            return Bus.objects.all().prefetch_related("facilities")
        else:
            return Bus.objects.all()

class TripViewSet(ModelViewSet):
    queryset = Trip.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return TripListSerializer
        elif self.action == "retrieve":
            return TripRetrieveSerializer
        else:
            return TripSerializer


    def get_queryset(self):
        if self.action in ("list", "retrieve"):
            return Trip.objects.all().select_related("bus")
        else:
            return Trip.objects.all()

class FacilityViewSet(ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

