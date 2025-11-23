import hashlib
from django.shortcuts import render
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CourseProgress, Student


# Create your views here.

def index(request):
    return render(request, 'pages/index.html')


@csrf_exempt
def api_register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        fullname = data.get("fullname")
        password = data.get("password")

        if not username or not password or not fullname:
            return JsonResponse({"error": "All fields required"}, status=400)

        if Student.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        Student.objects.create(username=username, full_name=fullname, password=password)
        return JsonResponse({"message": "Account created successfully"})

@csrf_exempt
def api_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        try:
            user = Student.objects.get(username=username)
            stored_hash, salt = user.password.replace("sha256:", "").split("$")
            computed = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
            if computed == stored_hash:
                request.session['user'] = username
                return JsonResponse({"message": "Login successful", "fullname": user.full_name})
            else:
                return JsonResponse({"error": "Invalid password"}, status=401)
        except Student.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        
def api_logout(request):
    request.session.flush()
    return JsonResponse({"message": "Logged out"})


def api_session(request):
    username = request.session.get("user")
    if username:
        from .models import Student
        user = Student.objects.filter(username=username).first()
        if user:
            return JsonResponse({"logged_in": True, "username": user.username, "full_name": user.full_name})
    return JsonResponse({"logged_in": False})

@csrf_exempt
def api_save_progress(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = request.session.get("user")

        # Fallback for debugging: use logged user from frontend if session missing
        if not username:
            username = data.get("username")  # optional for dev
            if not username:
                return JsonResponse({"error": "Not logged in"}, status=403)

        try:
            student = Student.objects.get(username=username)
        except Student.DoesNotExist:
            return JsonResponse({"error": "Invalid student"}, status=404)

        course_id = data.get("course_id")
        lesson_id = data.get("lesson_id")

        progress, _ = CourseProgress.objects.get_or_create(student=student, course_id=course_id)
        if lesson_id not in progress.completed_lessons:
            progress.completed_lessons.append(lesson_id)
            progress.save()
        return JsonResponse({"message": "Progress saved"})
    return JsonResponse({"error": "Invalid method"}, status=405)


@csrf_exempt
def api_get_progress(request):
    username = request.session.get("user")
    if not username:
        return JsonResponse({"error": "Not logged in"}, status=403)

    student = Student.objects.get(username=username)
    progress = CourseProgress.objects.filter(student=student)
    data = {p.course_id: p.completed_lessons for p in progress}
    return JsonResponse(data)