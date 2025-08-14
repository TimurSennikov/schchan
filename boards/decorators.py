import hashlib

from functools import wraps

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings

from .models import Board, Permission, get_or_create_anon

class BoardPermissionRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            board = get_object_or_404(Board, code=self.kwargs['pk'])
            anon = get_or_create_anon(request)

            codes_a = [p.code for p in anon.permissions.all()]
            codes_b = [p.code for p in board.permissions_required.all()]

            for c in codes_b:
                if c not in codes_a:
                    return render(request, 'error.html', {'error': 'Любопытно что тут? Напиши @botaner_1987 и попроси разрешения.'})

        return super().dispatch(request, *args, **kwargs)
