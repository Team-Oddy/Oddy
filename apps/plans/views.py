from django.shortcuts import render, redirect

# Create your views here.

def main(request):
    return render(request, 'main.html')

def create_group(request):
    return render(request, 'create_group.html')

def test(request):
    return render(request, 'test.html')

def my_page(request):
    return render(request, 'my_page.html')



