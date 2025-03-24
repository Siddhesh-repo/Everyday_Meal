from django.shortcuts import render, redirect, get_object_or_404
from .models import Receipe
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('/vegie/login/') 


def login_user(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password = password)

        if user is not None:
            # Log the user in
            login(request, user)
            messages.success(request, ".")
            return redirect('/vegie/receipes/')  # Redirect to the desired page
        else:
            # Show an error message
            messages.error(request, "Invalid username or password.")
            return redirect('/vegie/login/') 
        
    return render(request, 'login.html')

def register(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
           messages.error(request, "Username already exist!")
           return redirect('/vegie/register/')
        user = User.objects.create(
            username =  username
            
        )
        user.set_password(password)
        user.set_password(confirm_password)
        user.save()
        messages.success(request, "Account created successfully!")
        return redirect('/vegie/register/')



    return render(request, 'register.html')

@login_required(login_url="/vegie/login/")
def receipes(request):
    # Handle form submission
    if request.method == "POST":
        data = request.POST
        receipe_name = data.get('receipe_name')
        receipe_desc = data.get('receipe_desc')
        receipe_image = request.FILES.get('receipe_image')

        # Create a new recipe in the database
        Receipe.objects.create(
            receipe_name=receipe_name,
            receipe_desc=receipe_desc,
            receipe_image=receipe_image,
        )
        return redirect('/vegie/receipes/')  # Redirect back to the recipes list

    # Fetch all recipes from the database
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = Receipe.objects.filter(receipe_name__icontains=search_query)
    else:
        queryset = Receipe.objects.all()
    
    #if request.GET.get('search'):
       # queryset = queryset.filter(receipe_name__icontains = )

    context = {
        'receipes': queryset,
        'search_query': search_query,  # Pass the search query to the template
    }

    return render(request, 'receipes.html', context)

@login_required(login_url="/vegie/login/")
def delete_receipe(request, id):
    # Fetch the recipe to be deleted
    recipe = get_object_or_404(Receipe, id=id)
    recipe.delete()  # Delete the recipe
    return redirect('/vegie/receipes')  # Redirect back to the recipe list

@login_required(login_url="/vegie/login/")
def update_receipe(request, id):
    queryset = Receipe.objects.get(id=id)
    if request.method == "POST":
        data = request.POST
        receipe_name = data.get('receipe_name')
        receipe_desc = data.get('receipe_desc')
        receipe_image = request.FILES.get('receipe_image')

        # Update the recipe fields
        queryset.receipe_name = receipe_name
        queryset.receipe_desc = receipe_desc
        if receipe_image:  # Only update the image if a new one is provided
            queryset.receipe_image = receipe_image
        queryset.save()  # Save the updated recipe to the database

        return redirect('/vegie/receipes/')
    context = {'update_receipe': queryset} 
    return render(request, 'update_receipes.html', context)
    