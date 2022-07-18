from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def keyboards_index(request):
    keyboards = Keyboard.objects.all()
    return render(request, 'keyboards_index.html')