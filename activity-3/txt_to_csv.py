"""
    Actividad 3: Bases de datos de grafos
    -------------------------------------
    Curso: Bases de datos avanzadas
    Profesor: Vicente Cubells Nonell
    Equipo 5:
        Daniela Vignau León (A01021698)
        Cristopher Alan Cejudo Machuca (A01025468)
        Héctor Alexis Reyes Manrique (A01339607)
"""

import pandas as pd

profiles = pd.read_csv('./data/soc-pokec-profiles.txt', header=None, delimiter='\t')
profiles.columns = [
    'user_id',
    'public',
    'completion_percentage',
    'gender',
    'region',
    'last_login',
    'registration',
    'AGE',
    'body',
    'I_am_working_in_field',
    'spoken_languages',
    'hobbies',
    'I_most_enjoy_good_food',
    'pets',
    'body_type',
    'my_eyesight',
    'eye_color',
    'hair_color',
    'hair_type',
    'completed_level_of_education',
    'favourite_color',
    'relation_to_smoking',
    'relation_to_alcohol',
    'sign_in_zodiac',
    'on_pokec_i_am_looking_for',
    'love_is_for_me',
    'relation_to_casual_sex',
    'my_partner_should_be',
    'marital_status',
    'children',
    'relation_to_children',
    'I_like_movies',
    'I_like_watching_movie',
    'I_like_music',
    'I_mostly_like_listening_to_music',
    'the_idea_of_good_evening',
    'I_like_specialties_from_kitchen',
    'fun',
    'I_am_going_to_concerts',
    'my_active_sports',
    'my_passive_sports',
    'profession',
    'I_like_books',
    'life_style',
    'music',
    'cars',
    'politics',
    'relationships',
    'art_culture',
    'hobbies_interests',
    'science_technologies',
    'computers_internet',
    'education',
    'sport',
    'movies',
    'travelling',
    'health',
    'companies_brands',
    'more',
    'temp'
]

profiles.to_csv('./data/soc-pokec-profiles.csv', index=False)

relationships = pd.read_csv ('./data/soc-pokec-relationships.txt', header=None, delimiter='\t')
relationships.to_csv ('./data/soc-pokec-relationships.csv', index=False)
