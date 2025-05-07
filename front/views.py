from django.shortcuts import render

from config.settings import CURRENT_HOST


def comments(request):
    return render(request, 'comments.html', context={'current_host': CURRENT_HOST})