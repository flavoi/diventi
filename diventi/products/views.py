from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.http import Http404

from diventi.core.views import DiventiActionMixin

from .models import Product
from .forms import UserCollectionUpdateForm


class ProductDetailView(DetailView):
    """
        Displays a product with all its infos.
    """
    model = Product
    context_object_name = 'product'

    # Returns only published products
    def get_queryset(self):
        qs = super(ProductDetailView, self).get_queryset()
        return qs.published()

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['form'] = UserCollectionUpdateForm(initial={'slug': self.object.slug })
        context['bought'] = self.object.user_has_already_bought(self.request.user)
        return context


class ProductUpdateView(LoginRequiredMixin, DiventiActionMixin, UpdateView):
    """
        Base update view for the product model
    """
    model = Product
    context_object_name = 'product'


class UserCollectionUpdateView(ProductUpdateView):
    """
        Adds a user to the buyers of a product.
    """
    form_class = UserCollectionUpdateForm
    success_msg = 'The product has been added to you collection!'
    template_name = 'products/product_detail.html'

    def add_to_user_collection(self):
        if not self.object.user_has_already_bought(self.request.user):
            return self.object.buyers.add(self.request.user)
        else:
            msg = 'The user has this product already.'
            raise Http404(msg)

    def form_valid(self, form):
        self.add_to_user_collection()
        return super(UserCollectionUpdateView, self).form_valid(form)

