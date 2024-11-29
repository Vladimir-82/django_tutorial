"""Views for the polls app."""

import logging

from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import (
    get_object_or_404,
    render,
)
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Question


logger = logging.getLogger('django_tutorial')


class DetailView(generic.DetailView):
    """Detail view for the polls app."""

    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())


class IndexView(generic.ListView):
    """Index view for the polls app."""

    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions (not including those set to be published in the future)."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class ResultsView(generic.DetailView):
    """Results view for the polls app."""

    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    """Vote for a question."""
    question = get_object_or_404(Question, pk=question_id)
    logger.info('Question: %s' % question.question_text)
    try:
        choice = request.POST["choice"]
        selected_choice = question.choice_set.get(pk=choice)
        logger.info('User %s choice: %s' % (request.user.username, selected_choice.choice_text))
    except (KeyError, Choice.DoesNotExist):
        logger.info('User %s didnt make a choice' % request.user.username)
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
