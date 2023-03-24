from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=12)
    email = models.CharField(blank=True, null=True, default='', max_length=50)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        db_table = 'organizations'

    def __str__(self):
        return self.name