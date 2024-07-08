let dropdown = false;
function toggleDropDown() {
    if(dropdown == false) {
        document.getElementById('dropdown-list').classList.remove('hidden')
        dropdown = true;
    }
    else {
        document.getElementById('dropdown-list').classList.add('hidden')
        dropdown = false;
    }
}