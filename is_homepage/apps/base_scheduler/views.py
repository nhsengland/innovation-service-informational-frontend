from wagtail.admin.filters import WagtailFilterSet
from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.admin.views.generic import IndexView

from .models import SchedulerHistoryModel

class BaseSchedulerModelFilterSet(WagtailFilterSet):
    class Meta:
        model = SchedulerHistoryModel
        fields = {'name': ['icontains'], 'status': ['exact']}

class BaseSchedulerIndexView(IndexView):
    list_display = ['name', 'status', 'created_at', 'completed_at', 'notes']
    filterset_class = BaseSchedulerModelFilterSet

class BaseSchedulerModelAdmin(ModelViewSet):
    model = SchedulerHistoryModel
    index_view_class = BaseSchedulerIndexView
    form_fields = []
    icon = 'history'
    add_to_admin_menu = True
    ordering = ['-created_at']
    list_per_page = 50
    inspect_view_enabled = True
