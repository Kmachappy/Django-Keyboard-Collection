from django.shortcuts import render, redirect
from .models import Keyboard, Part, Cleaning
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import CleaningForm

class KeyboardCreate(CreateView):
    model = Keyboard
    fields = ['name', 'type', 'description', 'price']
    success_url = '/keyboards/'
    
class KeyboardUpdate(UpdateView):
    model = Keyboard
    fields = ['type', 'description', 'price']
 
class KeyboardDelete(DeleteView):
    model = Keyboard
    success_url = '/keyboards/'   


# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def keyboards_index(request):
    keyboards = Keyboard.objects.all()
    return render(request, 'keyboards/index.html', {'keyboards': keyboards})

def keyboards_detail(request, keyboard_id):
    keyboard = Keyboard.objects.get(id=keyboard_id)
    cleaning_form = CleaningForm()
    return render(request, 'keyboards/detail.html', {'keyboard': keyboard, 'cleaning_form': cleaning_form})

def add_cleaning(request, keyboard_id):
    # create the ModelForm using the data in request.POST
    form = CleaningForm(request.POST)
    print(form)
    # keyboard = Keyboard.objects.get(id=keyboard_id)
    # if the form is valid, save the data to the database
    if form.is_valid():
        # don't save the form to the database yet
        new_cleaning = form.save(commit=False)
        new_cleaning.keyboard_id = keyboard_id
        new_cleaning.save()
    return redirect('detail', keyboard_id=keyboard_id)

def associate_part(request, keyboard_id, part_id):
    Keyboard.objects.get(id=keyboard_id).parts.add(part_id)
    return redirect('detail', keyboard_id=keyboard_id)

