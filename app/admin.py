from django.contrib import admin
from .models import Categories,Author,Post,Course,Videos,Levels,Enrollment,requirements,what_you_learn,Lessons,Submission,Score,Assignment

class what_you_learn_TabularInline(admin.TabularInline):
    model = what_you_learn
class requirements_TabularInline(admin.TabularInline):
    model = requirements
class Videos_TabularInline(admin.TabularInline):
    model = Videos
class Course_admin(admin.ModelAdmin):
    inlines=(what_you_learn_TabularInline,requirements_TabularInline,Videos_TabularInline)
admin.site.register(Categories)
admin.site.register(Author)
admin.site.register(Videos)
admin.site.register(Course,Course_admin)
admin.site.register(Levels)
admin.site.register(requirements)
admin.site.register(what_you_learn)
admin.site.register(Submission)
admin.site.register(Score)
admin.site.register(Assignment)
admin.site.register(Lessons)
admin.site.register(Post)
admin.site.register(Enrollment)






# Register your models here.
