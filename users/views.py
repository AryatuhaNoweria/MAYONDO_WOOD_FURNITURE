from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm,Userloginform




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


def login_view(request):
    if request.method == 'POST':
        form = Userloginform(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            if request.user.is_authenticated:
                if request.user.role =='manager':
                    return redirect ('manager_dashboard')
                if request.user.role =='sales_agent':
                    return redirect('sales_agent_dashboard')
                if request.user.role =='attendant':
                    return redirect('attendant_dashboard')
    else:
        form = Userloginform()
    context ={'form':form}
    return render(request,'login.html', context)
    
                
                    


    #     username = request.POST['username']
    #     password = request.POST['password']
    #     user = authenticate(request, username=username, password=password)
    #     if user is not None:
    #         login(request, user)
    #         # Redirect based on role
    #         role = user.profile.role  # assumes Profile exists
    #         if role == 'manager':
    #             return redirect('manager_dashboard')
    #         elif role == 'sales_agent':
    #             return redirect('sales_dashboard')
    #         elif role == 'attendant':
    #             return redirect('attendant_dashboard')
    #         else:
    #             return redirect('home')  # fallback
    #     else:
    #         messages.error(request, "Invalid username or password")
    # return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def manager_dashboard(request):
    return render(request, 'manager_dashboard.html')

def attendant_dashboard(request):
    return render(request, 'attendant_dashboard.html')

def sales_dashboard(request):
    return render(request, 'sales_dashboard.html')