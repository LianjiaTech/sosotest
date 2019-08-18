from django.shortcuts import HttpResponse


# Create your views here.


def testcdc(request):
    return HttpResponse("""{"id":1}""")
