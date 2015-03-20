##
#    Copyright (C) 2013 Jessica Tallon & Matt Molyneaux
#
#    This file is part of Inboxen.
#
#    Inboxen is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Inboxen is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with Inboxen.  If not, see <http://www.gnu.org/licenses/>.
##

import os

from django.conf import settings, urls
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _

from two_factor.views import core as twofactor

from website import views
from website.views import error
from website.forms import PlaceHolderPasswordChangeForm

urls.handler400 = error.BadRequest.as_view()
urls.handler403 = error.PermissionDenied.as_view()
urls.handler404 = error.NotFound.as_view()
urls.handler500 = error.ServerError.as_view()

# If you're debugging regex, test it out on http://www.debuggex.com/ first - M
urlpatterns = urls.patterns('',
    urls.url(r'^$', views.Index.as_view(), name='index'),
    urls.url(r'^huh', views.TemplateView.as_view(template_name='huh.html', headline=_('Huh?')), name='huh'),
    urls.url(r'^stats', views.StatsView.as_view(), name='stats'),

    # inbox views
    urls.url(r'^inbox/add/', views.InboxAddView.as_view(), name='inbox-add'),
    urls.url(r'^inbox/edit/(?P<inbox>[a-zA-Z0-9\.]+)@(?P<domain>[a-zA-Z0-9\.]+)', views.InboxEditView.as_view(), name='inbox-edit'),

    urls.url(r'^inbox/attachment/(?P<attachmentid>\d+)/(?P<method>\w+)', views.AttachmentDownloadView.as_view(), name='email-attachment'),
    urls.url(r'^inbox/(?P<inbox>[a-zA-Z0-9\.]+)@(?P<domain>[a-zA-Z0-9\.]+)/email/(?P<id>[a-fA-F0-9]+)', views.EmailView.as_view(), name='email-view'),
    urls.url(r'^inbox/(?P<inbox>[a-zA-Z0-9\.]+)@(?P<domain>[a-zA-Z0-9\.]+)/(?P<page>\d+)', views.SingleInboxView.as_view(), name='single-inbox'),
    urls.url(r'^inbox/(?P<inbox>[a-zA-Z0-9\.]+)@(?P<domain>[a-zA-Z0-9\.]+)/', views.SingleInboxView.as_view(), name='single-inbox'),
    urls.url(r'^inbox/(?P<page>\d+)', views.UnifiedInboxView.as_view(), name='unified-inbox'),
    urls.url(r'^inbox/', views.UnifiedInboxView.as_view(), name='unified-inbox'),

    # form inlines
    urls.url(r'^forms/inbox/edit/(?P<inbox>[a-zA-Z0-9\.]+)@(?P<domain>[a-zA-Z0-9\.]+)', views.FormInboxEditView.as_view(), name='form-inbox-edit'),

    # user views
    urls.url(r'^user/login/', views.LoginView.as_view(), name='user-login'),
    urls.url(r'^user/home/(?P<page>\d+)', views.UserHomeView.as_view(), name='user-home'),
    urls.url(r'^user/home/', views.UserHomeView.as_view(), name='user-home'),
    urls.url(r'^user/search/(?P<q>.*)/(?P<page>\d+)', views.SearchView.as_view(), name='user-search'),
    urls.url(r'^user/search/(?P<q>.*)/', views.SearchView.as_view(), name='user-search'),
    urls.url(r'^user/search/', views.SearchView.as_view(), name='user-search'),
    urls.url(r'^user/searchapi/(?P<q>.*)/', views.SearchApiView.as_view(), name='user-searchapi'),


    urls.url(r'^user/account/security/password', 'django.contrib.auth.views.password_change',
        {
            'template_name': 'user/account/password.html',
            'post_change_redirect': reverse_lazy('user-security'),
            'password_change_form': PlaceHolderPasswordChangeForm,
            'extra_context': {
                'headline': _('Change Password'),
            },
        },
        name='user-password',
    ),
    urls.url(r'^user/account/security/setup', views.TwoFactorSetupView.as_view(), name='user-twofactor-setup'),
    urls.url(r'^user/account/security/backup', views.TwoFactorBackupView.as_view(), name='user-twofactor-backup'),
    urls.url(r'^user/account/security/disable', views.TwoFactorDisableView.as_view(), name='user-twofactor-disable'),
    urls.url(r'^user/account/security/qrcode', twofactor.QRGeneratorView.as_view(), name='user-twofactor-qrcode'),
    urls.url(r'^user/account/security', views.TwoFactorView.as_view(), name='user-security'),

    urls.url(r'^user/account/liberate/download', views.LiberationDownloadView.as_view(), name='user-liberate-get'),
    urls.url(r'^user/account/liberate', views.LiberationView.as_view(), name='user-liberate'),
    urls.url(r'^user/account/delete', views.AccountDeletionView.as_view(), name='user-delete'),
    urls.url(r'^user/account/username', views.UsernameChangeView.as_view(), name='user-username'),
    urls.url(r'^user/account/', views.GeneralSettingsView.as_view(), name='user-settings'),
    urls.url(r'^user/logout/', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='user-logout'),

    # other apps
    urls.url(r'^blog/', urls.include("blog.urls")),
    urls.url(r'^click/', urls.include("redirect.urls")),
    urls.url(r'^help/tickets/', urls.include("tickets.urls")),
    urls.url(r'^help/', urls.include("termsofservice.urls")),
    urls.url(r'^source/', urls.include("source.urls")),
)

if settings.ENABLE_REGISTRATION:
    urlpatterns += urls.patterns('',
        urls.url(r'^user/register/status', views.TemplateView.as_view(template_name='user/register/software-status.html', headline=_('We\'re not stable!')), name='user-status'),
        urls.url(r'^user/register/success', views.TemplateView.as_view(template_name='user/register/success.html', headline=_('Welcome!')), name='user-success'),
        urls.url(r'^user/register/', views.UserRegistrationView.as_view(), name='user-registration'),
    )

if ("INBOXEN_ADMIN_ACCESS" in os.environ and os.environ["INBOXEN_ADMIN_ACCESS"]) or settings.DEBUG:
    admin.autodiscover()

    urlpatterns += urls.patterns('',
        urls.url(r'^admin/', urls.include(admin.site.urls)),
    )
