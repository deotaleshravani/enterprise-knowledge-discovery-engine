<<<<<<< HEAD
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import UserProfile


@api_view(["POST"])
@permission_classes([])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return JsonResponse({"error": "username and password required"}, status=400)

    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({"error": "invalid credentials"}, status=401)

    login(request, user)
    token, _ = Token.objects.get_or_create(user=user)

    profile, _ = UserProfile.objects.get_or_create(
        user=user,
        defaults={"role": UserProfile.ROLE_EMPLOYEE},
    )

    return JsonResponse({
        "token": token.key,
        "username": user.username,
        "role": profile.role,
        "department": profile.department,
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
    profile, _ = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={"role": UserProfile.ROLE_EMPLOYEE},
    )

    return JsonResponse({
        "username": request.user.username,
        "role": profile.role,
        "department": profile.department,
        "is_admin": profile.role == UserProfile.ROLE_ADMIN,
        "is_manager": profile.role in [UserProfile.ROLE_ADMIN, UserProfile.ROLE_MANAGER],
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def role_required_view(request):
    profile, _ = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={"role": UserProfile.ROLE_EMPLOYEE},
    )

    if profile.role not in [UserProfile.ROLE_ADMIN, UserProfile.ROLE_MANAGER]:
        return JsonResponse({"error": "Forbidden: manager/admin role required"}, status=403)

    return JsonResponse({
        "message": "Access allowed",
        "role": profile.role,
        "username": request.user.username,
    })
=======
from django.shortcuts import render

# Create your views here.
>>>>>>> 295313f9544a55975afdff91c3cab55d8a5a635a
