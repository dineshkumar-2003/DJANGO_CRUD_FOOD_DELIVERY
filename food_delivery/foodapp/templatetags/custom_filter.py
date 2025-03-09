from django import template

register = template.Library()

@register.filter(name="sort_restaurants")
def sort_restaurants_name(restaurants):
    return sorted(restaurants, key=lambda x: x.name.lower())  


@register.filter
def sort_address(queryset):
    return queryset.order_by('address')

@register.filter
def sort_contact(restaurant):
    return restaurant.order_by("contact")
    