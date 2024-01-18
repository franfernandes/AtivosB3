from django.shortcuts import render,get_object_or_404, redirect, render
from ativos.api import obter_ativos_b3, obter_detalhes_ativo_yahoo
from ativos.scheduler import agendar_tarefa_monitoramento
from .models import Ativo  
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .api import obter_detalhes_ativo_yahoo
from .api import obter_ativos_b3, obter_detalhes_ativo_yahoo
from django.contrib.auth.decorators import login_required
from .models import Ativo
from django.contrib.auth.decorators import login_required
from .forms import AtivoMonitoramentoForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Ativo
from django.contrib import messages
from .models import Ativo
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AtivoMonitoramentoForm
from .models import Ativo

import logging


logger = logging.getLogger(__name__)  


logger.info('Informação inicializada.')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  
    else:
        form = UserCreationForm()
    return render(request, 'ativos/signup.html', {'form': form})



@login_required
def listar_ativos(request):
    dados_b3 = obter_ativos_b3()
    codigos_ativos = dados_b3.get('stocks', [])[:10]
    detalhes_ativos = []
    for codigo in codigos_ativos:
        try:
            detalhes = obter_detalhes_ativo_yahoo(codigo + '.SA')
            if detalhes:
                detalhes_ativos.append(detalhes)
                Ativo.objects.update_or_create(
                    codigo=detalhes['codigo'],
                    defaults={
                        'nome': detalhes['nome'],
                        'fechamento': detalhes.get('ultimo_fechamento', 0),
                        'abertura': detalhes.get('abertura', 0),
                        'cotacao': detalhes.get('cotacao', 0),
                        'variacao_percentual': detalhes.get('variacao_percentual', 0),
                    }
                )
        except Exception as e:
            print(f"Erro ao obter detalhes para o ativo {codigo}: {e}")
    return render(request, 'ativos/listar_ativos.html', {'detalhes_ativos': detalhes_ativos})




@login_required
def monitorar_ativo_view(request, codigo):
    ativo = get_object_or_404(Ativo, codigo=codigo)
    
    if request.user in ativo.usuarios_monitorando.all():
        print(f"Você ja está monitorando este ativo")
        messages.error(request, 'Você já está monitorando este ativo.')
        return redirect('listar_ativos')
    else:
        ativo.usuarios_monitorando.add(request.user)
        ativo.save()
        messages.success(request, 'Ativo adicionado ao monitoramento com sucesso.')
        
        return redirect('monitorar_ativo_form', codigo=codigo)





def acompanhamento_ativo(request, pk):
    
    
    try:
        ativo = Ativo.objects.get(pk=pk)
    except Ativo.DoesNotExist:
        
        ativo = None
    return render(request, 'ativos/acompanhamento_ativo.html', {'ativo': ativo})


def obter_e_listar_ativos_b3(request):
    
    
    ativos = obter_ativos_b3()
    for ativo_data in ativos:
        Ativo.objects.update_or_create(
            codigo=ativo_data['codigo'],
            defaults=ativo_data  
        )
    return redirect('listar_ativos_usuario')



@login_required
def monitorar_ativo_form_view(request, codigo):
    ativo = get_object_or_404(Ativo, codigo=codigo)
    if request.method == 'POST':
        form = AtivoMonitoramentoForm(request.POST, instance=ativo)
        if form.is_valid():
            ativo_monitorado = form.save()
            
            agendar_tarefa_monitoramento(ativo_monitorado, ativo_monitorado.frequencia_monitoramento)
            messages.success(request, 'Configurações de monitoramento salvas com sucesso.')
            return redirect('listar_ativos')
    else:
        form = AtivoMonitoramentoForm(instance=ativo)
    return render(request, 'ativos/monitorar_ativo_form.html', {'form': form, 'ativo': ativo})


