from djmoney.forms.widgets import MoneyWidget
from django.forms.widgets import TextInput, RadioSelect, RadioFieldRenderer


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


class AttributeStoreDict(dict):
    """Dictionary-like object that allows us to set an attribute too."""
    def __init__(self, original):
        super(AttributeStoreDict, self).__init__()
        self.__dict__ = original


class IndividualAttrsRadioFieldRenderer(RadioFieldRenderer):
    def render(self):
        """
        Outputs a <ul> for this set of choice fields.
        If an id was given to the field, it is applied to the <ul> (each
        item in the list will get an id of `$id_$i`).
        """
        a = self.attrs
        assert False
        id_ = self.attrs.get('id', None)
        start_tag = format_html('<ul id="{0}">', id_) if id_ else '<ul>'
        output = [start_tag]
        for i, choice in enumerate(self.choices):
            choice_value, choice_label = choice
            if isinstance(choice_label, (tuple, list)):
                attrs_plus = self.attrs.copy()
                if id_:
                    attrs_plus['id'] += '_{0}'.format(i)
                sub_ul_renderer = ChoiceFieldRenderer(name=self.name,
                                                      value=self.value,
                                                      attrs=attrs_plus,
                                                      choices=choice_label)
                sub_ul_renderer.choice_input_class = self.choice_input_class
                output.append(format_html('<li>{0}{1}</li>', choice_value,
                                          sub_ul_renderer.render()))
            else:
                w = self.choice_input_class(self.name, self.value,
                                            self.attrs.copy(), choice, i)
                output.append(format_html('<li>{0}</li>', force_text(w)))
        output.append('</ul>')
        return mark_safe('\n'.join(output))

class IndividualAttrsRadioSelect(RadioSelect):
    """Widget that allows you to specify custom attrs for each 
    individual choice.
    """
    renderer = IndividualAttrsRadioFieldRenderer

    def __init__(self, *args, **kwargs):
        self.individual_attrs = kwargs.pop('individual_attrs', [])
        super(IndividualAttrsRadioSelect, self).__init__(*args, **kwargs)

    def build_attrs(self, *args, **kwargs):
        final_attrs = super(IndividualAttrsRadioSelect, self).build_attrs(
                                                                    *args,
                                                                    **kwargs)

        return final_attrs
        # TODO - work out how to set an extra attribute on the dict

        new_final_attrs = AttributeStoreDict(final_attrs)
        new_final_attrs.individual_attrs = self.individual_attrs
        assert False

        return new_final_attrs

#     def get_renderer(self, name, value, attrs=None, choices=()):
#         """Returns an instance of the renderer.
#         This is lifted from RendererMixin.get_renderer(), it just passes
#         the individual_attrs to the renderer too."""
#         if value is None:
#             value = self._empty_value
#         final_attrs = self.build_attrs(attrs)
#         choices = list(chain(self.choices, choices))
#         return self.renderer(name, value, final_attrs, choices)

