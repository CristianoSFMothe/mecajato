from django.shortcuts import render
from django.http import HttpResponse
from .models import Cliente, Carro
import re

def validate_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    def calculate_digit(cpf, position):
        sum_digit = sum(int(cpf[num]) * (position - num) for num in range(position - 1))
        return 0 if (sum_digit * 10 % 11 == 10) else sum_digit * 10 % 11

    if calculate_digit(cpf, 10) != int(cpf[9]):
        return False

    if calculate_digit(cpf, 11) != int(cpf[10]):
        return False

    return True

def format_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'

def validate_placa(placa):
    padrao_antigo = re.compile(r'^[A-Z]{3}-?\d{4}$')
    padrao_mercosul = re.compile(r'^[A-Z]{3}\d[A-Z]\d{2}$')

    if re.fullmatch(padrao_antigo, placa) or re.fullmatch(padrao_mercosul, placa):
        return True
    return False

def clientes(request):
    if request.method == "GET":
        return render(request, "clientes.html")
    elif request.method == "POST":
        nome = request.POST.get("nome")
        sobrenome = request.POST.get("sobrenome")
        email = request.POST.get("email")
        cpf = request.POST.get("cpf")

        carros = request.POST.getlist("carro")
        placas = request.POST.getlist("placa")
        anos = request.POST.getlist("ano")

        cliente = Cliente.objects.filter(cpf=cpf)

        if cliente.exists():
            print("Cliente já existe.")
            return render(
                request,
                "clientes.html",
                {
                    "nome": nome,
                    "sobrenome": sobrenome,
                    "email": email,
                    "carros": zip(carros, placas, anos),
                },
            )

        if not validate_cpf(cpf):
            print("CPF inválido.")
            return render(
                request,
                "clientes.html",
                {
                    "nome": nome,
                    "sobrenome": sobrenome,
                    "email": email,
                    "carros": zip(carros, placas, anos),
                },
            )

        if not re.fullmatch(
            re.compile(
                r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
            ),
            email,
        ):
            print("Email inválido.")
            return render(
                request,
                "clientes.html",
                {
                    "nome": nome,
                    "sobrenome": sobrenome,
                    "cpf": cpf,
                    "carros": zip(carros, placas, anos),
                },
            )

        # Formatar CPF antes de salvar
        cpf = format_cpf(cpf)

        cliente = Cliente(nome=nome, sobrenome=sobrenome, email=email, cpf=cpf)
        cliente.save()

        for carro, placa, ano in zip(carros, placas, anos):
            if not validate_placa(placa):
                print(f"Placa inválida: {placa}")
                continue

            if Carro.objects.filter(placa=placa).exists():
                print(f"Placa já existe: {placa}")
                continue

            car = Carro(carro=carro, placa=placa, ano=ano, cliente=cliente)
            car.save()

        return HttpResponse("Teste")
