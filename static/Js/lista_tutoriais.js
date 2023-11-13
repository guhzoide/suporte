document.getElementById('search').addEventListener('input', function() {
    var input = this.value.toLowerCase();
    var tutorials = document.querySelectorAll('.tutorial');

    for (var i = 0; i < tutorials.length; i++) {
        var tutorial = tutorials[i];
        var tutorialName = tutorial.textContent.toLowerCase();
        
        if (tutorialName.includes(input)) {
            tutorial.style.display = 'block';
        } else {
            tutorial.style.display = 'none';
        }
    }
});