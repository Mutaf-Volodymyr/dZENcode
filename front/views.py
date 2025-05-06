from django.shortcuts import render

def comments(request):
    return render(request, 'comments.html')