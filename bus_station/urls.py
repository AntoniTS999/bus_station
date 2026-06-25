from django.urls import path, include
from rest_framework.routers import DefaultRouter

from bus_station.views import BusViewSet, TripViewSet, FacilityViewSet, OrderViewSet

app_name = "bus_station"

router=DefaultRouter()
router.register("busses", BusViewSet)
router.register("trips", TripViewSet)
router.register("facilities", FacilityViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [
    path("", include(router.urls))
]