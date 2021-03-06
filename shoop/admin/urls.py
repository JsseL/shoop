# -*- coding: utf-8 -*-
# This file is part of Shoop.
#
# Copyright (c) 2012-2015, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import unicode_literals
from django.conf.urls import patterns
from django.shortcuts import redirect
from shoop.admin.module_registry import get_module_urls
from shoop.admin.utils.urls import admin_url, AdminRegexURLPattern
from shoop.admin.views.dashboard import DashboardView
from shoop.admin.views.menu import MenuView
from shoop.admin.views.search import SearchView
import django.contrib.auth.views as auth_views
import warnings


def login(request, **kwargs):
    if not request.user.is_anonymous():  # No need to log in
        return redirect("shoop_admin:dashboard")
    return auth_views.login(request, **kwargs)


def get_urls():
    urls = []
    urls.extend(get_module_urls())

    urls.extend([
        admin_url(r'^$', DashboardView.as_view(), name='dashboard'),
        admin_url(r'^search/$', SearchView.as_view(), name='search'),
        admin_url(r'^menu/$', MenuView.as_view(), name='menu'),
        admin_url(
            r'^login/$',
            login,
            kwargs={"template_name": "shoop/admin/auth/login.jinja"},
            name='login',
            require_authentication=False
        ),
        admin_url(
            r'^logout/$',
            auth_views.logout,
            kwargs={"template_name": "shoop/admin/auth/logout.jinja"},
            name='logout',
            require_authentication=False
        ),
    ])

    for u in urls:  # pragma: no cover
        if not isinstance(u, AdminRegexURLPattern):
            warnings.warn("Admin URL %r is not an AdminRegexURLPattern" % u)

    return tuple(urls)

urlpatterns = patterns('', *get_urls())
