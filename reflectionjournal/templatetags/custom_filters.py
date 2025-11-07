from django import template

register = template.Library()

@register.filter
def minutes_to_hours_minutes(value):
    if value is None:
        return ""
    
    hours = value // 60
    minutes = value % 60
    if hours and minutes:
        if hours > 1 and minutes > 1:
            return f"{hours} hours {minutes} minutes"
        elif hours == 1:
            return f"1 hour {minutes} minutes"
        else:
            return f"{hours} hours 1 minute"
    elif hours:
        return f"{hours} hours" if hours > 1 else f"1 hour"
    elif minutes:
        return f"{minutes} minutes" if minutes > 1 else f"1 minute"
    else:
        return "0 minutes"

@register.filter
def weather_icon(condition):
    icons = {
        'Sunny': 'wi-day-sunny',
        'Partly Cloudy': 'wi-day-cloudy',
        'Cloudy': 'wi-cloudy',
        'Rainy': 'wi-rain',
        'Snow': 'wi-snow',
    }
    return icons.get(condition, '')
