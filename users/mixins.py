from django.contrib.auth.mixins import AccessMixin,UserPassesTestMixin


class TeacherMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if  request.user.is_student:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class StudentMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if  not request.user.is_student:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class OwnerMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if  not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)