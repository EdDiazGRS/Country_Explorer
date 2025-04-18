from django.db import models
from django.contrib.auth.models import User

class Country(models.Model):
    name = models.CharField(max_length = 100)
    currency = models.CharField(max_length = 100)
    language = models.CharField(max_length = 100)
    capital_city= models.CharField(max_length = 100)
    population = models.IntegerField()
    flag = models.URLField(max_length = 255)
    
    def __str__(self):
        return self.name
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'country') 
        
    def __str__(self):
        return f"{self.user.username} - {self.country.name}"
    
class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'country') 
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.country.name} - {self.rating}"
