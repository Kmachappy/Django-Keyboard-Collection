from django.db import models
from django.urls import reverse
from datetime import date

TYPES = (
    ('S', 'Switches'),
    ('K', 'Keycaps'),
    ('B', 'Body'),
)

class Part(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('parts_detail', kwargs={'pk': self.id})

# Create your models here.
class Keyboard(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    parts = models.ManyToManyField(Part)
    
    def __str__(self):
        return f"{self.name} ({self.type})"
    
    def get_absolute_url(self):
        return reverse("detail", kwargs={"keyboard_id": self.id})
    
    def cleaned_for_today(self):
        return self.cleaning_set.filter(date=date.today()).count() >=len(TYPES)
    
class Cleaning(models.Model):
    date = models.DateField('Date of Cleaning ')
    type = models.CharField(
        max_length=1,
        # add choices to the field
        choices = TYPES,
        # set the default value to 'S'
        default=TYPES[0][0]
        )
    # create keyboard_id as a foreign key
    keyboard = models.ForeignKey(Keyboard, on_delete=models.CASCADE)
    
    def __str__(self):
        return f" {self.keyboard} {self.get_type_display()} on {self.date}"
    
    class Meta:
        ordering = ['date']
        
class Photo(models.Model):
    url = models.CharField(max_length=200)
    keyboard = models.ForeignKey(Keyboard, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Photo for Keyboard {self.keyboard.name} @ {self.url}"