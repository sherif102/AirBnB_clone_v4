// script// scripts

// variables
let amenityIds = [];
let amenityNames = [];

let cityIds = [];
let cityNames = [];

let stateIds = [];
let stateNames = [];

let locationsChecked = [];


// post request objects
let body = [];

// filter amenities selected
$(".filter_amenities .popover input").on("click", function()
{
    let selectedAmenities = $(".filter_amenities .selected_amenities");
    amenityIds = [];
    amenityNames = [];

    const checked = $(".filter_amenities .popover input:checked")
    $.each(checked, function (indexInArray, valueOfElement) { 
        amenityIds.push(valueOfElement.dataset.id);
        amenityNames.push(valueOfElement.dataset.name);
    });

    selectedAmenities.text(amenityNames.join(", "));

    if (amenityNames.length < 1) {
        selectedAmenities.html("&nbsp");
    }
})

// filter locations:cities selected
$(".locations .popover h4 input").on("click", function()
{
    cityIds = [];
    cityNames = [];

    const checked = $(".locations .popover h4 input:checked")
    $.each(checked, function (indexInArray, valueOfElement) { 
        cityIds.push(valueOfElement.dataset.id);
        cityNames.push(valueOfElement.dataset.name);
    });
})

// filter locations:states selected
$(".locations .popover h2 input").on("click", function()
{
    stateIds = [];
    stateNames = [];

    const checked = $(".locations .popover h2 input:checked")
    $.each(checked, function (indexInArray, valueOfElement) { 
        stateIds.push(valueOfElement.dataset.id);
        stateNames.push(valueOfElement.dataset.name);
    });
})

// all locations selected
$(".locations input").on("click", function() {
    locationsChecked = [];

    let selectedLocations = $(".locations .selected_locations");

    locationsChecked = stateNames.concat(cityNames);

    selectedLocations.text(locationsChecked.join(", "));

    if (locationsChecked.length < 1) {
        selectedLocations.html("&nbsp");
    }
})

// API status getter
$.get("http://0.0.0.0:5001/api/v1/status/", function(response)
{
    if (response.status === "OK") {
        $("#api_status").addClass("available");
    } else {
        $("#api_status").removeClass("available");
    }
});

// all places fetch
$.ajax({
    type: "POST",
    url: "http://0.0.0.0:5001/api/v1/places_search/",
    data: "{}",
    dataType: "json",
    contentType: "application/json",
    success: function (response) {
        const places = $(".places");
        body = response.sort((a, b) => a.name.localeCompare(b.name));
        placeLister(body, places);
    }
});

/**
 * generates article section for each places in the list
 * @param {Array} body - the list of places to generate
 * @param {element} parent - container for the places list
 */
function placeLister(body, parent) {
    $.each(body, function(index, value) {
        const divArticle = $("<article></article>");
        const divHeadline = $("<div class='headline'></div>")
        divHeadline.append("<h2>" + value.name + "</h2>")

        // price by night section
        const sdivPricebynight = $("<div class='price_by_night'></div>")
        sdivPricebynight.text("$" + value.price_by_night)
        divHeadline.append(sdivPricebynight)

        // fetching the user_name
        const divUser = $("<div class='user'></div>")
        $.get(`http://0.0.0.0:5001/api/v1/users/${value.user_id}`, function(answer){
            divUser.html("<b>Owner</b>: " + answer.first_name + " " + answer.last_name);
        })

        const divInformation = $("<div class='information'></div>");
        // max_guest
        const sdivMaxGuest = $("<div class='max_guest'></div>");
        const ssdivGuestIcon = $("<div class='guest_icon'></div>");

        sdivMaxGuest.append(ssdivGuestIcon);
        sdivMaxGuest.append("<p>" + value.max_guest + " Guests</p>");

        // number_rooms
        const sdivNumberRooms = $("<div class='number_rooms'></div>");
        const ssdivBedIcon = $("<div class='bed_icon'></div>");

        sdivNumberRooms.append(ssdivBedIcon);
        sdivNumberRooms.append("<p>" + value.number_rooms + " Bedroom</p>");

        // number_bathrooms
        const sdivNumberBathrooms = $("<div class='number_bathrooms'></div>");
        const ssdivBathIcon = $("<div class='bath_icon'></div>");

        sdivNumberBathrooms.append(ssdivBathIcon);
        sdivNumberBathrooms.append("<p>" + value.number_bathrooms + " Bathroom</p>");

        // appending to the information tag
        divInformation.append(sdivMaxGuest);
        divInformation.append(sdivNumberRooms);
        divInformation.append(sdivNumberBathrooms);

        const divDescription = $("<div class='description'></div>")
        divDescription.html(value.description);

        divArticle.append(divHeadline);
        divArticle.append(divInformation);
        divArticle.append(divUser);
        divArticle.append(divDescription);

        parent.append(divArticle);
    })
}

// places filtering
$("button").on("click", function() {
    if(amenityNames.length > 0 || locationsChecked.length > 0) {
        $("article").remove();
        $.ajax({
            type: "POST",
            url: "http://0.0.0.0:5001/api/v1/places_search/",
            data: JSON.stringify({"amenities": amenityIds, "cities": cityIds, "states": stateIds}),
            dataType: "json",
            contentType: "application/json",
            success: function (response) {
                const places = $(".places");
                const filterBody = response.sort((a, b) => a.name.localeCompare(b.name));
                placeLister(filterBody, places);
                console.log(filterBody);
            }
        });
    } else {
        placeLister(body, $(".places"))
    }
})

