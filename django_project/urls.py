from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_view.LoginView.as_view(template_name='socio/login.html'
        ,extra_context={'title':'Welcome - Login to socio'}),name='login'),
    path('password-reset/', 
    	auth_view.PasswordResetView.as_view(template_name='socio/password_reset.html'),
    	name='password_reset'),

    path('password-reset-done/', 
    	auth_view.PasswordResetDoneView.as_view(template_name='socio/password_reset_done.html'),
    	name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', 
    	auth_view.PasswordResetConfirmView.as_view(template_name='socio/password_reset_confirm.html'),
    	name='password_reset_confirm'),

    path('password-reset-complete/', 
    	auth_view.PasswordResetCompleteView.as_view(template_name='socio/password_reset_complete.html'),
    	name='password_reset_complete'),

    # url(r'^notifications/', include('notify.urls', 'notifications')),
    path('', include('socio.urls')),
]


if settings.DEBUG:
    urlpatterns  += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)