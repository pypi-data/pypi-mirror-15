#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) Pootle contributors.
#
# This file is a part of the Pootle project. It is distributed under the GPL3
# or later license. See the LICENSE file for a copy of the license and the
# AUTHORS file for copyright and authorship information.

from django.conf.urls import patterns, url


from .views import PootleLoginView, SocialVerificationView


urlpatterns = patterns(
    '',
    url(r"^login/$",
        PootleLoginView.as_view(),
        name="account_login"),
    url(r'^social/verify/$',
        SocialVerificationView.as_view(),
        name='pootle-social-verify'),
)
