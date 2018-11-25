select 
	recipe.name,
	preference.name
from recipe
	join recipe_preference on recipe.id = recipe_preference.recipe_id
	join preference on recipe_preference.preference_id = preference.id