from django.shortcuts import render

# Create your views here.

def main(request):
    return render(request, 'main.html')

def create_group(request):
    return render(request, 'create_group.html')

def test(request):
    return render(request, 'test.html')