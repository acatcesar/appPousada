from django.contrib import admin
from django.templatetags.static import static
from apps.administracao.models import Apartamento,Cupons,Usuario, Reserva
from django.urls import reverse
from django.utils.html import format_html
from django.http import HttpResponseRedirect

from .models import Reserva

# admin.site.register(Cupons)
# admin.site.register(Usuario)
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': (static('css/cssadmin.css'),),  # Usa a função static para o caminho do arquivo CSS
        }


@admin.register(Apartamento)
class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor', 'status')
    list_editable = ('valor',)
    class Media:
        css = {
            'all': (static('css/cssadmin.css'),),  # Usa a função static para o caminho do arquivo CSS
        }
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('user', 'apartamento', 'valor', 'dataEntrada', 'dataSaida', 'gerar_relatorio_button')
    list_filter = ('dataEntrada', 'dataSaida')
    search_fields = ('user__username', 'apartamento__nome')  # Adicione campos de pesquisa conforme necessário

    def gerar_relatorio_button(self, obj):
        url = reverse('administracao:gerar_relatorio')
        return format_html('<a class="button" href="{}">Gerar Relatório</a>', url)

    gerar_relatorio_button.short_description = "Relatório"

    def response_post_save_change(self, request, obj):
        if "_gerar_relatorio" in request.POST:
            url = reverse('administracao:gerar_relatorio')
            return HttpResponseRedirect(url)
        return super().response_post_save_change(request, obj)

class SeuModeloAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': (static('css/cssadmin.css'),),  # Usa a função static para o caminho do arquivo CSS
        }

# Registra o modelo MeuModelo com a classe Admin personalizada
admin.site.register(Cupons, SeuModeloAdmin)

admin.site.site_header = 'Pousada Praia Campeche'
admin.site.site_title = 'Pousada Praia Campeche'


