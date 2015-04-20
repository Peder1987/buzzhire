from djmoney.forms.widgets import MoneyWidget
from django.forms.widgets import TextInput


class Bootstrap3SterlingMoneyWidget(MoneyWidget):
    """Bootstrap 3 style money widget for GBP.
    Usage:
    
        in __init__ method:
        
        amount, currency = self.fields['my_field_name'].fields
        self.fields['my_field_name'].widget = Bootstrap3SterlingMoneyWidget(
           amount_widget=amount.widget, currency_widget=widgets.HiddenInput)
    """
    def format_output(self, rendered_widgets):
        return ("""<div class="input-group">
            <span class="input-group-addon">&pound;</span>
            %s%s
            </div>""" % tuple(rendered_widgets))


class Bootstrap3TextInput(TextInput):
    """Bootstrap 3 style text input.
    Usage:
    
        
    """
    def __init__(self, *args, **kwargs):
        self.addon_before = kwargs.pop('addon_before', '')
        self.addon_after = kwargs.pop('addon_after', '')
        super(Bootstrap3TextInput, self).__init__(*args, **kwargs)

    def render(self, *args, **kwargs):
        output = ''
        if self.addon_before:
            output += '<span class="input-group-addon">%s</span>' % self.addon_before
        output += super(Bootstrap3TextInput, self).render(*args, **kwargs)
        if self.addon_after:
            output += '<span class="input-group-addon">%s</span>' % self.addon_after
        return '<div class="input-group">%s</div>' % output
