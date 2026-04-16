---
icon: lucide/network
title: Diagrams
---

## Entity Relationship Diagram
<div align="center">
```mermaid
---
config:
  layout: elk
---

erDiagram
    USER }o--o{ USER: follows
    USER ||--|| REVIEW: writes
    USER ||--|| RATING: gives
    USER }o--|| MOVIELIST: creates
    USER }o--o{ PERSON: follows
    USER }o--o{ PLATFORM: has
    USER ||--o{ FRIENDSHIP: has
    USER ||--o{ FRIENDREQUEST: sends
    USER ||--o{ FRIENDREQUEST: receives
    PERSON }o--|| MOVIE: directs
    PERSON }o--o{ MOVIE: acts
    MOVIE }|--o{ GENRE: has
    MOVIE }o--o{ PLATFORM: available_at
    MOVIE ||--o{ MOVIETRANSLATION: has
    AWARD ||--o{ MOVIE: awards
    AWARD ||--o{ PERSON: awards
    MOVIELIST }o--o{ MOVIE: has
    RATING ||--o{ MOVIE: rates
    REVIEW ||--o{ MOVIE: reviews
    GENRE ||--o{ GENRETRANSLATION: has
    PERSON  ||--o{ PERSONTRANSLATION: has
```
</div>

## Class Diagram

<div align="center">
```mermaid
---
config:
  layout: elk
---

erDiagram
    USER }o--o{ USER: follows
    USER ||--|| REVIEW: writes
    USER ||--|| RATING: gives
    USER }o--|| MOVIELIST: creates
    USER }o--o{ PERSON: follows
    USER }o--o{ PLATFORM: has
    USER ||--o{ FRIENDSHIP: has
    USER ||--o{ FRIENDREQUEST: sends
    USER ||--o{ FRIENDREQUEST: receives
    PERSON }o--|| MOVIE: directs
    PERSON }o--o{ MOVIE: acts
    MOVIE }|--o{ GENRE: has
    MOVIE }o--o{ PLATFORM: available_at
    MOVIE ||--o{ MOVIETRANSLATION: has
    AWARD ||--o{ MOVIE: awards
    AWARD ||--o{ PERSON: awards
    MOVIELIST }o--o{ MOVIE: has
    RATING ||--o{ MOVIE: rates
    REVIEW ||--o{ MOVIE: reviews
    GENRE ||--o{ GENRETRANSLATION: has
    PERSON ||--o{ PERSONTRANSLATION: has
    MOVIE {
        String title
        String slug
        Date release_date
        String synopsis
        Image cover
        M2M directors
        M2M actors
        M2M genres
        M2M platforms
    }
    MOVIETRANSLATION {
        String language
        String title
        String synopsis
        Image image
        Integer movie FK
    }
    GENRE {
        String name
        String slug
    }
    GENRETRANSLATION {
        String language
        String name
        Integer genre FK
    }
    PERSON {
        String name
        String slug
        Image image
    }
    PERSONTRANSLATION{
        String language
        String biograpy
        String person_slug
    }
    AWARD {
        Date date
        String name
        String slug
        ENUM category
        Image icon
    }
    RATING {
        Integer rating
        Integer movie FK
        Integer user FK
    }
    USER {
        Image picture
        String bio
        String preferred_language
        M2M following_person
        M2M platforms
        M2M unseen_movies
    }
    MOVIELIST {
        String name
        String slug
        Enum privacity
        String description
        M2M movies
        Integer user FK
    }
    REVIEW {
        String title
        String content
        Boolean is_positive
        Integer user FK
        Integer movie FK
    }
    PLATFORM {
        String url
        String name
        String slug
        Image image
    }
    FRIENDSHIP {
        Integer user1 FK
        Integer user2 FK
        Date created_at
    }
    FRIENDREQUEST {
        Integer from_user FK
        Integer to_user FK
        ENUM status
        Date created_at
    }
```
</div>