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
### Review
<figure markdown="span">
  ![Review light](assets/img/components/review/review-light.svg){ loading=lazy }
  <figcaption>Review light</figcaption>
</figure>

<figure markdown="span">
  ![Review light](assets/img/components/review/review-dark.svg){ loading=lazy }
  <figcaption>Review dark</figcaption>
</figure>

<figure markdown="span">
  ![Review light](assets/img/components/review/review-profile-light.svg){ loading=lazy }
  <figcaption>Review profile light</figcaption>
</figure>

<figure markdown="span">
  ![Review light](assets/img/components/review/review-profile-dark.svg){ loading=lazy }
  <figcaption>Review profile dark</figcaption>
</figure>

## Pages

## Prototype
