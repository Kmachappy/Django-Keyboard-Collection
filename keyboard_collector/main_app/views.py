from django.shortcuts import render, redirect
from .models import Keyboard, Part, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import CleaningForm
import uuid
import boto3
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'keyboard-collector-y789'

class KeyboardCreate(LoginRequiredMixin, CreateView):
    model = Keyboard
    fields = ['name', 'type', 'description', 'price']
    
    # This inherited method is called when a 
    # valid keyboard form is being submitted
    def form_valid(self, form):
        # assign the logged in user (self.request.user)
        print('form!!!!@#!@#', form.instance)
        form.instance.user = self.request.user
        print('!~@!$#$', form.instance.user)
        # form.instance is the keyboard that is being created
        # let the createview do its thing
        return super().form_valid(form)
    
class KeyboardUpdate(LoginRequiredMixin, UpdateView):
    model = Keyboard
    fields = ['type', 'description', 'price']
 
class KeyboardDelete(LoginRequiredMixin, DeleteView):
    model = Keyboard
    success_url = '/keyboards/'   


# Create your views here.

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

@login_required
def keyboards_index(request):
    keyboards = Keyboard.objects.filter(user=request.user)
    return render(request, 'keyboards/index.html', {'keyboards': keyboards})

@login_required
def keyboards_detail(request, keyboard_id):
    keyboard = Keyboard.objects.get(id=keyboard_id)
    parts_keyboard_doesnt_have = Part.objects.exclude(id__in=keyboard.parts.all().values_list('id'))
    print(parts_keyboard_doesnt_have)
    cleaning_form = CleaningForm()
    return render(request, 'keyboards/detail.html', {
        'keyboard': keyboard, 'cleaning_form': cleaning_form,
        'parts': parts_keyboard_doesnt_have,    
    })

@login_required
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

@login_required
def add_photo(request, keyboard_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        # s3 is the AWS service that provides access to our buckets
        # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
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
        
@login_required
def associate_part(request, keyboard_id, part_id):
    Keyboard.objects.get(id=keyboard_id).parts.add(part_id)
    return redirect('detail', keyboard_id=keyboard_id)

def signup(request):
    #  initialize error message to blank string to start with 
    error_message = ''
    # if this is a POST request, process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        # usercreationform is a form that is used to create a new user
        print('~~~~', request.POST)
        form = UserCreationForm(request.POST)
        # if the form is valid, save the data to the database
        if form.is_valid():
            # user is saved to the database
            user = form.save()
            # this is how we log a user in via code (not via a browser)
            # parameter is the user object that we want to log in as (user)
            login(request, user)
            # redirect to a new URL: the homepage (/)
            return redirect('index')
        #  if the form is invalid, get the error message
        else:
            # get the error message from the form
            error_message = 'Invalid sign up - try again'
    # A presentational page that displays the sign up form
    form = UserCreationForm()
    # context is a dictionary that contains the form we just created
    context = {'form': form, 'error_message': error_message}
    # render signup.html with the context dictionary
    return render(request, 'registration/signup.html', context)

class PartList(LoginRequiredMixin, ListView):
    model = Part

class PartDetail(LoginRequiredMixin, DetailView):
    model = Part

class PartCreate(LoginRequiredMixin, CreateView):
    model = Part
    fields = '__all__'

class PartUpdate(LoginRequiredMixin, UpdateView):
    model = Part
    fields = ['name', 'type']

class PartDelete(LoginRequiredMixin, DeleteView):
    model = Part
    success_url = '/parts/'