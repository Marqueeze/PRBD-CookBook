from flask_wtf import Form
from wtforms import StringField, TextAreaField, IntegerField
from wtforms.validators import AnyOf, Regexp, NoneOf, URL, Optional, DataRequired
from models import *


class FindChapter_Ingredient_PreferenceForm(Form):
    recipe = StringField('recipe')
    name = StringField('name')
    id = IntegerField('id')

    def get_item(self, i):
        return {
            0: self.id,
            1: self.name,
            2: self.recipe
        }[i]

    def __len__(self):
        return 3

    def finder(self, contents: list):
        for i in range(len(self)):
            if self.get_item(i).data:
                # contents = list(filter(lambda x: x.get_item(i) == self.get_item(i).data, contents))
                contents = list(filter(lambda x: str(self.get_item(i).data.lower()) in str(x.get_item(i)), contents))
        return contents


class FindRecipeForm(Form):
    name = StringField('name')
    id = IntegerField('id')
    source = StringField('source')
    time = StringField('time')
    level = StringField('level')
    calorific = StringField('calorific')
    text = TextAreaField('text')
    chapter = StringField('chapter')
    preferences = StringField('preferences')
    ingredients = StringField('ingredients')

    def get_item(self, index):
        return {
            0: self.id,
            1: self.name,
            2: self.source,
            3: self.time,
            4: self.level,
            5: self.calorific,
            6: self.text,
            7: self.chapter,
            8: self.ingredients,
            9: self.preferences
        }[index]

    def __len__(self):
        return 10

    def finder(self, contents: list):
        for i in range(len(self)):
            if self.get_item(i).data:
                # contents = list(filter(lambda x: x.get_item(i) == self.get_item(i).data, contents))
                contents = list(filter(lambda x: str(self.get_item(i).data.lower()) in str(x.get_item(i)), contents))
        return contents


class BaseForm(Form):
    name = StringField('name',
                       validators=[
                           DataRequired(message='Name is required'),
                           NoneOf(['"', "'", ";", "/", "\\"], message="\", ', ;, /, \\ are not allowed")
                       ])
    id = IntegerField('id', validators=[Regexp("\d*", message="Id must be an integer")])

    def get_item(self, i):
        return {
            0: self.id,
            1: self.name,
            2: self.recipe
        }[i]


class RecipeForm(BaseForm):
    source = StringField('source', validators=[URL(message="Source must be an URL"), Optional()])
    time = StringField('time', validators=[Regexp(".*")])
    level = StringField('level', validators=[Regexp("\d*", message="Level must be an integer")])
    calorific = StringField('calorific', validators=[Regexp("\d*", message="Calorific must be an integer")])
    text = TextAreaField('text', validators=[Regexp("(.|\n)*")])
    chapter = StringField('chapter', validators=[Regexp(".*")])
    preferences = StringField('preferences', validators=[Regexp(".*")])
    ingredients = StringField('ingredients', validators=[Regexp(".*")])

    def get_item(self, index):
        return {
            0: self.id,
            1: self.name,
            2: self.source,
            3: self.time,
            4: self.level,
            5: self.calorific,
            6: self.text,
            7: self.chapter,
            8: self.ingredients,
            9: self.preferences
        }[index]

    def __len__(self):
        return 10

    def create_instance(self, _id=0):
        if _id == 0:
            r = Recipe(name=self.name.data.lower(), source=self.source.data, time=self.time.data,
                       level=self.level.data, calorific=self.calorific.data, text=self.text.data.lower())
        else:
            r = Recipe.query.get(_id)
            r.name = self.name.data.lower()
            r.source = self.source.data
            r.time = self.time.data
            r.level = self.level.data
            r.calorific = self.calorific.data
            r.text = self.text.data.lower()

        if(self.chapter.data):
            c = Chapter.query.filter_by(name=self.chapter.data.lower()).first()
            if not c:
                c = Chapter(name=self.chapter.data.lower())
                db.session.add(c)
                db.session.commit()
            r.chapter_id = c.id
            if r not in c.recipes:
                c.recipes.append(r)

        for ingr_name in self.ingredients.data.split(','):
            if(ingr_name):
                ingr = Ingredient.query.filter_by(name=ingr_name.strip().lower()).first()
                if not ingr:
                    ingr = Ingredient(name=ingr_name.strip().lower())
                    db.session.add(ingr)
                    db.session.commit()
                ri = RecipeIngredient.query.filter_by(recipe_id=r.id, ingredient_id=ingr.id).first()
                if not ri:
                    ri = RecipeIngredient(recipe_id=r.id, ingredient_id=ingr.id)
                    db.session.add(ri)
                if ri not in r.rec_ingr:
                    r.rec_ingr.append(ri)
        db.session.add(r)
        db.session.commit()


