from django.shortcuts import render

def page_404(request):
    return render(request,"permission/page_404.html")

def not_permission(request):
    return render(request,"permission/not_permission.html")

