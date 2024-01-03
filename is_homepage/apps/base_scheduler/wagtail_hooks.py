from wagtail import hooks

from .views import BaseSchedulerModelAdmin


@hooks.register('register_admin_viewset') #type: ignore
def register_viewset():
    return BaseSchedulerModelAdmin('scheduler')
