from django.contrib import admin
from django.templatetags.static import static
from apps.administracao.models import Apartamento,Cupons,Usuario, Reserva


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
    list_display = ('user', 'apartamento', 'valor')

    class Media:
        css = {
            'all': (static('css/cssadmin.css'),),  # Usa a função static para o caminho do arquivo CSS
        }

class SeuModeloAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': (static('css/cssadmin.css'),),  # Usa a função static para o caminho do arquivo CSS
        }

# Registra o modelo MeuModelo com a classe Admin personalizada
admin.site.register(Cupons, SeuModeloAdmin)

admin.site.site_header = 'Pousada Praia Campeche'
admin.site.site_title = 'Pousada Praia Campeche'