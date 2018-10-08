from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Length, AnyOf, Regexp, Optional, NoneOf, URL
from models import *


class RecipeForm(Form):
    id = IntegerField('id', validators=[Regexp("\d*", message="Id must be an integer")])
    name = StringField('name',
                       validators=[NoneOf(['"', "'", ";", "/", "\\"], message="\", ', ;, /, \\ are not allowed")])
    source = StringField('source', validators=[URL(message="Source must be an URL")])
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
                       level=self.level.data, calorific=self.calorific.data, text=self.text.data.lower(),
                       chapter_id=Chapter.query.filter_by(name=self.chapter.data.lower()).first().id)
            self.filler(r)
        else:
            r = Recipe.query.get(_id)
            r.name = self.name.data.lower()
            r.source = self.source.data
            r.time = self.time.data
            r.level = self.level.data
            r.calorific = self.calorific.data
            r.text = self.text.data.lower()
            r.chapter_id = Chapter.query.filter_by(name=self.chapter.data.lower()).first().id
            self.filler(r)
        db.session.add(r)
        db.session.commit()

    def filler(self, r):
        if r:
            for t in self.ingredients.data.lower().replace(',', '').split(' '):
                i = Ingredient.query.filter_by(name=t.lower()).first()
                if i:
                    tmp = RecipeIngredient.query.filter_by(recipe_id=r.id, ingredient_id=i.id).first()
                    if not tmp:
                        tmp = RecipeIngredient(recipe_id=r.id, ingredient_id=i.id)
                        r.rec_ingr.append(tmp)
                        i.rec_ingr.append(tmp)
                        db.session.add(i)
                        db.session.add(tmp)
            for t in self.preferences.data.lower().replace(',', '').split(' '):
                p = Preference.query.filter_by(name=t.lower()).first()
                if p:
                    tmp = RecipePreference.query.filter_by(recipe_id=r.id, preference_id=p.id).first()
                    if not tmp:
                        tmp = RecipePreference(recipe_id=r.id, preferecne_id=p.id)
                        r.rec_pref.append(tmp)
                        p.rec_pref.append(tmp)
                        db.session.add(p)
                        db.session.add(tmp)
        else:
            raise(Exception("Wrong recipe adding"))


class IngredientForm(Form):
    id = IntegerField('id', validators=[Regexp("\d*", message="Id must be an integer")])
    name = StringField('name',
                       validators=[NoneOf(['"', "'", ";", "/", "\\"], message="\", ', ;, /, \\ are not allowed")])
    recipe = StringField('recipe', validators=[Regexp(".*")])

    def create_instance(self):
        i = Ingredient(name=self.name.data.lower())
        db.session.add(i)
        db.session.commit()

    def filler(self):
        i = Ingredient.query.filter_by(name=self.name.data.lower()).first()
        if i:
            for t in self.recipe.data.lower().replace(',', '').split(' '):
                r = Recipe.query.filter_by(name=t.lower()).first()
                if r:
                    tmp = RecipeIngredient(ingredient_id=i.id, recipe_id=r.id)
                    i.rec_ingr.append(tmp)
                    r.rec_ingr.append(tmp)
                    db.session.add(tmp)
                    db.session.add(r)
            db.session.add(i)
            db.session.commit()
        else:
            raise (Exception("Wrong ingredient adding"))


class PreferenceForm(Form):
    id = IntegerField('id', validators=[Regexp("\d*", message="Id must be an integer")])
    name = StringField('name',
                       validators=[NoneOf(['"', "'", ";", "/", "\\"], message="\", ', ;, /, \\ are not allowed")])
    recipe = StringField('recipe', validators=[Regexp(".*")])

    def create_instance(self):
        p = Preference(name=self.name.data.lower())
        db.session.add(p)
        db.session.commit()

    def filler(self):
        p = Preference.query.filter_by(name=self.name.data.lower()).first()
        if p:
            for t in self.recipe.data.lower().replace(',', '').split(' '):
                r = Recipe.query.filter_by(name=t.lower()).first()
                if r:
                    tmp = RecipePreference(preference_id=p.id, recipe_id=r.id)
                    p.rec_pref.append(tmp)
                    r.rec_pref.append(tmp)
                    db.session.add(tmp)
                    db.session.add(r)
            db.session.add(p)
            db.session.commit()
        else:
            raise(Exception("Wrong preference adding"))


class ChapterForm(Form):
    id = IntegerField('id', validators=[Regexp("\d*", message="Id must be an integer")])
    name = StringField('name',
                       validators=[NoneOf(['"', "'", ";", "/", "\\"], message="\", ', ;, /, \\ are not allowed")])
    recipe = StringField('recipe', validators=[Regexp(".*")])

    def create_instance(self):
        c = Chapter(self.name.data.lower())
        db.session.add(c)
        db.session.commit()

    def filler(self):
        c = Chapter.query.filter_by(name=self.name.data.lower()).first()
        if c:
            for t in self.recipe.data.lower().replace(',', '').split(' '):
                r = Recipe.query.filter_by(name=t.lower()).first()
                if r:
                    r.chapter_id = c.id
                    c.recipes.append(r)
                    db.session.add(r)
            db.session.add(c)
            db.session.commit()
        else:
            raise(Exception("Wrong chapter adding"))
