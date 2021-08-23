from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

from posts.views import index, blog, post,search,post_create,post_update,post_delete,profile,edit_profile,contact,comment_delete,category

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('category/<int:pk>/',category, name='category'),
    path('blog/', blog, name='post-list'),
    path('search/', search, name='search'),
    path('post/<id>/', post, name='post-detail'),
    path('create/', post_create, name='post-create'),
    path('post/<id>/update/', post_update, name='post-update'),
    path('post/<id>/delete/', post_delete, name='post-delete'),
    path('comment/<int:pk>/remove/', comment_delete, name='comment_delete'),
    path('accounts/', include('allauth.urls')),
    path('tinymce/',include('tinymce.urls')),
    path('profile/', profile, name='profile'),
    path('profile/edit_profile', edit_profile, name='edit_profile'),
    path('contact/',contact,name='contact'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)