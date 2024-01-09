from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
def test(request):
    return render(request, 'uploadFile.html', {})