from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm




def landing_view(request):
    return render(request, 'landing.html')
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. You can now log in.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
# Login View with role-based redirect
# class RoleBasedLoginView(LoginView):
#     template_name = 'login.html'
#     def form_valid(self, form):
#         selected_role = self.request.POST.get('role')
#         user = form.get_user()
#         if selected_role and user and getattr(user, 'role', None) and selected_role != user.role:
#             form.add_error(None, "Selected role does not match your account role.")
#             return self.form_invalid(form)
#         return super().form_valid(form)
#     def get_success_url(self):
#         user = self.request.user
#         # Prefer selected role from the submitted form if provided and valid
#         selected_role = self.request.POST.get('role') or getattr(user, 'role', None)
#         if selected_role == 'manager':
#             return '/dashboard/manager/'
        # elif selected_role == 'sales_agent':
        #     return '/dashboard/sales/'
        # elif selected_role == 'attendant':
        #     return '/dashboard/attendant/'
        # return 'manager_dashboard'


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect based on role
            role = user.profile.role  # assumes Profile exists
            if role == 'manager':
                request.session['role'] = manager
                return redirect('manager_dashboard')
            elif role == 'sales_agent':
                return redirect('sales_dashboard')
            elif role == 'attendant':
                return redirect('attendant_dashboard')
            else:
                return redirect('home')  # fallback
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def manager_dashboard(request):
    return render(request, 'manager_dashboard.html')

def attendant_dashboard(request):
    return render(request, 'attendant_dashboard.html')

def sales_dashboard(request):
    return render(request, 'sales_dashboard.html')