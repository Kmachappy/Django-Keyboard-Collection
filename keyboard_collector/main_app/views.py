from django.shortcuts import render, redirect
from .models import Keyboard, Part, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import CleaningForm
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'keyboard-collector-y789'

class KeyboardCreate(CreateView):
    model = Keyboard
    fields = ['name', 'type', 'description', 'price']
    
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
    parts_keyboard_doesnt_have = Part.objects.exclude(id__in=keyboard.parts.all().values_list('id'))
    print(parts_keyboard_doesnt_have)
    cleaning_form = CleaningForm()
    return render(request, 'keyboards/detail.html', {
        'keyboard': keyboard, 'cleaning_form': cleaning_form,
        'parts': parts_keyboard_doesnt_have,    
    })

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

def add_photo(request, keyboard_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        # s3 is the AWS service that provides access to our buckets
        s3 = boto3.Session(profile_name='keyboardcollector').client('s3')
        # need a unique 'key' for s3 / needs file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # try to upload file to S3
        try: 
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to keyboard_id or keyboard (if you have a keyboard object)
            photo = Photo(url=url, keyboard_id=keyboard_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', keyboard_id=keyboard_id)  
        

def associate_part(request, keyboard_id, part_id):
    Keyboard.objects.get(id=keyboard_id).parts.add(part_id)
    return redirect('detail', keyboard_id=keyboard_id)

class PartList(ListView):
    model = Part

class PartDetail(DetailView):
    model = Part

class PartCreate(CreateView):
    model = Part
    fields = '__all__'

class PartUpdate(UpdateView):
    model = Part
    fields = ['name', 'type']

class PartDelete(DeleteView):
    model = Part
    success_url = '/parts/'