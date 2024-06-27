import datetime
from dateutil.relativedelta import relativedelta
from django.contrib import admin
from django.templatetags.static import static
from apps.administracao.models import Apartamento,Cupons,Usuario, Reserva
from django.urls import reverse
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from .models import Reserva
from django.utils.translation import gettext_lazy as _


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ( 'username','gerar_relatorio_button')


    def gerar_relatorio_button(self, obj):
        return format_html('<a class="button" href="{}">Gerar Relatório</a>', reverse('administracao:relatorio_usuarios'))

    gerar_relatorio_button.short_description = "Relatório"
    gerar_relatorio_button.allow_tags = True
    class Media:
        css = {
            'all': (static('css/cssadmin.css'),),
        }


@admin.register(Apartamento)
class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor', 'status')
    list_editable = ('valor',)
    class Media:
        css = {
            'all': (static('css/cssadmin.css'),),
        }

class DataIntervaloFilter(admin.SimpleListFilter):
    title = _('Intervalo de Data')
    parameter_name = 'intervalo_data'

    def lookups(self, request, model_admin):
        return (
            ('hoje', _('Hoje')),
            ('ontem', _('Ontem')),
            ('esta_semana', _('Esta semana')),
            ('este_mes', _('Este mês')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'hoje':
            return queryset.filter(dataEntrada__date=datetime.date.today())
        elif self.value() == 'ontem':
            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            return queryset.filter(dataEntrada__date=yesterday)
        elif self.value() == 'esta_semana':
            start_of_week = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
            end_of_week = start_of_week + datetime.timedelta(days=6)
            return queryset.filter(dataEntrada__date__range=[start_of_week, end_of_week])
        elif self.value() == 'este_mes':
            start_of_month = datetime.date.today().replace(day=1)
            end_of_month = start_of_month + relativedelta(months=1, days=-1)
            return queryset.filter(dataEntrada__date__range=[start_of_month, end_of_month])

class ReservaAdmin(admin.ModelAdmin):
    list_display = ('user', 'apartamento', 'valor', 'dataEntrada', 'dataSaida', 'gerar_relatorio_button')
    search_fields = ('user__username', 'apartamento__nome')
    list_filter = ('dataEntrada', 'dataSaida')

    def gerar_relatorio_button(self, obj):
        return format_html('<a class="button" href="{}">Gerar Relatório</a>', reverse('administracao:relatorio_reservas'))

    gerar_relatorio_button.short_description = "Relatório"
    gerar_relatorio_button.allow_tags = True



class SeuModeloAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': (static('css/cssadmin.css'),),
        }

admin.site.register(Cupons, SeuModeloAdmin)

admin.site.site_header = 'Pousada Praia Campeche'
admin.site.site_title = 'Pousada Praia Campeche'


admin.site.register(Reserva, ReservaAdmin)