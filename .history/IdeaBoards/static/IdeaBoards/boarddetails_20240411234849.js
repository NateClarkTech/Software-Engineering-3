console.log('script loaded');

function addFormItem() {
    // Example: Get the title and description values from the form
    let title = document.getElementById("title").value;
    let description = document.getElementById("description").value;

    // Create new elements
    let card = document.createElement("div");
    card.classList.add("card");
    
    let cardBody = document.createElement("div");
    cardBody.classList.add("card-body");
    
    let cardTitle = document.createElement("h2");
    cardTitle.classList.add("card-title");
    cardTitle.textContent = title;
    
    let cardDescription = document.createElement("p");
    cardDescription.classList.add("card-description");
    cardDescription.textContent = description;

    // Build the hierarchy
    cardBody.appendChild(cardTitle);
    cardBody.appendChild(cardDescription);
    card.appendChild(cardBody);

    // Add the new card to the "row" div
    document.getElementById("boardItems").appendChild(card);
}

document.getElementById("addItemForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Call the addFormItem function
    addFormItem();
});