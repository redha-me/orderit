from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.urls import reverse_lazy


class LoggedOutOnly(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated 
    def handle_no_permission(self):
        return redirect('core:home')

class UserInfo(UserPassesTestMixin):
    to_redirect=None
    def test_func(self):
        if self.request.user.is_authenticated:
                return True
           
        else:
            self.to_redirect='users:login'
            return False
    def handle_no_permission(self):
        
        return redirect(self.to_redirect)
class LoggedInOnly(LoginRequiredMixin):
    login_url=reverse_lazy('users:login')

# class AccessDenied(UserPassesTestMixin):
#     def test_func(self):
#         return False
#     def handle_no_permission(self):
#         messages.error(self.request,"can't go there")
#         return redirect('core:home')