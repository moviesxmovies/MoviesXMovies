# MoviesXMovies

## Data Structure
Movie
- name
- year
- sinopsis
- cover
- director (Person)
- ratings (Rating)
- awards (Award)
- genres (Genre)
- casting (Person)
- platforms (Platform)

Genre 
- name

Person
- name

Award
- date
- name

Rating
- rating
- date

Saga
- name
- movies (Movie)

User
- followingActor (Person)
- followingDirector (Person)
- followingSaga (Saga)
- followers
- following
- movieList (Movie)

Review
- movie (Movie)
- user (User)
- isPositive
- content
- date

Platform
- url
- name

## User Manual
When registered, you can search for your favourite movies and calificate them so we can know what are your movies preferences.
After that, movies will display on your screen as a Tinder swipping 