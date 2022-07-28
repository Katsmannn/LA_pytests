from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


User = get_user_model()


class Lesson(models.Model):
    description = models.TextField('description')
    lesson_type = models.CharField('lesson type', max_length=20)
    duration = models.PositiveIntegerField('duration')


class Chapter(models.Model):
    title = models.CharField('chapter title', max_length=100)
    lesson = models.ManyToManyField(to=Lesson, through='ChapterLesson')


class Course(models.Model):
    title = models.CharField('ourse_title', max_length=100)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='courses')
    content = models.ManyToManyField(to=Chapter, through='CourseChapter')


class CourseChapter(models.Model):
    course = models.ForeignKey(Course, related_name='course', on_delete=models.PROTECT)
    chapter = models.ForeignKey(Chapter, related_name='chapter_in_course', on_delete=models.PROTECT)
    created_at = models.DateTimeField('created', auto_now_add=True)
    
    class Meta:
        constraints = [models.UniqueConstraint(
            name='unique_chapter_in_course', fields=['course', 'chapter']
        )]


class ChapterLesson(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='chapter', on_delete=models.PROTECT)
    lesson = models.ForeignKey(Lesson, related_name='lesson_in_chapter', on_delete=models.PROTECT)
    lesson_order = models.PositiveSmallIntegerField('lessons number in chapter', validators=[MinValueValidator(1)])

    class Meta:
        constraints = [models.UniqueConstraint(
            name='unique_lesson_in_chapter', fields=['chapter', 'lesson', 'lesson_order']
        )]


class UserRole(models.Model):

    class Role(models.TextChoices):
        MAIN_ADMIN = 'MAdmin', 'Main administrator'
        ADMIN = 'Admin', 'Administrator'
        TEACHER = 'Teacher', 'Teacher'
        VOLUNTEER = 'Volunteer', 'Volunteer'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.TextField('user role', choices=Role.choices)

    class Meta:
        constraints = [models.UniqueConstraint(
            name='unique_user_roles', fields=['user', 'role']
        )]
