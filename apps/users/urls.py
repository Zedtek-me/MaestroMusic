from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthFlow

router = DefaultRouter()
router.register("", AuthFlow, basename="")

urlpatterns = router.urls
