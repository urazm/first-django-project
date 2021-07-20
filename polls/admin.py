from django.contrib import admin
from .models import Question

from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3  # по умолчанию показывать 3 пустых формы для добавления Choice


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    # Позволяет создавать объекты Choice при создании Question
    inlines = [
        ChoiceInline,
    ]

    list_display = ('question_text', 'pub_date', 'was_published_recently')  # Отображение полей у объектов Question(по умолчанию str())
    list_filter = ('pub_date', )  # Добавление возможности фильтра по дате
    search_fields = ['question_text']  # Возможность поиска по записи


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
# Register your models here.
