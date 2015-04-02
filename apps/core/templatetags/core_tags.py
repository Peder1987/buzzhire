from django import template
from copy import copy


register = template.Library()

@register.filter
def get_field_title(object, field_name):
    """Loads the practioner model based on its pk.
    
    Usage:
    
        {{ object|get_field_title:'my_field_name' }}
    """
    return object._meta.get_field(field_name).verbose_name


@register.filter
def get_field_value(object, field_name):
    """Outputs the value of an object's field.
    Equivalent to {{ object.field_name }}.
    
    Usage:
    
        {{ object|get_field_value:'my_field_name' }}
    """
    return getattr(object, field_name)


@register.filter
def instances_and_widgets(bound_field):
    """Returns a list of two-tuples of instances and widgets, designed to
    be used with ModelMultipleChoiceField and CheckboxSelectMultiple widgets.
    
    Allows templates to loop over a multiple checkbox field and display the
    related model instance, such as for a table with checkboxes.
      
    Usage:
        {% for instance, widget in form.my_field_name|instances_and_widgets %}
            <p>{{ instance }}: {{ widget }}</p> 
        {% endfor %}
    """
    instance_widgets = []
    index = 0
    for instance in bound_field.field.queryset.all():
         widget = copy(bound_field[index])
         # Hide the choice label so it just renders as a checkbox
         widget.choice_label = ''
         instance_widgets.append((instance, widget))
         index += 1
    return instance_widgets


@register.filter
def startswith(test_string, start_string):
    """Returns whether comparison string starts with the original string.
    Usage:
    
      {% if test_string|startswith:start_string %}
          <p>'{{ test_string }}' starts with '{{ start_string }}'!
      {% endif %}
    """
    return test_string.startswith(start_string)
