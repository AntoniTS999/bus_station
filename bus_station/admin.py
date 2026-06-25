from django.contrib import admin

from bus_station.models import Bus, Order, Trip, Facility, Ticket

class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [TicketInline]

admin.site.register(Bus)
admin.site.register(Order, OrderAdmin)
admin.site.register(Trip)
admin.site.register(Facility)
admin.site.register(Ticket)
