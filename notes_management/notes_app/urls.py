from django.urls import path

from . import views

urlpatterns = [
    path("notes/", views.NotesView.as_view(), name='get_notes'),
    path("notes/create/", views.NotesCreateView.as_view(), name='create_notes'),
    path("notes/<int:note_id>/", views.SingleNoteView.as_view(), name='get_notes'),
    path("notes/<int:note_id>/detail/", views.SingleNoteDetailView.as_view(), name='get_detailed_notes'),
    path("notes/share/", views.NotesShareView.as_view(), name='share_notes'),
    path("notes/version-history/<int:note_id>/", views.NotesHistoryView.as_view(), name='get_history'),
    # path("user/", views.UserView.as_view(), name='get_user'), 
    # path("signup/", views.SignUpView.as_view(), name='create_user'), 
    # path("user/<int:pk>/", views.SingleUserView.as_view(), name='get_put_delete_user'), 
]