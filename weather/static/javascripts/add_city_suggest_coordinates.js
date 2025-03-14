function fetchCoordinates(){

    let cityName = document.querySelector("#name").value.trim();

    if (cityName.length < 3) {
        alert("Įveskite pilną miesto pavadinimą!");
        return;
    }

    fetch(`/orai/get_place_data/?name=${cityName}`)
        .then(response => response.json())
        .then(data => {
            if (data.latitude && data.longitude) {
                document.querySelector("#latitude").value = data.latitude;
                document.querySelector("#longitude").value = data.longitude;
                document.querySelector("#administrativeDivision").value = data.administrative_division;
                document.querySelector("#country").value = data.country_code == "LT"? "Lietuva": data.country_code;
            } else {
                alert("Toks miestas nerastas!");
                document.querySelector("#latitude").value = "";
                document.querySelector("#longitude").value = "";
            }
        })
        .catch(error => console.error("Užklauso klaida:",  error));
}