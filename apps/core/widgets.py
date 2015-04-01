from djmoney.forms.widgets import MoneyWidget


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

