
let image = document.getElementsByTagName('img');

function removeImage(){
    image[1].remove();
}

image[1].addEventListener('click', removeImage);