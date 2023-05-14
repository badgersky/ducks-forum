from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Duck(models.Model):
    """model representing duck"""

    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='ducks')
    occupied_areas = models.TextField()
    strength = models.DecimalField(validators=[MinValueValidator(0), MaxValueValidator(10.0)],
                                   max_digits=3,
                                   decimal_places=1
                                   )
    agility = models.DecimalField(validators=[MinValueValidator(0), MaxValueValidator(10.0)],
                                  max_digits=3,
                                  decimal_places=1
                                  )
    intelligence = models.DecimalField(validators=[MinValueValidator(0), MaxValueValidator(10.0)],
                                       max_digits=3,
                                       decimal_places=1
                                       )
    charisma = models.DecimalField(validators=[MinValueValidator(0), MaxValueValidator(10.0)],
                                   max_digits=3,
                                   decimal_places=1
                                   )
    date_at = models.DateTimeField(auto_now_add=True)