function fetchCoordinates(){

    let cityName = document.getElementById("name").value.trim();

    if (cityName.length < 3) {
        alert("Įveskite pilną miesto pavadinimą!");
        return;
    }

    fetch(`/weathers/get_place_data/?name=${cityName}`)
        .then(response => response.json())
        .then(data => {
            if (data.latitude && data.longitude) {
                document.getElementById("latitude").value = data.latitude;
                document.getElementById("longitude").value = data.longitude;
            } else {
                alert("Toks miestas nerastas!");
                document.getElementById("latitude").value = "";
                document.getElementById("longitude").value = "";
            }
        })
        .catch(error => console.error("Užklauso klaida:",  error));
}