from django.shortcuts import render
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.mixins import UserPassesTestMixin

from diventi.blog.models import Article


class DiventiActionMixin:
    """ Disable redirect for update and creation views. """

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super(DiventiActionMixin, self).form_valid(form)


class StaffRequiredMixin:
    """ Restrict the access of a page to admins only. """

    def test_func(self):
        return self.request.user.is_staff