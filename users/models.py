from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields.files import ImageField
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    image = ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    #optimizing image saved
    
    # #get middle of pic
    # def crop_center(pil_img, crop_width, crop_height):
    #         img_width, img_height = pil_img.size
    #         return pil_img.crop(((img_width - crop_width) // 2,
    #                         (img_height - crop_height) // 2,
    #                         (img_width + crop_width) // 2,
    #                         (img_height + crop_height) // 2))
    
    # #get largest square
    # def crop_max_square(pil_img):
    #     return crop_center(pil_img, min(pil_img.size), min(pil_img.size))

    # def save(self, *args, **kwargs): #after model has saved - save method which we are overwriting
    #     super().save(*args, **kwargs) #

    #     img = Image.open(self.image.path)

           

    #     if img.height > 300 or img.width > 300:
    #         output_size =(300,300)

            

    #         img.thumbnail(output_size)
    #         img.save(self.image.path) # override and save back to path

