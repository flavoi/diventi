from django.shortcuts import render, get_object_or_404
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from .models import DiventiComment


class CommentPromoteToggleView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        comment_id = self.kwargs.get('pk') 
        comment = get_object_or_404(DiventiComment, pk=comment_id)
        user = self.request.user
        if user.is_authenticated():
            if user in comment.promotions.all():
                comment.promotions.remove(user)                           
            else:
                comment.promotions.add(user)
                messages.success(self.request, 'Comment has been promoted!')
        next = 'landing:home'
        return reverse_lazy(next)


class CommentPromoteToggleAPIView(APIView):

    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, pk=None):
        comment = get_object_or_404(DiventiComment, pk=pk)
        user = self.request.user
        updated = False
        promoted = False
        if user.is_authenticated():
            if user in comment.promotions.all():
                comment.promotions.remove(user)
                promoted = False
            else:
                comment.promotions.add(user)
                promoted = True
            updated = True
        promotions = {
            'updated': updated,
            'promoted': promoted,
        }
        return Response(promotions)



