var loadFile = function(event){
    var image = document.getElementById('output')
    document.getElementById("choose").style="display: none;"
    document.getElementById("displayImagediv").style="display: inline"
    document.getElementById("output").style="display: block"
    document.getElementById("upload").style="display: block"
    
    image.src = URL.createObjectURL(event.target.files[0]);
}