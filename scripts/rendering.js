async function fetchData() {
    const query = document.getElementById('query').value;
    const response = await fetch('/data?query=${query}');
    const data = await response.json();

    if (data.error) {
        alert(data.error);
        return;
    }

    console.log(data);
}