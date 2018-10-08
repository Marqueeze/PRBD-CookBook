from flask import render_template, flash, redirect, url_for, request, g
from datetime import datetime
from models import *
from forms import *
from __init__ import app

form_dict = {
        "chapter": ChapterForm,
        "recipe": RecipeForm,
        "ingredient": IngredientForm,
        "preference": PreferenceForm
    }

instance_dict = {
    "chapter": Chapter,
    "recipe": Recipe,
    "ingredient": Ingredient,
    "preference": Preference
}


@app.route("/create/<instance>", methods=["GET", "POST"])
def create(instance):
    form = form_dict[instance.lower()]
    form = form()
    if form.validate_on_submit():
        form.create_instance()
        form.filler()
        flash('{} added successfully'.format(instance.capitalize()))
        return redirect(url_for('index'))
    return render_template("create.html", form=form, instance=instance.lower())


@app.route('/', methods=['GET', 'POST'])
def index():
    contents_dict = {
        "chapter": Chapter.query.all(),
        "recipe": Recipe.query.all(),
        "ingredient": Ingredient.query.all(),
        "preference": Preference.query.all()
    }
    return render_template("tables.html", contents_dict=contents_dict)


@app.route('/change/<chtype>/<changing>', methods=['GET', 'POST'])
def change(changing, chtype):
    contents_dict = {
        "chapter": Chapter.query.all(),
        "recipe": Recipe.query.all(),
        "ingredient": Ingredient.query.all(),
        "preference": Preference.query.all()
    }
    form = form_dict[chtype]
    form = form()
    if form.validate_on_submit():
        form.create_instance(_id=changing)
        flash('{} changed successfully'.format(chtype.capitalize()))
        return redirect(url_for('index'))
    for i in range(len(form)):
        form.get_item(i).data = instance_dict[chtype].query.get(int(changing)).get_item(i)
    return render_template("change.html", form=form, index=changing, chtype=chtype, contents_dict=contents_dict)


@app.route('/delete/<chtype>/<deleting>', methods=['GET', 'POST'])
def delete(deleting, chtype):
    inst = instance_dict[chtype].query.get(deleting)
    db.session.delete(inst)
    db.session.commit()
    return redirect(url_for('index'))


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
