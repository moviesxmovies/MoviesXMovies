---
icon: lucide/figma
title: Design
---

<script src="https://coolors.co/palette-widget/widget.js"></script>

## Color Palette

### Light mode

<div id="coolors-container-light"></div>

### Dark mode

<div id="coolors-container-dark"></div>

<script>
(function() {
    function setupWidget(containerId, dataId, colors) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = '';

        const fakeScript = document.createElement('script');
        fakeScript.setAttribute('data-id', dataId);
        container.appendChild(fakeScript);

        try {
            new CoolorsPaletteWidget(dataId, colors);
        } catch (e) {
            console.log("Esperando a la librería...");
        }
    }

    function initAll() {
        if (typeof CoolorsPaletteWidget !== 'undefined') {
            setupWidget("coolors-container-light", "038381989895575563", ["1f1f1f","2f27ce","bb3dff","bcbbdd","f2f2f2"]);
            setupWidget("coolors-container-dark", "04507449106158865", ["0d0d0d","232244","7e00c2","3a31d8","e0e0e0"]);
        } else {
            setTimeout(initAll, 200);
        }
    }

    initAll();

    if (typeof document$ !== 'undefined') {
        document$.subscribe(function() {
            initAll();
        });
    }
})();
</script>

## Fonts and sizes

<p style="font-size: 4.210rem; font-weight: 400">Inter 5xl</p>
<p style="font-size: 3.158rem; font-weight: 400">Inter 4xl</p>
<p style="font-size: 2.369rem; font-weight: 400">Inter 3xl</p>
<p style="font-size: 1.777rem; font-weight: 400">Inter 2xl</p>
<p style="font-size: 1.333rem; font-weight: 400">Inter xl</p>
<p style="font-size: 1rem; font-weight: 400">Inter</p>
<p style="font-size: 0.75rem; font-weight: 400">Inter sm</p>
<p style="font-size: 1rem; font-weight: 700">Inter bold</p>

## Components
### Button
=== "Light"
    <figure markdown="span">
    ![Button light](assets/img/components/button/button-light.svg){ loading=lazy }
    <figcaption>Button light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Button dark](assets/img/components/button/button-dark.svg){ loading=lazy }
    <figcaption>Button dark</figcaption>
    </figure>

<br>

=== "Light"
    <figure markdown="span">
    ![Button2 light](assets/img/components/button/button2-light.svg){ loading=lazy }
    <figcaption>Button 2 light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Button2 dark](assets/img/components/button/button2-dark.svg){ loading=lazy }
    <figcaption>Button 2 dark</figcaption>
    </figure>

### Search
<figure markdown="span">
![Search](assets/img/components/search.svg){ loading=lazy }
<figcaption>Search</figcaption>
</figure>

### Search Fields 
=== "Light"
    <figure markdown="span">
    ![Search fields light](assets/img/components/search-fields-light.svg){ loading=lazy }
    <figcaption>Search fields light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Search fields dark](assets/img/components/search-fields-dark.svg){ loading=lazy }
    <figcaption>Search fields dark</figcaption>
    </figure>

### Navbar
=== "Light"
    <figure markdown="span">
    ![Navbar light](assets/img/components/navbar-light.svg){ loading=lazy }
    <figcaption>Navbar light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Navbar dark](assets/img/components/navbar-dark.svg){ loading=lazy }
    <figcaption>Navbar dark</figcaption>
    </figure>

### Stars
<figure markdown="span">
![Stars](assets/img/components/stars-dark.svg#only-light){ loading=lazy }
![Stars](assets/img/components/stars-light.svg#only-dark){ loading=lazy }
<figcaption>Stars</figcaption>
</figure>

### Pill
=== "Light"
    <figure markdown="span">
    ![Pill light](assets/img/components/pill/pill-light.svg){ loading=lazy }
    <figcaption>Pill light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Pill dark](assets/img/components/pill/pill-dark.svg){ loading=lazy }
    <figcaption>Pill dark</figcaption>
    </figure>

<br>

=== "Light"
    <figure markdown="span">
    ![Pill2 light](assets/img/components/pill/pill2-light.svg){ loading=lazy }
    <figcaption>Pill 2 light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Pill2 dark](assets/img/components/pill/pill2-dark.svg){ loading=lazy }
    <figcaption>Pill 2 dark</figcaption>
    </figure>

