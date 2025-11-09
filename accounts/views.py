from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Add new users to Readers group by default
            from django.contrib.auth.models import Group
            readers_group = Group.objects.get(name='Readers')
            user.groups.add(readers_group)
            
            messages.success(request, 'Registration successful! You can now login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def custom_logout(request):
    if request.method == 'POST':
        auth_logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect('home')
    else:
        # For GET requests, show confirmation page
        return render(request, 'accounts/logout_confirm.html')