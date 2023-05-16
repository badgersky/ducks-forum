from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Duck(models.Model):
    """model representing duck"""

    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='ducks')
    origin_country = models.CharField(max_length=200, blank=True)
    avg_weight = models.DecimalField(validators=[MinValueValidator(0)], max_digits=3, decimal_places=1)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
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

    def __str__(self):
        return self.name


class DuckRate(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    duck = models.ForeignKey('Duck', on_delete=models.CASCADE)
    rate = models.DecimalField(validators=[MinValueValidator(0), MaxValueValidator(10.0)],
                               max_digits=3,
                               decimal_places=1)

    def __str__(self):
        return f'{self.duck.name} - {str(self.rate)}'
    