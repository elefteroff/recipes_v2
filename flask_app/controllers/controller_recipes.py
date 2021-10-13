from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import model_users, model_recipes

# ******************** DISPLAY ROUTES ********************

@app.route('/dashboard')
def dashboard():
    recipes = model_recipes.Recipe.get_all_recipes()
    user = model_users.User.get_one(id = session['id'])
    return render_template('dashboard.html', all_recipes = recipes, user = user)

@app.route('/recipes/new')
def recipe_new():
    return render_template('new_recipe.html')

@app.route('/recipes/<int:id>')
def recipe_view(id):
    recipe = model_recipes.Recipe.get_one(id = id)
    user = model_users.User.get_one(id = session['id'])
    return render_template("view_recipe.html", recipe = recipe, user = user)

@app.route('/recipes/edit/<int:id>')
def recipe_edit(id):
    recipe = model_recipes.Recipe.get_one(id = id)
    return render_template('edit_recipe.html', recipe = recipe)

# ******************** ACTION ROUTES ********************

@app.route('/recipes/create', methods = ["POST"])
def create_recipe():
    is_valid = model_recipes.Recipe.validate_recipes(request.form)
    if not is_valid:
        return redirect('/recipes/new')
    recipe_data = {
        "users_id": session["id"],
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under_30_min": request.form["under_30_min"],
        "date_made": request.form["date_made"],
    }
    model_recipes.Recipe.create(recipe_data)
    return redirect('/dashboard')

@app.route('/recipe/delete/<int:id>')
def recipe_delete(id):
    model_recipes.Recipe.delete_one(id = id)
    return redirect('/dashboard')

@app.route('/recipes/update/<int:id>', methods = ["POST"])
def update_recipe(id):
    is_valid = model_recipes.Recipe.validate_recipes(request.form)
    if not is_valid:
        return redirect(f'/recipes/edit/{id}')
    updated_recipe_data = {
        "users_id": session["id"],
        "id": id,
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under_30_min": request.form["under_30_min"],
        "date_made": request.form["date_made"],
    }
    model_recipes.Recipe.update_one(updated_recipe_data)
    return redirect('/dashboard')