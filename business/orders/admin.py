from django.contrib import admin

from .models import Order, ProductOrder


# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'transaction', 'date_added', 'state', 'date_due')
    list_editable = ['state']
    list_filter = ['date_due', 'date_added', 'state']
    list_display_links = ('transaction', '__str__',)
    search_fields = ('user__username',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'user',
                'state',
            )
        }
         ),
    )


class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'number', 'order')
    list_filter = ['number']
    list_display_links = ('__str__', 'number', 'order')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'product',
                'number',
                'order'
            )
        }
         ),
    )


admin.site.register(Order, OrderAdmin)

admin.site.register(ProductOrder, ProductOrderAdmin)
