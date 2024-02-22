from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.files.storage import FileSystemStorage

def home(request):
    if request.method == "POST":
        request_file = request.FILES['document'] if 'document' in request.FILES else None
        if request_file:
            fs = FileSystemStorage()
            file = fs.save(request_file.name, request_file)
            fileurl = fs.url(file)
            return render(request, 'customize.html', {})
    return render(request, 'uploadFile.html', {})
