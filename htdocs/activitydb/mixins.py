from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from djangocosign.models import UserProfile
from activitydb.models import Country as ActivityCountry

from django.core.exceptions import PermissionDenied

class LoggedInMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)
