from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True, blank=True, max_length=150)
    featured = models.BooleanField(default=False)
    created_date= models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['title']
        
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self, slugify(self.title))
        super().save(*args, **kwargs)
    
    

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(unique=True, blank=True, max_length=250)
    featured = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    thumbnail = models.URLField()
    description = models.TextField(null=True, blank=True, default='N/A')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    in_stock = models.BooleanField(default=True)
    
    
    class Meta:
        ordering = ['-id']
        
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def related(self):
        return self.category.products.all().exclude(pk=self.pk)

class Slider(models.Model):
    title = models.CharField(max_length=50)
    banner = models.ImageField(upload_to='banners')
    show = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.title
    