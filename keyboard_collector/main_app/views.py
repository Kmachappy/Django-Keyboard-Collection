from django.shortcuts import render
from .models import Keyboard

# class Keyboard:
#     def __init__(self, name, type, description, price):
#         self.name = name
#         self.type = type
#         self.description = description
#         self.price = price

# keyboards = [
#     Keyboard('Keyboard 1', 'Type 1', 'Description 1', 'Price 1'),
#     Keyboard('Keyboard 2', 'Type 2', 'Description 2', 'Price 2'),
#     Keyboard('Keyboard 3', 'Type 3', 'Description 3', 'Price 3'),
    
# ]


# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def keyboards_index(request):
    keyboards = Keyboard.objects.all()
    return render(request, 'keyboards/index.html', {'keyboards': keyboards})