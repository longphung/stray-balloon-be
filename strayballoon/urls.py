"""strayballoon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework import routers

from quickstart import views
from quickstart.views import CustomAuthToken
from app import consumers, views as app_views

router = routers.DefaultRouter()
# Quick start app management apis
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'questions', app_views.QuestionsViewSet)
router.register(r'question-answers', app_views.QuestionAnswersViewSet)
router.register(r'session-progress', app_views.SessionProgressViewSet)
router.register(r'session', app_views.SessionViewSet)
router.register(r'sessions-questions', app_views.SessionsQuestionsViewSet)

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)$", consumers.ChatConsumer.as_asgi()),
    re_path(r"ws/session/(?P<session_name>\w+)$", consumers.SessionConsumer.as_asgi()),
]

base_patterns = [
    path('', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', CustomAuthToken.as_view()),
    path('answers-of-question/', app_views.AnswersOfQuestionsViews.as_view(), name="AnswersOfQuestions"),
    path('session-progress-of-students/', app_views.SessionProgressOfStudent.as_view(), name="SessionProgressOfStudent"),
    path('students/', app_views.Students.as_view(), name="Students")
]

urlpatterns = [
    path(settings.BASE_URL, include(base_patterns)),
]
