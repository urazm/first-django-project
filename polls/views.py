from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Question, Choice
from django.template import loader
from django.utils import timezone


# Это очень распространенная идиома: загрузить шаблон,
# заполнить контекст и вернуть объект HttpResponse с результатом
# визуализации шаблона. Джанго предоставляет сокращение.

# Функция render() принимает объект запроса в качестве первого аргумента, имя шаблона
# в качестве второго аргумента и словарь в качестве необязательного третьего аргумента.
# Она возвращает объект HttpResponse данного шаблона, отображенный в данном контексте.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    # Переопределяет название контекстной переменной(question_list по умолчанию)
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()
                                       ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """
    В предыдущих частях руководства шаблоны были снабжены контекстом, который содержит переменные контекста question
     и latest_question_list. Для DetailView переменная question предоставляется автоматически - поскольку мы используем
    модель Django (Question)
    """
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())




class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))



