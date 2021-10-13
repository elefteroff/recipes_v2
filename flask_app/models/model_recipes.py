from flask_app import app, DATABASE
from flask_app.models import model_users
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.under_30_min = data['under_30_min']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['users_id']

    @classmethod
    def create(cls,data):
        query = "INSERT INTO recipes (name, description, under_30_min, instructions, date_made, users_id) VALUES (%(name)s, %(description)s, %(under_30_min)s, %(instructions)s, %(date_made)s, %(users_id)s);"
        recipe_id = connectToMySQL(DATABASE).query_db(query,data)
        return recipe_id

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(DATABASE).query_db(query)
        all_recipes = []
        for recipe in results:
            all_recipes.append(cls(recipe))
        return all_recipes

    @classmethod
    def get_one(cls, **data):
        query = "SELECT * FROM recipes JOIN users ON users.id = users_id WHERE recipes.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        row = results[0]
        recipe = cls(row)
        row_data = {
        **row,
        "id":row['users.id'],
        "created_at":row['users.created_at'],
        "updated_at":row['users.updated_at'],
        }
        recipe.user = model_users.User(row_data)
        return recipe

    @classmethod
    def update_one(cls, data):
        query = "UPDATE recipes SET id = %(id)s, name = %(name)s, description = %(description)s, under_30_min = %(under_30_min)s, instructions = %(instructions)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def delete_one(cls, **data):
        query = "DELETE FROM recipes WHERE (id = %(id)s);"
        return connectToMySQL(DATABASE).query_db(query,data)

    # ******************** VALIDATIONS ********************

    @staticmethod
    def validate_recipes(data):
        is_valid = True

        if len(data['name']) <= 3:
            flash("Recipe name must be at least 3 characters.", "error_name")
            is_valid = False

        if len(data['under_30_min']) <= 1:
            flash("Input must be at least 2 characters.", "error_under_30_min")
            is_valid = False

        if len(data['description']) < 5:
            flash("Description must be 5 characters or greater.", "error_description")
            is_valid = False

        if len(data['instructions']) <= 8:
            flash("Instructions must be at least 8 characters.", "error_instructions")
            is_valid = False

        if len(data['date_made']) <= 8:
            flash("Select date made date.", "error_date_made")
            is_valid = False

        return is_valid