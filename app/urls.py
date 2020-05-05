from django.urls import path

from . import views

urlpatterns = [
    # path('', views.EventList.as_view(), name='event-list'),
    path('', views.home, name='home'),
    # path('test/', views.test, name='test'),

    path('permalink/<str:permalink>/', views.redirect_permalink, name='permalink'),
    path('recipient/', views.RecipientList.as_view(), name='recipient-list'),
    path('recipient/add/', views.recipient_create, name='recipient-create'),
    path('suggestion/<int:id>/', views.gift_suggestions, name='gift-suggestions'),
    path('result/<int:id>/', views.voting_result, name='voting-result'),

    path('event/', views.EventList.as_view(), name='event-list'),
    path('event/<int:pk>/', views.EventDetail.as_view(), name='event-detail'),
    # path('event/<int:event_id>/gift/', views.gift_list, name='gift-list'),
    path('event/<int:event_id>/gift/', views.GiftList.as_view(), name='gift-list'),
    path('event/<int:event_id>/gift/add/', views.GiftCreate.as_view(), name='gift-create'),
    path('event/<int:event_id>/gift/<int:pk>/', views.GiftDetail.as_view(), name='gift-detail'),
    path('event/<int:event_id>/gift/<int:pk>/update/', views.GiftUpdate.as_view(), name='gift-update'),
    path('event/<int:event_id>/gift/<int:pk>/delete/', views.GiftDelete.as_view(), name='gift-delete'),

    path('withdraw/<int:event_id>/', views.withdraw, name='withdraw'),
    path('participate/<int:event_id>/', views.participate, name='participate'),
    path('count-me-out/<int:gift_id>/', views.count_me_out, name='count-me-out'),
    path('count-me-in/<int:gift_id>/', views.count_me_in, name='count-me-in'),

    path('accounts/signup/', views.SignUp.as_view(), name='signup')

    # path('', views.test, name='test'),
]


