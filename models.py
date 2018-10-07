from __init__ import db


class RecipeIngredient(db.Model):
    recipe_id = db.Column(db.INT, db.ForeignKey('recipe.id'), primary_key=True, autoincrement=False)
    ingredient_id = db.Column(db.INT, db.ForeignKey('ingredient.id'), primary_key=True, autoincrement=False)
    recipes = db.relationship("Recipe", back_populates='rec_ingr')
    ingredients = db.relationship("Ingredient", back_populates='rec_ingr')

    def __repr__(self):
        return "RecId: {}, IngId: {}".format(self.recipe_id, self.ingredient_id)

    def __iter__(self):
        return ({
            0: self.recipe_id,
            1: self.ingredient_id
        }[i] for i in range(0, 2))


class RecipePreference(db.Model):
    recipe_id = db.Column(db.INT, db.ForeignKey('recipe.id'), primary_key=True, autoincrement=False)
    preference_id = db.Column(db.INT, db.ForeignKey('preference.id'), primary_key=True, autoincrement=False)
    recipes = db.relationship("Recipe", back_populates='rec_pref')
    preferences = db.relationship("Preference", back_populates='rec_pref')

    def __repr__(self):
        return "RecId: {}, PrefId: {}".format(self.recipe_id, self.preference_id)

    def __iter__(self):
        return ({
            0: self.recipe_id,
            1: self.preference_id
        }[i] for i in range(0, 2))


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.TEXT(16), index=True, unique=True)

    recipes = db.relationship("Recipe")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Name: {}".format(self.name)

    def __iter__(self):
        return ({
            0: self.id,
            1: self.name,
            2: ", ".join('{}'.format(x.name) for x in self.recipes)
        }[i] for i in range(0, 3))


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.TEXT(512), index=True)
    source = db.Column(db.TEXT(512))
    time = db.Column(db.String(32))
    level = db.Column(db.INT)
    calorific = db.Column(db.INT)
    text = db.Column(db.TEXT(8192))

    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.id"), index=True)
    rec_ingr = db.relationship("RecipeIngredient", back_populates='recipes')
    rec_pref = db.relationship("RecipePreference", back_populates='recipes')

    def __repr__(self):
        return "Name: {}".format(self.name)

    def __iter__(self):
        return ({
            0: str(self.id),
            1: str(self.name),
            2: str(self.source),
            3: str(self.time),
            4: str(self.level),
            5: str(self.calorific),
            6: str(self.text),
            7: str(Chapter.query.get(self.chapter_id).name),
            8: ', '.join(list('{}'.format(Ingredient.query.get(x.ingredient_id).name)
                              for x in RecipeIngredient.query.filter_by(recipe_id=self.id).all())),
            9: ', '.join(list('{}'.format(Preference.query.get(x.preference_id).name)
                              for x in RecipePreference.query.filter_by(recipe_id=self.id).all()))
        }[i] for i in range(0, 10))


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.TEXT(16), index=True)

    rec_ingr = db.relationship("RecipeIngredient", back_populates='ingredients')

    def __repr__(self):
        return "Name: {}".format(self.name)

    def __iter__(self):
        return ({
            0: self.id,
            1: self.name,
            2: ', '.join(map(str, list('{}'.format(Recipe.query.get(x.ingredient_id).name)
                                       for x in RecipeIngredient.query.filter_by(recipe_id=self.id).all())))
        }[i] for i in range(0, 3))


class Preference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.TEXT(16), index=True)

    rec_pref = db.relationship("RecipePreference", back_populates='preferences')

    def __repr__(self):
        return "Name: {}".format(self.name)

    def __iter__(self):
        return ({
            0: self.id,
            1: self.name,
            2: ', '.join(map(str, list('{}'.format(Recipe.query.get(x.preference_id).name)
                                       for x in RecipePreference.query.filter_by(recipe_id=self.id).all())))
        }[i] for i in range(0, 3))
