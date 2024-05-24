from django.shortcuts import redirect, render, get_object_or_404
from .models import Recipe
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate ,login,logout
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")
def recipes(request):
    if request.method == "POST":
        data = request.POST
        recipe_name = data.get('recipeName')
        recipe_discription = data.get('recipeDescription')
        recipe_img = request.FILES.get('photo')

        Recipe.objects.create(
            recipe_name=recipe_name,
            recipe_discription=recipe_discription,
            recipe_image=recipe_img,
        )

        return redirect('/recipes/')
    
    queryset = Recipe.objects.all()
    if request.GET.get('search'):
        queryset = queryset.filter(recipe_name__icontains = request.GET.get('search'))

    context = {'recipes': queryset}
    return render(request, 'recipe.html', context)


@login_required(login_url="/login/")
def delete_recipes(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    recipe.delete()
    return redirect('/recipes/')


@login_required(login_url="/login/")
def update_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if request.method == "POST":
        data = request.POST
        recipe_name = data.get('recipeName')
        recipe_discription = data.get('recipeDescription')
        recipe_img = request.FILES.get('photo')

        recipe.recipe_name = recipe_name
        recipe.recipe_discription = recipe_discription
        if recipe_img:
            recipe.recipe_image = recipe_img
        recipe.save()

        return redirect('/recipes/')

    context = {'recipe': recipe}
    return render(request, 'update_recipe.html', context)



def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")

        user = User.objects.filter(username=user_name)
        if user.exists():
            messages.info(request,'User Name Is Already Taken')
            return redirect('http://127.0.0.1:8000/register/#')
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = user_name
        )
        user.set_password(password)
        user.save()
        messages.info(request,'Account Created Successfully ')
    return render(request,'register.html')


def login_page(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")
        user = User.objects.filter(username=user_name)
        if not user.exists():
          messages.info(request,'Invalid Username')
          return redirect('/login/')
        user = authenticate(username=user_name,password=password)
        if user is None:
           messages.info(request,'Invalid Password')
           return redirect('/login/') 
        else :
            login(request,user)
            return redirect('/recipes/')
    return render(request,'login.html')



def logout_page(request):
    logout(request)
    return redirect('/login/')