from django import forms
from django.template.context import Context
from django.template.loader import render_to_string
from django.forms.widgets import TextInput
from crispy_forms.helper import FormHelper
from crispy_forms import layout


class ConfirmForm(forms.Form):
    """A general form for confirming things.
    
    Instantiate with:
    
    - question: text that will be asked on the page, default 'Are you sure?'
    - action_text: confirm submit button text, default 'Confirm'
    - cancel_text: confirm submit button text, default 'Cancel'
    
    
    Usage:
    
        form = ConfirmForm(question='Lorem ipsum?',
                       action_text='Yes, do it.',
                       cancel_url=reverse('object_detail', object.pk),
        )
    """

    def __init__(self, *args, **kwargs):
        self.cancel_url = kwargs.pop('cancel_url')
        self.question = kwargs.pop('question', 'Are you sure?')
        self.action_text = kwargs.pop('action_text', 'Confirm')
        self.cancel_text = kwargs.pop('cancel_text', 'Cancel')
        self.cancel_icon = kwargs.pop('cancel_icon', None)
        self.action_icon = kwargs.pop('action_icon', None)

        super(ConfirmForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(layout.HTML(self.get_inner_html()))

    def get_inner_html(self):
        return render_to_string('includes/forms/confirm_form_inner.html',
                            {'question': self.question,
                             'action_text': self.action_text,
                             'cancel_text': self.cancel_text,
                             'cancel_url': self.cancel_url,
                             'action_icon': self.action_icon,
                             'cancel_icon': self.cancel_icon})


class UsabilityFormMixin(object):
    """Helps with usability on mobile devices.
    Adds some widget attributes to certain fields."""

    # Some attributes to add to widgets to make them more usable on mobile
    USABILITY_WIDGET_ATTRS = {'autocapitalize': 'off', 'autocorrect': 'off'}

    def __init__(self, *args, **kwargs):
        super(UsabilityFormMixin, self).__init__(*args, **kwargs)
        # Go through the fields
        for field_name in self.fields:
            field = self.fields[field_name]
            # Add certain attributes to the text inputs
            # to make them easier to use on mobile
            if isinstance(field.widget, TextInput):
                field.widget.attrs.update(self.USABILITY_WIDGET_ATTRS)


class CrispyFormMixin(object):
    """Form mixin to add a standard submit button and crispyform helper
    to a form.
    """
    submit_name = 'submit'
    submit_text = 'Submit'
    submit_context = {}
    submit_template_name = 'includes/forms/buttons.html'
    top_html = None
    top_html_dict = {}
    bottom_html = None
    bottom_html_dict = {}
    form_tag = True
    wrap_fieldset_title = ''  # The title of the fieldset to wrap the form in

    def __init__(self, *args, **kwargs):
        super(CrispyFormMixin, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # Allow forms to easily override the form_tag
        self.helper.form_tag = self.form_tag

        # Wrap the whole form in a fieldset, if wrap_fieldset is specified
        if self.wrap_fieldset_title:
            fieldset_kwargs = [self.wrap_fieldset_title]
            fieldset_kwargs.extend(self.fields.keys())
            self.helper.layout = layout.Layout(
                layout.Fieldset(*fieldset_kwargs)
            )

        if self.submit_name:
            self.helper.layout.append(self.get_submit_button())

        if self.top_html:
            self.helper.layout.insert(0, layout.HTML(
                                        self.top_html % self.top_html_dict))

        if self.bottom_html:
            self.helper.layout.append(layout.HTML(
                                    self.bottom_html % self.bottom_html_dict))

    def get_full_submit_name(self):
        if self.prefix:
            return '%s_%s' % (self.prefix, self.submit_name)
        else:
            return self.submit_name

    def get_submit_button(self):
        # Use the template instead - good for adding extra stuff
        # such as icons and colours
        context = {
            'submit_name': self.get_full_submit_name(),
            'submit_text': self.submit_text,
        }
        context.update(self.submit_context)
        return layout.HTML(render_to_string(
                                self.submit_template_name, context))
