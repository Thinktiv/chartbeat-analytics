from django import template
from django.db import models
from django.contrib.sites.models import Site

from django.conf import settings

from django.template import Context, loader


register = template.Library()
Analytics = models.get_model('chartbeat_analytics', 'chartbeat_analytics')

def do_get_analytics(parser, token):
    enabled = getattr(settings, "CHARTBEAT_ANALYTICS__MODEL" , False)
    if not enabled:
        return AnalyticsNode("", "", "", False)

    contents = token.split_contents()
    tag_name = contents[0]
    template_name = 'chartbeat_analytics/%s_template.html' % tag_name
    if len(contents) == 2:
        # split_contents() knows not to split quoted strings.
        code = contents[1]
    elif len(contents) == 1:
        code = None
    else:
        raise template.TemplateSyntaxError, "%r cannot take more than one argument" % tag_name
   
    if not code:
        current_site = Site.objects.get_current()
    else:
        if not (code[0] == code[-1] and code[0] in ('"', "'")):
            raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
        code = code[1:-1]
        current_site = None

    return AnalyticsNode(current_site, code, template_name, True)

@register.inclusion_tag('chartbeat_analytics/chartbeat_analytics_template_header.html')
def chartbeat_analytics_header():
    enabled = getattr(settings, "CHARTBEAT_ANALYTICS__MODEL" , False)
    return {'enabled': enabled}

class AnalyticsNode(template.Node):
    def __init__(self, site=None, code=None, template_name='chartbeat_analytics/chartbeat_analytics_template.html', enabled = True):
        self.enabled = enabled
        self.site = site
        self.code = code
        self.template_name = template_name
        
    def render(self, context):
        if not self.enabled:
            return ""
        
        content = ''
        domain = ''
        if self.site:
            domain = self.site.domain
            code_set = self.site.chartbeatanalytics_set.all()
            if code_set:
                code = code_set[0].analytics_code
            else:
                return ''
        elif self.code:
            code = self.code
        else:
            return ''
        
        if code:
            t = loader.get_template(self.template_name)
            c = Context({
                'analytics_code': code,
                'analytics_domain': domain,
            })
            return t.render(c)
        else:
            return ''
        
register.tag('chartbeat_analytics', do_get_analytics)