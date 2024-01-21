import logging
from django.core.paginator import Paginator

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render

from .api import obter_ativos_b3, obter_detalhes_ativo_yahoo
from .forms import AtivoMonitoramentoForm, CustomUserCreationForm, CustomAuthenticationForm
from .models import Ativo
from .scheduler import agendar_tarefa_monitoramento

logger = logging.getLogger(__name__)
logger.info('Informação inicializada.')



def home_view(request):
    return render(request, 'ativos/home.html')


@login_required
def listar_ativos(request):
    dados_b3 = obter_ativos_b3()
    codigos_ativos = dados_b3.get('stocks', [])[:50]  
    detalhes_ativos = []
    for codigo in codigos_ativos:
        try:
            detalhes = obter_detalhes_ativo_yahoo(codigo + '.SA')
            if detalhes:
                ativo, created = Ativo.objects.update_or_create(
                    codigo=detalhes['codigo'],
                    defaults={
                        'nome': detalhes['nome'],
                        'fechamento': detalhes.get('ultimo_fechamento', 0),
                        'abertura': detalhes.get('abertura', 0),
                        'cotacao': detalhes.get('cotacao', 0),
                        'variacao_percentual': detalhes.get('variacao_percentual', 0),
                    }
                )
                detalhes['monitorando'] = request.user in ativo.usuarios_monitorando.all()
                detalhes_ativos.append(detalhes)
        except Exception as e:
            logger.error(f"Erro ao obter detalhes para o ativo {codigo}: {e}")

    
    paginator = Paginator(detalhes_ativos, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ativos/listar_ativos.html', {'page_obj': page_obj})




@login_required
def monitorar_ativo_view(request, codigo):
    ativo = get_object_or_404(Ativo, codigo=codigo)
    
    return redirect('monitorar_ativo_form', codigo=codigo)


@login_required
def desmonitorar_ativo_view(request, codigo):
    ativo = get_object_or_404(Ativo, codigo=codigo)
    
    if request.user in ativo.usuarios_monitorando.all():
        ativo.usuarios_monitorando.remove(request.user)
        ativo.save()
        messages.success(request, 'Você não está mais monitorando este ativo.')
    else:
        messages.error(request, 'Você não estava monitorando este ativo.')
    
    return redirect('listar_ativos')

@login_required
def esta_monitorando_ativo(request, codigo):
    ativo = get_object_or_404(Ativo, codigo=codigo)
    
    if request.user in ativo.usuarios_monitorando.all():
        return True
    else:
        return False


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

            
            request.user.ativos_monitorados.add(ativo_monitorado)
            
            agendar_tarefa_monitoramento(ativo_monitorado, ativo_monitorado.frequencia_monitoramento)
            messages.success(request, 'Ativo adicionado ao monitoramento e configurações salvas com sucesso.')
            return redirect('listar_ativos')
    else:
        form = AtivoMonitoramentoForm(instance=ativo)
    return render(request, 'ativos/monitorar_ativo_form.html', {'form': form, 'ativo': ativo})


@login_required
def meus_ativos(request):
    
    ativos_monitorados_ids = request.user.ativo_usuarios_monitorando.values_list('ativo_id', flat=True)
    ativos_monitorados = Ativo.objects.filter(id__in=ativos_monitorados_ids)
    return render(request, 'ativos/meus_ativos.html', {'ativos_monitorados': ativos_monitorados})

@login_required
def editar_ativo_view(request, codigo):
    ativo = get_object_or_404(Ativo, codigo=codigo, usuarios_monitorando=request.user)
    if request.method == 'POST':
        form = AtivoMonitoramentoForm(request.POST, instance=ativo)
        if form.is_valid():
            form.save()
            messages.success(request, 'As configurações de monitoramento foram atualizadas.')
            return redirect('meus_ativos')
    else:
        form = AtivoMonitoramentoForm(instance=ativo)
    return render(request, 'ativos/editar_ativo_form.html', {'form': form, 'ativo': ativo})



@login_required
def meus_ativos_view(request):
    ativos_monitorados = request.user.ativos_monitorados.all()
    return render(request, 'ativos/meus_ativos.html', {'ativos_monitorados': ativos_monitorados})

from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data.get('email')
            user.first_name = form.cleaned_data.get('first_name')
            user.save()
            login(request, user)
            
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'ativos/signup.html', {'form': form})
