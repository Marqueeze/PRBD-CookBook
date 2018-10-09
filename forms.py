from flask_wtf import Form
from wtforms import StringField, TextAreaField, IntegerField
from wtforms.validators import AnyOf, Regexp, NoneOf, URL, Optional
from models import *


class Finder(Form):
    id = IntegerField('id', validators=[Regexp("\d*", message="Id must be an integer")])
    name = StringField('name',
                       validators=[NoneOf(['"', "'", ";", "/", "\\"], message="\", ', ;, /, \\ are not allowed")])

    def get_item(self, i):
        return {
            0: self.id,
            1: self.name,
            2: self.recipe
        }[i]

    def finder(self, contents: list):
        for i in range(len(self)):
            if self.get_item(i).data:
                # contents = list(filter(lambda x: x.get_item(i) == self.get_item(i).data, contents))
                contents = list(filter(lambda x: str(self.get_item(i).data) in str(x.get_item(i)), contents))
        return contents

    def __len__(self):
        return 3


class RecipeForm(Finder):
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
            c = Chapter.query.filter_by(name=self.chapter.data.lower()).first()
            if c:
                r.chapter_id = c.id
            else:
                r.chapter_id = None
        else:
            r = Recipe.query.get(_id)
            r.name = self.name.data.lower()
            r.source = self.source.data
            r.time = self.time.data
            r.level = self.level.data
            r.calorific = self.calorific.data
            r.text = self.text.data.lower()
            c = Chapter.query.filter_by(name=self.chapter.data.lower()).first()
            if c:
                r.chapter_id = c.id
            else:
                r.chapter_id = None
        db.session.add(r)
        db.session.commit()
        self.filler(Recipe.query.filter_by(name=self.name.data.lower(), source=self.source.data, time=self.time.data,
                                           level=self.level.data, calorific=self.calorific.data,
                                           text=self.text.data.lower()).first())

    def filler(self, r):
        if r:
            added = []
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
                    added.append(tmp)
            for tmp in r.rec_ingr:
                if tmp not in added:
                    db.session.delete(tmp)
            added = []
            for t in self.preferences.data.lower().replace(',', '').split(' '):
                p = Preference.query.filter_by(name=t.lower()).first()
                if p:
                    tmp = RecipePreference.query.filter_by(recipe_id=r.id, preference_id=p.id).first()
                    if not tmp:
                        tmp = RecipePreference(recipe_id=r.id, preference_id=p.id)
                        r.rec_pref.append(tmp)
                        p.rec_pref.append(tmp)
                        db.session.add(p)
                        db.session.add(tmp)
                    added.append(tmp)
            for tmp in r.rec_pref:
                if tmp not in added:
                    db.session.delete(tmp)
            db.session.commit()
        else:
            raise (Exception("Wrong recipe adding"))


class IngredientForm(Finder):
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


class PreferenceForm(Finder):
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


class ChapterForm(Finder):
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

