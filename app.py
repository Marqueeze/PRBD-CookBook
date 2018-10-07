from flask import render_template, flash, redirect, url_for, request, g
from datetime import datetime
from models import *
from forms import *
from __init__ import app


@app.route("/create/<instance>", methods=["GET", "POST"])
def create(instance):
    instance_dict = {
        "chapter": ChapterForm,
        "recipe": RecipeForm,
        "ingredient": IngredientForm,
        "preference": PreferenceForm
    }
    form = instance_dict[instance.lower()]
    form = form()
    if form.validate_on_submit():
        form.create_instance()
        form.filler()
        flash('{} added successfully'.format(instance.capitalize()))
        return redirect(url_for('index'))
    return render_template("create.html", form=form, instance=instance.lower())


@app.route('/', methods=['GET', 'POST'])
def index():
    p = Preference.query.all()
    r = Recipe.query.all()
    c = Chapter.query.all()
    i = Ingredient.query.all()
    contents_dict = {
        "chapter": c,
        "recipe": r,
        "ingredient": i,
        "preference": p
    }
    return render_template("tables.html", contents_dict=contents_dict)


@app.route('/change/<chtype>/<changing>', methods=['GET', 'POST'])
def change(changing, chtype):
    instance_dict = {
        "chapter": ChapterForm,
        "recipe": RecipeForm,
        "ingredient": IngredientForm,
        "preference": PreferenceForm
    }
    form = instance_dict[chtype]
    form = form()
    return render_template("change.html", form=form)


@app.route('/delete/<chtype>/<deleting>', methods=['GET', 'POST'])
def delete(deleting, chtype):
    instance_dict = {
        "chapter": ChapterForm,
        "recipe": RecipeForm,
        "ingredient": IngredientForm,
        "preference": PreferenceForm
    }
    form = instance_dict[chtype]
    form = form()
    return render_template("delete.html", form=form)


def Clear_DB():
    for t in [RecipeIngredient, RecipePreference, Recipe, Chapter, Preference, Ingredient]:
        for t1 in t.query.all():
            db.session.delete(t1)
    db.session.commit()


def Print_DB():
    for t in [Recipe, RecipeIngredient, RecipePreference, Chapter, Preference, Ingredient]:
        print(t.query.all())


if __name__ == '__main__':
    #Clear_DB()
    Print_DB()
    app.run(debug=True)
