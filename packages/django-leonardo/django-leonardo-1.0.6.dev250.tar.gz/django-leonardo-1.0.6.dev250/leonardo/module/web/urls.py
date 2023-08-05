
from __future__ import absolute_import

from django.conf.urls import include, patterns, url
from horizon_contrib.forms.views import CreateView, UpdateView
from horizon_contrib.generic.views import GenericIndexView
from leonardo.decorators import _decorate_urlconf, staff_member

# override native horizon-contrib views
GenericIndexView.template_name = "leonardo/common/_index.html"
CreateView.template_name = "leonardo/common/modal.html"
UpdateView.template_name = "leonardo/common/modal.html"


urlpatterns = patterns('',
                       url(r'^page/', include('leonardo.module.web.page.urls')),
                       url(r'^widget/', include('leonardo.module.web.widgets.urls')),
                       )

# mark all edit view as staff member required
_decorate_urlconf(urlpatterns, staff_member)
