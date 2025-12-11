from django.db import models
from django.conf import settings
from decimal import Decimal

User = settings.AUTH_USER_MODEL

class Course(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    subject = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def average_rating(self):
        agg = self.reviews.aggregate(models.Avg("rating"))
        return agg["rating__avg"] or 0

class CoursePart(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="parts")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    num_videos = models.PositiveIntegerField(default=0)
    num_texts = models.PositiveIntegerField(default=0)
    price_z = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.course.title} - {self.name}"

class Lesson(models.Model):
    LESSON_TYPE = [
        ("video", "Video"),
        ("text", "Text"),
    ]
    part = models.ForeignKey(CoursePart, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=255)
    lesson_type = models.CharField(max_length=10, choices=LESSON_TYPE)
    video_url = models.URLField(blank=True, null=True)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    part = models.ForeignKey(CoursePart, on_delete=models.CASCADE, related_name="enrollments")
    created_at = models.DateTimeField(auto_now_add=True)
    is_trial = models.BooleanField(default=False)
    progress_percent = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("student", "part")

    def __str__(self):
        return f"{self.student} -> {self.part}"

class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="course_reviews")
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("course", "student")

    def __str__(self):
        return f"{self.course} - {self.rating}★ by {self.student}"
