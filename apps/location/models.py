from django.contrib.gis.db import models
from .utils import GeoLocation, GeoLocationMatchException


class Postcode(models.Model):
    """A postcode is a model that represents a particular postcode,
    with a geographical point."""

    postcode = models.CharField(max_length=8, db_index=True)
    point = models.PointField()

    objects = models.GeoManager()

    def __init__(self, *args, **kwargs):
        super(Postcode, self).__init__(*args, **kwargs)
        # Store the original postcode, so we can tell if it's change
        # in the save() method
        self._original_postcode = self.postcode

    def save(self, *args, **kwargs):
        # If the postcode has changed,
        # set the point based on the postcode
        if not self.point or (self.postcode != self._original_postcode):
            try:
                geolocation = GeoLocation(self.postcode)
            except GeoLocationMatchException as e:
                # This is most likely to happen if the quota is exceeded
                raise ValidationError(
                    "Sorry, there was a problem matching that location. "
                    "Please try saving the location again, or adjusting "
                    "the postcode.")
            else:
                self.point = geolocation.point

        # Ensure we validate the model before saving
        self.full_clean()
        return super(Postcode, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.postcode

    class Meta:
        ordering = ['postcode']
