from django.db import models
from django.contrib.sites.models import Site

class ChartbeatAnalytics(models.Model):
    site = models.ForeignKey(Site)
    analytics_code = models.IntegerField()

    def __unicode__(self):
        return u"%s" % (self.analytics_code)
    
    class Meta:
        verbose_name_plural = "Chartbeat Analytics"
