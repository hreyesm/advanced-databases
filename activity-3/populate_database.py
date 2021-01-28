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

from database import Database

def main():
    db = Database()
    
    _ = db.run(':auto USING PERIODIC COMMIT\nLOAD CSV WITH HEADERS FROM "file:///pokec/pokec-fixed.csv" AS row\nCREATE (:Profile { userID: row.user_id, public: row.public, completion_percentage: row.completion_percentage, gender: row.gender, region: row.region, last_login: row.last_login, registration: row.registration, AGE: row.AGE, body: row.body, I_am_working_in_field: row.I_am_working_in_field, spoken_languages: row.spoken_languages, hobbies: row.hobbies, I_most_enjoy_good_food: row.I_most_enjoy_good_food, pets: row.pets, body_type: row.body_type, my_eyesight: row.my_eyesight, eye_color: row.eye_color, hair_color: row.hair_color, hair_type: row.hair_type, completed_level_of_education: row.completed_level_of_education, favourite_color: row.favourite_color, relation_to_smoking: row.relation_to_smoking, relation_to_alcohol: row.relation_to_alcohol, sign_in_zodiac: row.sign_in_zodiac, on_pokec_i_am_looking_for: row.on_pokec_i_am_looking_for, love_is_for_me: row.love_is_for_me, relation_to_casual_sex: row.relation_to_casual_sex, my_partner_should_be: row.my_partner_should_be, marital_status: row.marital_status, children: row.children, relation_to_children: row.relation_to_children, I_like_movies: row.I_like_movies, I_like_watching_movie: row.I_like_watching_movie, I_like_music: row.I_like_music, I_mostly_like_listening_to_music: row.I_mostly_like_listening_to_music, the_idea_of_good_evening: row.the_idea_of_good_evening, I_like_specialties_from_kitchen: row.I_like_specialties_from_kitchen, fun: row.fun, I_am_going_to_concerts: row.I_am_going_to_concerts, my_active_sports: row.my_active_sports, my_passive_sports : row.my_passive_sports, profession: row.profession, I_like_books: row.I_like_books, life_style: row.life_style, music: row.music, cars: row.cars, politics: row.politics, relationships : row.relationships, art_culture : row.art_culture, hobbies_interests : row.hobbies_interests, science_technologies : row.science_technologies, computers_internet : row.computers_internet, education : row.education, sport : row.sport, movies : row.movies, travelling : row.travelling, health : row.health, companies_brands: row.companies_brands, more: row.more } );')

    _ = db.run('CREATE INDEX FOR (n:Profile) ON (n.userID);')
    
    _ = db.run(':auto USING PERIODIC COMMIT\nLOAD CSV WITH HEADERS FROM "file:///pokec/soc-pokec-relationships.csv" AS row\nMATCH (start:Profile {userID: row.start_id})\nMATCH (end:Profile {userID: row.end_id})\nMERGE (start)-[:FRIENDS_WITH]->(end);')

    db.close()


if __name__ == '__main__':
    main()