from django import template

register = template.Library()

@register.filter
def translate_month(month):
    months = {
        'Enero':'01',
        'Febrero':'02',
        'Marzo':'03',
        'Abril':'04',
        'Mayo':'05',
        'Junio':'06',
        'Julio':'07',
        'Agosto':'08',
        'Septimebre':'09',
        'Octubre':'10',
        'Noviembre':'11',
        'Diciembre':'12'
    }

    return months[month]