### Badge
=== "Light"
    <figure markdown="span">
    ![Badge light](assets/img/components/delete-badge-light.svg){ loading=lazy }
    <figcaption>Badge light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Badge dark](assets/img/components/delete-badge-dark.svg){ loading=lazy }
    <figcaption>Badge dark</figcaption>
    </figure>

### Checkbox
<figure markdown="span">
![Checkbox](assets/img/components/checkbox.svg){ loading=lazy }
<figcaption>Checkbox</figcaption>
</figure>

### Rating
=== "Light"
    <figure markdown="span">
    ![Rating light](assets/img/components/rating-light.svg){ loading=lazy }
    <figcaption>Rating light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Rating dark](assets/img/components/rating-dark.svg){ loading=lazy }
    <figcaption>Rating dark</figcaption>
    </figure>

### Review

=== "Light"
    <figure markdown="span">
    ![Review light](assets/img/components/review/review-light.svg){ loading=lazy }
    <figcaption>Review light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Review dark](assets/img/components/review/review-dark.svg){ loading=lazy }
    <figcaption>Review dark</figcaption>
    </figure>

<br>

=== "Light"
    <figure markdown="span">
    ![Review profile light](assets/img/components/review/review-profile-light.svg){ loading=lazy }
    <figcaption>Review profile light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Review profile dark](assets/img/components/review/review-profile-dark.svg){ loading=lazy }
    <figcaption>Review profile dark</figcaption>
    </figure>

### Following
=== "Light"
    <figure markdown="span">
    ![Following light](assets/img/components/following/following-light.svg){ loading=lazy }
    <figcaption>Following light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Following dark](assets/img/components/following/following-dark.svg){ loading=lazy }
    <figcaption>Following dark</figcaption>
    </figure>

<br>

=== "Light"
    <figure markdown="span">
    ![Follow light](assets/img/components/following/follow-light.svg){ loading=lazy }
    <figcaption>Follow light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Follow dark](assets/img/components/following/follow-dark.svg){ loading=lazy }
    <figcaption>Follow dark</figcaption>
    </figure>

### Actions
=== "Light"
    <figure markdown="span">
    ![More Info light](assets/img/components/actions/action-moreinfo-light.svg){ loading=lazy }
    <figcaption>More Info light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![More Info dark](assets/img/components/actions/action-moreinfo-dark.svg){ loading=lazy }
    <figcaption>More Info dark</figcaption>
    </figure>

<br>

=== "Light"
    <figure markdown="span">
    ![Not seen light](assets/img/components/actions/action-notseen-light.svg){ loading=lazy }
    <figcaption>More Info light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Not seen dark](assets/img/components/actions/action-notseen-dark.svg){ loading=lazy }
    <figcaption>Not seen dark</figcaption>
    </figure>

<br>

=== "Light"
    <figure markdown="span">
    ![Add to List light](assets/img/components/actions/action-addtolist-light.svg){ loading=lazy }
    <figcaption>Add to List light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Add to List dark](assets/img/components/actions/action-addtolist-dark.svg){ loading=lazy }
    <figcaption>Add to List dark</figcaption>
    </figure>

### Movie
#### Movie cover
<figure markdown="span">
![Movie cover](assets/img/components/movie-cover.svg){ loading=lazy }
<figcaption>Movie cover</figcaption>
</figure>

#### New Movie
<figure markdown="span">
![New Movie](assets/img/components/new-movie.svg){ loading=lazy }
<figcaption>New Movie</figcaption>
</figure>

### Movie List
<figure markdown="span">

![Movie List](assets/img/components/movie-list.svg){ loading=lazy }
<figcaption>Movie List</figcaption>
</figure>

#### Add Movie List
<figure markdown="span">
![Add Movie List](assets/img/components/add-button/add-movielist.svg){ loading=lazy }
<figcaption>Add Movie List</figcaption>
</figure>

=== "Light"
    <figure markdown="span">
    ![Blank Movie List light](assets/img/components/add-button/blank-list-light.svg){ loading=lazy }
    <figcaption>Blank Movie List light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Blank Movie List dark](assets/img/components/add-button/blank-list-dark.svg){ loading=lazy }
    <figcaption>Blank Movie List dark</figcaption>
    </figure>

<br>

=== "Light"
    <figure markdown="span">
    ![Smart Movie List light](assets/img/components/add-button/smart-list-light.svg){ loading=lazy }
    <figcaption>Smart Movie List light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Smart Movie List dark](assets/img/components/add-button/smart-list-dark.svg){ loading=lazy }
    <figcaption>Smart Movie List dark</figcaption>
    </figure>

