console.log('script loaded');

document.getElementById("addItemForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Call the addFormItem function
    addFormItem();
});

function addFormItem() {
    // Example: Get the title and description values from the form
    let title = document.getElementById("title").value;
    let description = document.getElementById("description").value;

    html = "<div class='card'>\n" +
        "<div class='card-body'>\n" +
            "<h2 class='card-title'>" + title + "</h2>\n" +
            "<p class='card-description'>" + description + "</p>\n" +
        "</div>\n" +
    "</div>";

    // Add the html to the "row" div
    document.getElementById("row").innerHTML += html;
}