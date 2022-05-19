from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin


class RegistredPartnerOnly(UserPassesTestMixin):
    to_redirect=None
    def test_func(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_delivery_man:
                return True
            else:
                self.to_redirect='delivery_man:signup'
                return False
        else:
            self.to_redirect='users:login'
            return False

    def handle_no_permission(self):
        return redirect(self.to_redirect)

class SignUpPartnerOnly(UserPassesTestMixin):
    to_redirect=None
    def test_func(self):
        if self.request.user.is_authenticated:
            if not self.request.user.is_delivery_man:
                return True
            else:
                self.to_redirect='core:home'
                return False
        else:
            self.to_redirect='users:login'
            return False

    def handle_no_permission(self):
        return redirect(self.to_redirect)



