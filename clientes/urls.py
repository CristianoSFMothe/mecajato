from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientes, name="clientes"),
    path('atualizar_clientes/', views.att_cliente, name="atualizar_clientes"),
    path('update_carro/<int:id>', views.update_carros, name="update_carros"),
    path('excluir_carro/<int:id>', views.excluir_carro, name="excluir_carro"),
]