class IngredientForm(BaseForm):
    recipe = StringField('recipe', validators=[Regexp(".*")])

    def create_instance(self, _id=0):
        if _id == 0:
            i = Ingredient(name=self.name.data.lower())
        else:
            i = Ingredient.query.get(_id)
            i.name = self.name.data.lower()
        db.session.add(i)
        db.session.commit()
        self.filler(Ingredient.query.filter_by(name=self.name.data.lower()).first())

    def filler(self, i):
        if i:
            added = []
            for t in self.recipe.data.lower().replace(',', '').split(' '):
                r = Recipe.query.filter_by(name=t.lower()).first()
                if r:
                    tmp = RecipeIngredient.query.filter_by(ingredient_id=i.id, recipe_id=r.id).first()
                    if not tmp:
                        tmp = RecipeIngredient(ingredient_id=i.id, recipe_id=r.id)
                        i.rec_ingr.append(tmp)
                        r.rec_ingr.append(tmp)
                        db.session.add(tmp)
                        db.session.add(r)
                        added.append(tmp)
            for rec_ingr in i.rec_ingr:
                if rec_ingr not in added:
                    db.session.delete(rec_ingr)
            db.session.add(i)
            db.session.commit()
        else:
            raise (Exception("Wrong ingredient adding"))


class PreferenceForm(BaseForm):
    recipe = StringField('recipe', validators=[Regexp(".*")])

    def create_instance(self, _id=0):
        if _id == 0:
            p = Preference(name=self.name.data.lower())
        else:
            p = Preference.query.get(_id)
            p.name = self.name.data.lower()
        db.session.add(p)
        db.session.commit()
        self.filler(Preference.query.filter_by(name=self.name.data.lower()).first())

    def filler(self, p):
        if p:
            added = []
            for t in self.recipe.data.lower().replace(',', '').split(' '):
                r = Recipe.query.filter_by(name=t.lower()).first()
                if r:
                    tmp = RecipePreference.query.filter_by(preference_id=p.id, recipe_id=r.id).first()
                    if not tmp:
                        tmp = RecipePreference(preference_id=p.id, recipe_id=r.id)
                        p.rec_pref.append(tmp)
                        r.rec_pref.append(tmp)
                        db.session.add(tmp)
                        db.session.add(r)
                        added.append(tmp)
            for rec_pref in p.rec_pref:
                if rec_pref not in added:
                    db.session.delete(rec_pref)
            db.session.add(p)
            db.session.commit()
        else:
            raise (Exception("Wrong ingredient adding"))


class ChapterForm(BaseForm):
    recipe = StringField('recipe', validators=[Regexp(".*")])

    def create_instance(self, _id=0):
        if _id == 0:
            c = Chapter(name=self.name.data.lower())
        else:
            c = Chapter.query.get(_id)
            c.name = self.name.data.lower()
        db.session.add(c)
        db.session.commit()
        self.filler(Chapter.query.filter_by(name=self.name.data.lower()).first())

    def filler(self, c):
        if c:
            added = []
            for t in self.recipe.data.lower().replace(',', '').split(' '):
                rs = Recipe.query.filter_by(name=t.lower()).all()
                if rs:
                    for r in rs:
                        r.chapter_id = c.id
                        c.recipes.append(r)
                        db.session.add(r)
                        added.append(r)
            for r in c.recipes:
                if r not in added:
                    db.session.delete(r)
            db.session.add(c)
            db.session.commit()
        else:
            raise (Exception("Wrong chapter adding"))

