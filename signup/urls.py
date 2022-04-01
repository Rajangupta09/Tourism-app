from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="list"),
    path('verifycode/<int:id>', views.VerifyHome.as_view(), name="verify"),
    path('signup/', views.signup, name="signup"),
    path('Logout/', views.logout, name="logout"),
    path('Destination/<int:pk>', views.DestinationView.as_view(), name="destination"),
    path('Tour/', views.TourView.as_view(), name="tour"),
    path('contactList/', views.ContactView.as_view(), name="contact"),
    path('Tour/Delete/<int:pk>', views.TourDeleteView.as_view(),name="delete"),
    path('Tour/Approve/<int:id>', views.Approve,name="approve"),
    path('Tour/Reject/<int:id>', views.Reject,name="reject"),
    path('Tour/Arrived/<int:id>', views.Arrived,name="arrived"),
    path('Tour/Left/<int:id>', views.Left,name="left"),

    path('Contact', views.Contactcreate.as_view(), name="create"),
    path('Main', views.AdminView.as_view(), name="adminview"),
    path('Contact/Reply', views.Replyc,name="reply"),
    path('Inbox', views.inbox,name="inbox"),
    
]