from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

class StatusChoices(TextChoices):
    PENDING= 'pending' ,_('Pending')
    IN_PROGRESS = 'in progress' , _('in_progress')
    DELIVERED = 'delivered', _('delivered')
    CANCELLED = 'cancelled', _('cancelled')