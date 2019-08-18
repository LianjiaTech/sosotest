from django.shortcuts import render,HttpResponse

def jsoncn(request):
    print(str(request))
    context = {"jsonstr":request.GET.get("json","")}
    return render(request, "littletool/jsoncn.html", context)
