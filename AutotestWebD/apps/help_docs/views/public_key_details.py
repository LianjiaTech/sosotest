
from django.shortcuts import render

def PublicKeyDetails(request):
    context = {}
    return render(request,"help_docs/publicKeyDetails.html",context)


def ReadMeDetails(request):
    context = {}
    return render(request,"help_docs/readmeDetails.html",context)

def pythonModeDetails(request):
    context = {}
    context['host'] = request.get_host()
    return render(request,"help_docs/pythonmodeDetails.html",context)