#### Movie List Checkbox
=== "Light"
    <figure markdown="span">
    ![Movie List Checkbox light](assets/img/components/movielist-checkbox-light.svg){ loading=lazy }
    <figcaption>Movie List Checkbox light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Movie List Checkbox dark](assets/img/components/movielist-checkbox-dark.svg){ loading=lazy }
    <figcaption>Movie List Checkbox dark</figcaption>
    </figure>

### Modals
#### Pop up
=== "Light"
    <figure markdown="span">
    ![Pop up light](assets/img/components/modals/popup-light.svg){ loading=lazy }
    <figcaption>Pop up light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Pop up dark](assets/img/components/modals/popup-dark.svg){ loading=lazy }
    <figcaption>Pop up dark</figcaption>
    </figure>

#### Create Movie List
=== "Light"
    <figure markdown="span">
    ![Blank List light](assets/img/components/modals/blanklist-create-light.svg){ loading=lazy }
    <figcaption>Blank List light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Blank List dark](assets/img/components/modals/blanklist-create-dark.svg){ loading=lazy }
    <figcaption>Blank List dark</figcaption>
    </figure>

<br>

=== "Light"
    <figure markdown="span">
    ![Smart List light](assets/img/components/modals/smartlist-create-light.svg){ loading=lazy }
    <figcaption>Smart List light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Smart List dark](assets/img/components/modals/smartlist-create-dark.svg){ loading=lazy }
    <figcaption>Smart List dark</figcaption>
    </figure>

#### Add to Movie List
=== "Light"
    <figure markdown="span">
    ![Add to Movie List light](assets/img/components/modals/movielist-add-light.svg){ loading=lazy }
    <figcaption>Add to Movie List light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Add to Movie List dark](assets/img/components/modals/movielist-add-dark.svg){ loading=lazy }
    <figcaption>Add to Movie List dark</figcaption>
    </figure>

## Pages
=== "Light"
    <figure markdown="span">
    ![Home light](assets/img/pages/light/home.png){ loading=lazy }
    <figcaption>Home light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Home dark](assets/img/pages/dark/home.png){ loading=lazy }
    <figcaption>Home dark</figcaption>
    </figure>

<br>

=== "Light"
    <figure markdown="span">
    ![Movie Info light](assets/img/pages/light/movie-info.png){ loading=lazy }
    <figcaption>Movie Info light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Movie Info dark](assets/img/pages/dark/movie-info.png){ loading=lazy }
    <figcaption>Movie Info dark</figcaption>
    </figure>

<br>

=== "Light"
    <figure markdown="span">
    ![Movie List light](assets/img/pages/light/movie-list.png){ loading=lazy }
    <figcaption>Movie List light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Movie List dark](assets/img/pages/dark/movie-list.png){ loading=lazy }
    <figcaption>Movie List dark</figcaption>
    </figure>

<br>

=== "Light"
    <figure markdown="span">
    ![Person light](assets/img/pages/light/person.png){ loading=lazy }
    <figcaption>Person light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Person dark](assets/img/pages/dark/person.png){ loading=lazy }
    <figcaption>Person dark</figcaption>
    </figure>

<br>

=== "Light"
    <figure markdown="span">
    ![Profile light](assets/img/pages/light/profile.png){ loading=lazy }
    <figcaption>Profile light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Profile dark](assets/img/pages/dark/profile.png){ loading=lazy }
    <figcaption>Profile dark</figcaption>
    </figure>

<br>

=== "Light"
    <figure markdown="span">
    ![Search Results light](assets/img/pages/light/search-results.png){ loading=lazy }
    <figcaption>Search Results light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Search Results dark](assets/img/pages/dark/search-results.png){ loading=lazy }
    <figcaption>Search Results dark</figcaption>
    </figure>

<br>

=== "Light"
    <figure markdown="span">
    ![Select Create List light](assets/img/pages/light/select-create-list.png){ loading=lazy }
    <figcaption>Select Create List light</figcaption>
    </figure>

=== "Dark"
    <figure markdown="span">
    ![Select Create List dark](assets/img/pages/dark/select-create-list.png){ loading=lazy }
    <figcaption>Select Create List dark</figcaption>
    </figure>

## Prototype
<iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="800" height="450" src="https://embed.figma.com/proto/DngkWasn7sjCtRTMbUfqJh/MoviesXMovies?node-id=1-2&p=f&scaling=scale-down&content-scaling=fixed&page-id=0%3A1&embed-host=share" allowfullscreen></iframe>