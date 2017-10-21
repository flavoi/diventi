from django.shortcuts import render
from django.contrib import messages


class DiventiActionMixin:
    """ Disable redirect for update and creation views. """

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super(DiventiActionMixin, self).form_valid(form)