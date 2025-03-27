// script// scripts

$(".filter_amenities .popover input").on("click", function()
{
    const amenityIds = [];
    const amenityNames = [];
    let selectedAmenities = $(".filter_amenities .selected_amenities");

    const checked = $(".filter_amenities .popover input:checked")
    $.each(checked, function (indexInArray, valueOfElement) { 
        amenityIds.push(valueOfElement.dataset.id);
        amenityNames.push(valueOfElement.dataset.name);
    });

    selectedAmenities.text(amenityNames.join(", "));

    if (amenityNames.length() < 1) {
        selectedAmenities.text("&nbps;");
    }
})

$.get("http://0.0.0.0:5001/api/v1/status/", function(body)
{
    const status = console.log(body.status);
    if 
})