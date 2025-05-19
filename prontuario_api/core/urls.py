from django.urls import path
from .views import gerar_qr_paciente, dar_alta, cadastrar_gerar_qr
from .views import home

urlpatterns = [
     path('', home, name='home'),
    path('api/cadastrar_gerar_qr/', cadastrar_gerar_qr, name='cadastrar_gerar_qr'),
    path('api/qr/<str:cpf>/', gerar_qr_paciente, name='gerar_qr_paciente'),
    path('api/alta/<str:cpf>/', dar_alta, name='dar_alta'),
]

