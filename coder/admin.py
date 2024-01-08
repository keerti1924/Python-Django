from django.contrib import admin
from .models import *

# Register your models here.


class what_you_learn_TabularInline(admin.TabularInline):
    model = What_You_Learn


class Requirements_TabularInline(admin.TabularInline):
    model = Requirements


class Video_TabularInline(admin.TabularInline):
    model = Video


class course_admin(admin.ModelAdmin):
    inlines = (what_you_learn_TabularInline,
               Requirements_TabularInline, Video_TabularInline)


admin.site.register(Categories)
admin.site.register(Contact)
admin.site.register(Author)
admin.site.register(Language)
admin.site.register(Course, course_admin)
admin.site.register(Level)
admin.site.register(What_You_Learn)
admin.site.register(Requirements)
admin.site.register(Lesson)
admin.site.register(UserCourse)
admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(Payment)
admin.site.register(Profile)
admin.site.register(Subscriber)
