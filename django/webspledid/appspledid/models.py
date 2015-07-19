from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Splendid(models.Model):
    pack_name = models.CharField(max_length=200)
    creator = models.CharField(max_length=20)
    images_per_card = models.IntegerField(validators=[MinValueValidator(3),
                                       MaxValueValidator(8)])
    words = models.TextField(null=True)
    image_zip_file = models. FileField(upload_to='zips', null=True)
    source_of_images = models.TextField()
    # No need for BooleanField as pdf will be null or point to error.pdf
    pdf = models. FileField(upload_to='pdfs', null=True)

    # Date published ?

    def __str__(self): 
        return (self.pack_name + ". Created by " + self.creator)

#s = Splendid(pack_name="First Test", creator="bmsleight", images_per_card=3, words="aa,bb,cc,ddd,eee,fff,ggg,hhh,")
