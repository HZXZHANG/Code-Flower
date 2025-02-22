from django import template
from django.contrib.auth.models import User
from main.models import *
import math

register = template.Library()

@register.simple_tag
def get_topic_progress(user_name, topic_id):
    curr_user = User.objects.get(username=user_name)
    curr_topic = Topic.objects.get(id=topic_id)
    lessons = Lesson.objects.filter(topic=curr_topic)
    total_lessons = len(lessons)
    total_credits = 0

    for curr_lesson in lessons:
        try:
            if curr_lesson.published:
                score = UserLessonProgress.objects.get(user=curr_user, lesson=curr_lesson).score
                total_credits += score
            else:
                total_lessons -= 1
        except UserLessonProgress.DoesNotExist:
            pass

    if total_lessons <= 0:
        return 0
    else:
        return math.trunc(total_credits/total_lessons)

@register.simple_tag
def get_lesson_progress(user_name, lesson_id):
    curr_user = User.objects.get(username=user_name)
    curr_lesson = Lesson.objects.get(id=lesson_id)

    try:
         return math.trunc(UserLessonProgress.objects.get(user=curr_user, lesson=curr_lesson).score)
    except UserLessonProgress.DoesNotExist:
        return 0


@register.simple_tag
def check_completion(user_name, topic_id, idx, ach):
    curr_user = User.objects.get(username=user_name)
    curr_topic = Topic.objects.get(id=topic_id)
    lessons = Lesson.objects.filter(topic=curr_topic)
    achievement=ach[idx]
    total_lessons = len(lessons)
    total_credits = 0

    for curr_lesson in lessons:
        try:
            if curr_lesson.published:
                score = UserLessonProgress.objects.get(user=curr_user, lesson=curr_lesson).score
                total_credits += score
            else:
                total_lessons -= 1
        except UserLessonProgress.DoesNotExist:
            pass


    if total_lessons <= 0:
        return False
    else:
        if math.trunc(total_credits / total_lessons) == 100:
            achievement.completed = True
            return True


@register.simple_tag
def get_achievement_progress(complete, total, ach):
    count = 0
    for a in ach:
        if a.completed:
            count = count + 1

    return round(count/total*100, 1)

