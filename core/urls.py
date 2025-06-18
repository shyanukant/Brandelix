from django.urls import path
from .views import GenerateContent

urlpatterns = [
    path('generate/', GenerateContent.as_view(), name='generate_content'),
]
