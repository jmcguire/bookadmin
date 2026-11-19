import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        # setup
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        expect = False

        # test
        result = future_question.was_published_recently()

        # assert
        self.assertIs(result, expect)
