function loadCoolorsWidget() {
    if (typeof CoolorsPaletteWidget !== 'undefined') {
        new CoolorsPaletteWidget("038381989895575563", ["1f1f1f","2f27ce","bb3dff","bcbbdd","f2f2f2"]);
    }
}

document.addEventListener("DOMContentLoaded", loadCoolorsWidget);

if (typeof app !== 'undefined' && app.document$) {
    app.document$.subscribe(function() {
        loadCoolorsWidget();
    });
}