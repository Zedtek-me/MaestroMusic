from rest_framework.routers import DefaultRouter
from .views import AuthFlow, UserFlow

router = DefaultRouter()
router.register("auth", AuthFlow, basename="")
router.register("user", UserFlow, basename="users")

urlpatterns = router.urls
