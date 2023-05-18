from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class Account(AbstractUser):
    """model representing forum user"""

    score = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    fav_ducks = models.ManyToManyField('ducks.Duck')
