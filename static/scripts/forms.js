function setFormActions(action) {
    console.log("hi -kei")
    const form = document.getElementById('search-form');
    if (form.querySelector('input[name="query"]').value == null) {
        alert("Please enter a valid MAL username.")
        document.getElementById('search-form').action = "/";
    }
    else if (form.querySelector('input[name="query"]').value.trim() == "") {
        alert("Please enter a valid MAL username.")
        document.getElementById('search-form').value = "";
        document.getElementById('search-form').action = "/";
    }
    else {
        document.getElementById('search-form').action = action;
    }
}

function handleEnterKey(event) {
    if (event.key == 'Enter') {
        event.preventDefault();
        alert("Please select the option for the data you want to see.")
    }
    else {
        console.log("successful search")
    }
}

window.onload = function () {
    document.getElementById('search-form').addEventListener('keydown', handleEnterKey);
}