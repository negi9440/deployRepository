from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sample/', include('sample.urls')),
    path('sample/login/', auth_views.LoginView.as_view(template_name='sample/login.html'), name='login'),
    path('', RedirectView.as_view(url='/sample/signup/', permanent=False)),  # ルートURLをsignupにリダイレクト
]
