from django.db import models
from django.core.urlresolvers import reverse
from .slugs import unique_slugify


class SlugModel(models.Model):
    """Abstract model mixin for models with a slug field."""
    slug = models.SlugField(
            unique=True,
            help_text="Used to build the URL.")

    def save(self, *args, **kwargs):
        if not self.pk:
            # Save a unique slug when creating for first time
            unique_slugify(self, str(self))
        return super(SlugModel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """Returns the absolute url, using the url name '<model_name>_detail'.
        """
        return reverse('%s_detail' % self._meta.model_name,
                       kwargs={'slug': self.slug})

    class Meta:
        abstract = True
