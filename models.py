from django.db import models

from oAuth.models import User


class Images(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # date when the product was added
    date = models.DateTimeField(auto_now_add=True, null=True)
    url = models.CharField(max_length=512)
