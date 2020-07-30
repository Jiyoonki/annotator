from django.urls import path
from . import views

urlpatterns = [
    path('test', views.test, name='test'),
    path('', views.keyword_selector, name='keyword_selector'),
    path('keyword_selector', views.keyword_selector, name='keyword_selector'),
    path('keyword_selector/update', views.keyword_selector_update, name='keyword_selector_update'),



    path('token_list', views.token_list, name='token_list'),
    path('keywords', views.select_keywords_first_page, name='select_keywords'),
    path('keywords/', views.select_keywords_first_page, name='select_keywords'),
    path('keywords/<int:current_page>', views.select_keywords, name='select_keywords'),
    path('keywords/<int:current_page>/', views.select_keywords, name='select_keywords'),
    path('ajaxUpdate', views.ajax_update, name='ajax_update'),
    path('export/', views.export_users_csv_no_key, name='export_users_csv'),
    path('export/<str:key>', views.export_users_csv, name='export_users_csv'),
    path('keywords/upload', views.upload_data, name='upload_data'),
    path('keywords/upload/', views.upload_data, name='upload_data'),

    # for v1
    path('v1/keywords', views.v1_select_keywords_first_page, name='v1_select_keywords'),
    path('v1/keywords/', views.v1_select_keywords_first_page, name='v1_select_keywords'),
    path('v1/keywords/<int:current_page>', views.v1_select_keywords, name='v1_select_keywords'),
    path('v1/keywords/<int:current_page>/', views.v1_select_keywords, name='v1_select_keywords'),
    path('v1/ajaxUpdate', views.v1_ajax_update, name='v1_ajax_update'),
    path('v1/export/<str:session_id>', views.v1_export_users_csv, name='v1_export_users_csv'),
]