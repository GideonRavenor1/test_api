from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.forms import Form

from src.teasers.models import Teaser, Category
from src.wallets.models import Wallet


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Teaser)
class TeaserAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'status')
    list_editable = ('status',)

    def get_queryset(self, request: WSGIRequest) -> QuerySet:
        return super().get_queryset(request).select_related('user', 'category')

    def save_model(self, request: WSGIRequest, obj: Teaser, form: Form, change: bool) -> None:
        super().save_model(request, obj, form, change)
        if change and form.cleaned_data['status'] == obj.STATUS.paid:
            wallet: Wallet = obj.user.wallet
            wallet.transfer_amount()
            wallet.save(update_fields=['balance'])
