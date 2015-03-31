from django.views.generic.edit import FormView, FormMixin
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
import logging
from .forms import ConfirmForm
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


logger = logging.getLogger('project')


class ContextMixin(object):
    """Views mixin - adds the extra_context attribute
    to the context.
    """
    extra_context = {}

    def get_context_data(self, *args, **kwargs):
        context = super(ContextMixin, self).get_context_data(*args, **kwargs)
        context.update(self.extra_context)
        return context


class ContextTemplateView(ContextMixin, TemplateView):
    """TemplateView that makes it easy to add extra context
    within the url conf.

    Usage:

        url(r'^$', ContextTemplateView.as_view(
                                template_name='template.html',
                                extra_context={'title': 'Title'}),
                                    name='home'),
    """
    pass


class TabsMixin(object):
    """Mixin for adding the tabs to a page context.

    Adds 'tabs' and 'page_title' to the context.

    For child pages of tab pages, you can specify which tab is
    active by setting the active_tab_name attribute to the url name
    of the relevant tab.
    
    Usage:

        class MySectionTabsMixin(TabsMixin):
            tabs = [
                ('Tab one', 'url/for/tab/1/'),
                ('Tab two', 'url/for/tab/2/'),
            ]
    """

    tabs = []
    active_tab_name = ''

    def get_tabs(self):
        "Returns a list of two-tuples for the tabs."
        return self.tabs

    def get_active_tab_name(self):
        "Returns the url of the active tab, to be used for child tabs."
        return self.active_tab_name

    def get_context_data(self, **kwargs):
        context = super(TabsMixin, self).get_context_data(**kwargs)

        context['tabs'] = []

        # Build the tabs from the tabs tuple
        tabs = self.get_tabs()
        active_detected = False
        for title, url in tabs:
            tab = {'title': title,
                    'url': url}
            if tab['url'] == self.request.get_full_path():
                active_detected = True
                # Set this tab as being active
                tab['active'] = True
                context['page_title'] = tab['title']
            elif url == self.get_active_tab_name():
                # Make the tab active for child pages
                tab['active'] = True
            else:
                tab['active'] = False
            context['tabs'].append(tab)
        if not active_detected:
            # Make the first tab active
            context['tabs'][0]['active'] = True

        # Add page title
        for tab in context['tabs']:

                break

        return context


class MultiFormViewMixin(object):
    """View mixin designed to work with multiple forms on the same page.
    Only one form should be submitted.
    
    Usage:
        
        class MyFormView(MultiFormViewMixin, FormView):
            form_classes = {
                FirstFormClass: 'first',
                SecondFormClass: 'second',
            }
     
    """

    def get(self, request, *args, **kwargs):
        # Build all forms passed by get
        forms = {}
        for form_class, prefix in self.form_classes.items():
            forms[prefix] = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(forms=forms))

    def form_invalid(self, form):
        forms = {form.prefix: form}
        for form_class, prefix in self.form_classes.items():
            if prefix != form.prefix:
                forms[prefix] = self.get_form(form_class, suppress_bind=True)
        return self.render_to_response(self.get_context_data(forms=forms))

    def get_form(self, form_class, suppress_bind=False):
        # Pass the form_class to get_form_kwargs
        return form_class(**self.get_form_kwargs(form_class, suppress_bind))

    def get_form_kwargs(self, form_class, suppress_bind=False):
        # Set the prefix on the form
        if suppress_bind:
            # If another form was posted, we don't want to bind the data
            # to the form
            form_kwargs = {}
        else:
            form_kwargs = super(MultiFormViewMixin, self).get_form_kwargs(
                                                                    form_class)
        form_kwargs['prefix'] = self.form_classes[form_class]
        return form_kwargs

    def get_form_class(self, request):
        if request.method == 'POST':
            # Determine which form was posted.
            for form_class, prefix in self.form_classes.items():
                # If the submit button matches the prefix, it was that form
                if '%s_submit' % prefix in request.POST:
                    return form_class
        else:
            # We only use this from the post() method
            raise Exception('MultiFormViewMixin.get_form_class() should ' \
                            'only be called from post().')

    def get_context_data(self, *args, **kwargs):
        context = super(MultiFormViewMixin, self).get_context_data(*args,
                                                                 **kwargs)
        for form_class, prefix in self.form_classes.items():
            context['%s_form' % prefix] = context['forms'][prefix]
        return context


class CanEditObject(object):
    """Views mixin - only allow users who can edit
    the object.
    
    Designed for use with views that extend SingleObjectMixin.
    """

    def get_object(self, *args, **kwargs):
        object = super(CanEditObject, self).get_object(*args, **kwargs)
        if not object.can_edit(self.request.user):
            raise PermissionDenied
        return object


class ConfirmationMixin(FormMixin):
    "Generic confirmation view mixin."

    template_name = 'form_page.html'
    form_class = ConfirmForm
    question = None
    cancel_url = ''
    action_icon = 'confirm'
    cancel_icon = 'undo'

    def get_form_kwargs(self):
        form_kwargs = super(ConfirmationMixin, self).get_form_kwargs()
        form_kwargs.update({
            'cancel_url': self.get_cancel_url(),
            'question': self.get_question(),
            'action_icon': self.action_icon,
            'cancel_icon': self.cancel_icon,
        })
        return form_kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(ConfirmationMixin, self).get_context_data(*args,
                                                                 **kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        return context

    def get_cancel_url(self):
        "Returns url to link to if they cancel."
        return self.cancel_url

    def get_question(self):
        "Returns question to ask."
        return self.question


class OwnerOnlyMixin(object):
    """Mixin for a DetailView - restricts the view to the user who owns
    the model in question, or a site admin.
    'Ownership' is determined by a 'user' field on the model.
    """
    def dispatch(self, request, *args, **kwargs):
        # If the user is not logged in, give them the chance to
        if self.request.user.is_anonymous():
            return redirect_to_login(self.request.path)
        elif not self.request.user.is_admin:
            if self.get_object().user != self.request.user:
                # The user doesn't 'own' the object
                raise PermissionDenied
        return super(OwnerOnlyMixin, self).dispatch(request, *args, **kwargs)
