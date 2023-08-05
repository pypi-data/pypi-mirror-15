# coding: utf-8
"""
Amavis management frontend.

Provides:

* SQL quarantine management
* Per-domain settings

"""

from django.utils.translation import ugettext_lazy

from modoboa.admin.models import Domain
from modoboa.core.extensions import ModoExtension, exts_pool
from modoboa.lib import parameters

from . import __version__
from . import general_callbacks
from .lib import create_user_and_policy, create_user_and_use_policy


class Amavis(ModoExtension):

    """The Amavis extension."""

    name = "modoboa_amavis"
    label = ugettext_lazy("Amavis frontend")
    version = __version__
    description = ugettext_lazy("Simple amavis management frontend")
    url = "quarantine"
    available_for_topredirection = True

    def load(self):
        from .app_settings import ParametersForm, UserSettings

        parameters.register(ParametersForm, "Amavis")
        parameters.register(UserSettings, ugettext_lazy("Quarantine"))

    def load_initial_data(self):
        """Create records for existing domains and co."""
        for dom in Domain.objects.all():
            policy = create_user_and_policy("@{0}".format(dom.name))
            for domalias in dom.domainalias_set.all():
                domalias_pattern = "@{0}".format(domalias.name)
                create_user_and_use_policy(domalias_pattern, policy)

exts_pool.register_extension(Amavis)
