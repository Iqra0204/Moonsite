from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from ckeditor.fields import RichTextField

from django.utils.timezone import now
from django.utils.timezone import now
from datetime import datetime



class contact(models.Model):
    name = models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    message = models.TextField()

class Categories(models.Model):
    icon = models.CharField(max_length=200,null=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Levels(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Author(models.Model):
    author_name = models.CharField(max_length = 100 )
    author_profile = models.ImageField(upload_to='images/')
    about_author = models.TextField()

    def __str__(self):
        return self.author_name
class Course(models.Model):
    title = models.CharField(max_length=100)
    status = (
        ("Publish","Publish"),
        ("DRAFT","DRAFT"),
    )
    featured_images = models.ImageField(upload_to='featured_images/')
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,null=True)
    author_image = models.ImageField(upload_to='author_images/',default='')
    category  = models.ForeignKey(Categories,on_delete=models.CASCADE,null=True)
    desc = models.TextField()
    level = models.ForeignKey(Levels,on_delete=models.CASCADE,null=True)
    slug = models.SlugField(default='',max_length=100,null=True,blank=True,unique=True)

    created_at=models.DateTimeField(default=now)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse ( "course_details", kwargs={'slug': self.slug} )

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Course.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Course)

class requirements(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    points = models.CharField(max_length=500)
    def __str__(self):
        return self.points
class what_you_learn(models.Model):
    course = models.ForeignKey ( Course, on_delete=models.CASCADE )
    points = models.CharField ( max_length=500 )

    def __str__(self):
        return self.points


class Lessons(models.Model):
    course  = models.ForeignKey(Course,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name + " " + str(self.course)
class Videos(models.Model):
    serial_number= models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to="Media/Yt_Thumbnail",null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    lesson = models.ForeignKey ( Lessons, on_delete=models.CASCADE )
    title = models.CharField ( max_length=100 )
    video = models.FileField(upload_to="video/%y")
    time_duration = models.FloatField(null=True)
    preview = models.BooleanField(default=False)

    def __str__(self):
        return self.title
class Enrollment(models.Model):
    user = models.ForeignKey ( User, on_delete=models.CASCADE )
    course = models.ForeignKey ( Course, on_delete=models.CASCADE )
    def __str__(self):
        return str(self.user)

class Post(models.Model):
    id = models.AutoField ( primary_key=True )
    name = models.CharField(max_length=100)
    # email = models.EmailField(max_length=100)
    comments =  RichTextField(blank=True ,null=True)
    course = models.ForeignKey ( Course, on_delete=models.CASCADE )
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    timestamp=models.DateTimeField(default=now)

    def __str__(self):
        return self.comments

class Assignment ( models.Model ):
    course = models.ForeignKey ( Course, on_delete=models.CASCADE )
    topic = models.TextField ()

    def __str__(self):
        return self.topic

class Submission(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    link = models.CharField(max_length=500)

    def __str__(self):
        return self.link
class Score(models.Model):
    user_detail=models.ForeignKey(User,on_delete=models.CASCADE)
    assignment= models.ForeignKey ( Assignment, on_delete=models.CASCADE )
    grades=models.CharField(max_length=10 ,default=0)
    course = models.ForeignKey(Course , on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user_detail)
