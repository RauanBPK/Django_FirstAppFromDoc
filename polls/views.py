from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.filter(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Please select a choice!"
        })
    else:
        # Explained here: https://docs.djangoproject.com/en/3.2/ref/models/expressions/#avoiding-race-conditions-using-f
        selected_choice.update(votes=F('votes') + 1)
        # Always return HttpResponseRedirect after a successfull POST to prevent posting twice if the back button is pressed
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
