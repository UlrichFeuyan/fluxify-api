from django.contrib import admin
from django.utils.html import format_html
from .models import Demande, TypeDemande, DemandeValidation, Commentaire


class DemandeAdmin(admin.ModelAdmin):
    list_display = ('type_demande', 'initiateur', 'status_display', 'active', 'created_at', 'updated_at')
    list_filter = ('status', 'active', 'type_demande')
    search_fields = ('type_demande__nom', 'initiateur__codeuser')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    actions = ['mark_as_active', 'mark_as_inactive']

    def mark_as_active(self, request, queryset):
        queryset.update(active=True)
    mark_as_active.short_description = "Marquer comme actif"

    def mark_as_inactive(self, request, queryset):
        queryset.update(active=False)
    mark_as_inactive.short_description = "Marquer comme inactif"

    def status_display(self, obj):
        if obj.status == 0:
            color = "orange"
            text = "En attente"
        elif obj.status == 1:
            color = "green"
            text = "Approuvé"
        elif obj.status == 2:
            color = "red"
            text = "Rejeté"
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px; border-radius: 5px;">{}</span>',
            color, text
        )

    status_display.short_description = 'Statut'


class TypeDemandeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'nombre_validations_min_requis', 'created_at', 'updated_at')
    search_fields = ('nom',)
    ordering = ('nom',)


class DemandeValidationAdmin(admin.ModelAdmin):
    list_display = ('demande', 'user', 'status_display', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('demande__id', 'user__codeuser')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def status_display(self, obj):
        if obj.status == 0:
            color = "orange"
            text = "En attente"
        elif obj.status == 1:
            color = "green"
            text = "Validé"
        elif obj.status == 2:
            color = "red"
            text = "Rejeté"
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px; border-radius: 5px;">{}</span>',
            color, text
        )

    status_display.short_description = 'Statut'


class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('demande', 'user', 'texte', 'created_at')
    search_fields = ('demande__id', 'user__codeuser', 'texte')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


admin.site.register(Demande, DemandeAdmin)
admin.site.register(TypeDemande, TypeDemandeAdmin)
admin.site.register(DemandeValidation, DemandeValidationAdmin)
admin.site.register(Commentaire, CommentaireAdmin)
