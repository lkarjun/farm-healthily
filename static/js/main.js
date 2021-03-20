var loadFile = function(event){
    var image = document.getElementById('output')
    document.getElementById("choose").style="display: none;"
    image.src = URL.createObjectURL(event.target.files[0]);
}