console.log('script loaded');


// Function to add a new item to the board
function addFormItem() {
    // Example: Get the title and description values from the form
    let title = document.getElementById("title").value;
    let description = document.getElementById("description").value;

    if (title !== "" && description !== "") {
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
}

// Add an event listener to the form so items can be added to the board
document.getElementById("addItemForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent the default form submission

    if (document.getElementById("no-items-found")) {
        document.getElementById("no-items-found").remove();
    
    }

    // Call the addFormItem function
    addFormItem();

    // Close the modal
    $('#createBoardItem').modal('hide');

    // Reset the form
    document.getElementById("addItemForm").reset();
});