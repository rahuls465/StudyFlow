from django.db import models
import hashlib, secrets

# Create your models here.


class Student(models.Model):
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=100)
    password = models.CharField(max_length=150)

    def save(self, *args, **kwargs):
        salt = "djanog_is_awesome" 
        hash_password = lambda s: hashlib.sha256((s + salt).encode('utf-8')).hexdigest()
        if not self.password.startswith("sha256:"):
            hashed = hash_password(self.password)
            self.password = f"sha256:{hashed}${salt}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class CourseProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.IntegerField()
    completed_lessons = models.JSONField(default=list)

    def __str__(self):
        return f"{self.student.username} - Course {self.course_id}"
    
class UserProfile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, default="")
    avatar = models.CharField(max_length=10, default="👤")  # emoji avatar

    def __str__(self):
        return f"{self.student.username}'s Profile"


class QuizProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz_id = models.IntegerField()
    score = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student.username} - Quiz {self.quiz_id}"
