/**
 * Date Created: 4/24/2024
 * Date Modified: 4/24/2024
 * 
 * Author: Nathaniel Clark
 * Purpose: This file is used to handle the javascript for the board details page
 */

console.log('script loaded');

//saves changes to be done to board
let changesToBoard = [];

//Used for assigning a unique id to each board item
let assignBoardId = 0;

// Variable to keep track of the number of board items
let numberOfBoardItems = 0;

// Set the initial state to "view", state is used for function that occurs when a item is clicked
state = "view";
document.getElementById("modes").value = "view";

/**********************************************************************
 * Adds an event listener to the "modes" dropdown menu
 * When the drop down menu selects the mode switch state to that mode
 * This is used to handel what happens when a board is clicked
 * 
 * Author: Nathaniel Clark
 **********************************************************************/
document.getElementById("modes").addEventListener("change", function() {
    // Get the selected value
    var selectedValue = this.value;
    
    //change state to view
    if (selectedValue === "view"){
        state = "view";
    }

    //change state to delete
    if (selectedValue === "delete"){
        state = "delete";
    }

    //change state to edit
    if (selectedValue === "edit"){
        state = "edit";
    }
});





/**********************************************************************
 * retrieves the value of the CSRF token from the cookie
 * 
 * Author: Nathaniel Clark (ChatGPT used to help)
 * https://chat.openai.com/share/274e26c2-df74-4548-926b-cde8ff1216b0
 * ********************************************************************/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if the cookie name matches the CSRF cookie name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**********************************************************************
 * Adds a new item to the board using javascript if the form is valid
 * 
 * WARNING - Made objects will not be saved to the surver if the
 * "Save Board" button is not clicked
 * 
 * Author: Nathaniel Clark
 * ********************************************************************/
function addFormItem() {
    // Example: Get the title and description values from the form
    let title = document.getElementById("title").value;
    let description = document.getElementById("description").value;

    if (title !== "" && description !== "" && title.length <= 64) {
        changesToBoard.push(
            {   
                type: "add",
                title: title,
                description: description
            }
        );
        console.log(changesToBoard);
        assignBoardId = assignBoardId + 1;
        numberOfBoardItems = numberOfBoardItems + 1;

        // Create new elements
        let colDiv = document.createElement("div");
        colDiv.classList.add("col-md-4", "px-3", "py-3", "text-center");
        
        let button = document.createElement("button");
        button.id = "board-item-" + assignBoardId;
        button.classList.add("btn", "btn-outline-primary", "btn-size");
        
        let card = document.createElement("div");
        card.classList.add("card", "card-custom"); // Add a custom class for the card
        
        let cardBody = document.createElement("div");
        cardBody.classList.add("card-body");
        
        let cardTitle = document.createElement("h2");
        cardTitle.id = "board-item-" + assignBoardId + "-title";
        cardTitle.classList.add("card-title");
        cardTitle.textContent = title;
        
        let cardDescription = document.createElement("p");
        cardDescription.id = "board-item-" + assignBoardId + "-description";
        cardDescription.classList.add("card-description", "pb-2");
        cardDescription.textContent = description;

        // Build the hierarchy
        cardBody.appendChild(cardTitle);
        cardBody.appendChild(cardDescription);
        card.appendChild(cardBody);
        button.appendChild(card);
        colDiv.appendChild(button);
        
        // Add an event listener to the button
        (function(index) {
            colDiv.addEventListener("click", function() {
                let title = document.getElementById("board-item-" + index + "-title").textContent;
                let description = document.getElementById("board-item-" + index + "-description").textContent;
        
                document.getElementById("view-item-title").textContent = title;
                document.getElementById("view-item-text").textContent = description;
        
                $('#viewBoardItem').modal('show');
            });
        })(assignBoardId); // Pass assignBoardId as an argument to the IIFE

        // Add the new card to the "row" div
        document.getElementById("boardItems").appendChild(colDiv);

        // Create the "New Note" button
        let createNewItemButton = document.createElement("button");
        createNewItemButton.type = "button";
        createNewItemButton.classList.add("btn", "btn-primary");
        createNewItemButton.id = "create-new-item-button";
        createNewItemButton.setAttribute("data-toggle", "modal");
        createNewItemButton.setAttribute("data-target", "#createBoardItem");
        createNewItemButton.textContent = "New Note";

        // Create the "Save Board" button
        let saveBoardButton = document.createElement("button");
        saveBoardButton.type = "button";
        saveBoardButton.classList.add("btn", "btn-primary");
        saveBoardButton.id = "save-board-button";
        saveBoardButton.textContent = "Save Board";

        // Add the buttons to the document
        boardItems = document.getElementById("boardItems");
        boardItems.appendChild(createNewItemButton);
        boardItems.appendChild(saveBoardButton);

        if (document.getElementById("no-items-found")) {
            document.getElementById("no-items-found").remove();
        }

        // Close the modal
        $('#createBoardItem').modal('hide');
    }
    else if (title.length > 64){  
        document.getElementById("error-modal-text").innerHTML = "Title must be less than 64 characters";
        $('#createBoardItem').modal('hide');
        $('#errorModel').modal('show');
    }
    else {
        document.getElementById("error-modal-text").innerHTML = "Please fill in all fields";
        $('#createBoardItem').modal('hide');
        $('#errorModel').modal('show');
    }
}

/**********************************************************************
 * Adds an event listener to the button that adds a new item to the board
 * 
 * When the button is clicked, add the item to the board which is handled by addFormItem
 * 
 * Author: Nathaniel Clark
 * ********************************************************************/
document.getElementById("addItemForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Call the addFormItem function
    addFormItem();

    // Reset the form
    document.getElementById("addItemForm").reset();
});

/**********************************************************************
 * Adds an event listener to the button that saves the board
 * 
 * When the button is clicked, changesToBoard is turned into a JSON object
 * and then sent to the server using a POST request
 * 
 * Author: Nathaniel Clark (ChatGPT used to help)
 * https://chat.openai.com/share/274e26c2-df74-4548-926b-cde8ff1216b0
 * ********************************************************************/
document.getElementById("save-board-button").addEventListener("click", function() {
    // Send the POST request with the CSRF token included in the headers

    let csrftoken = getCookie('csrftoken');
    fetch(window.location.pathname, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,  // Include the CSRF token in the headers
        },
        body: JSON.stringify(changesToBoard),
    }).then(data => {
        console.log(data);
        changesToBoard = [];
    })
});

/**********************************************************************
 * Adds an event listener to each item to do a specified action when clicked
 * What action that occurs is based on the current state
 * 
 * - view: Opens a modal to show the item's title and description
 * - edit: brings up modal to edit the name and description of the item
 * - delete: brings up modal to confirm deletion
 * 
 * Author: Nathaniel Clark
 **********************************************************************/
let i = 1;
while (document.getElementById("board-item-" + i)) {
    // Add an event listener to the item
    (function(index) {
        let item = document.getElementById("board-item-" + index);
        
        item.addEventListener("click", function() {

            //bring up modal to view item
            if (state === "view"){
                let itemTitle = document.getElementById("board-item-" + index + "-title").textContent;
                let itemDescription = document.getElementById("board-item-" + index + "-description").textContent;
                
                document.getElementById("view-item-title").textContent = itemTitle;
                document.getElementById("view-item-text").textContent = itemDescription;
                
                $('#viewBoardItem').modal('show');
            }
    
            //bring up modal to edit item
            else if (state === "edit"){
                let itemTitle = document.getElementById("board-item-" + index + "-title");
                let itemDescription = document.getElementById("board-item-" + index + "-description");
                let item_id = itemTitle.getAttribute("data-id");
                
                let editItemTitle = document.getElementById("editItemTitleInput");
                editItemTitle.placeholder = itemTitle.textContent;
                editItemTitle.value = itemTitle.textContent;
                editItemTitle.setAttribute("data-id", item_id)

                let editItemDescription = document.getElementById("editItemDescriptionInput");
                editItemDescription.placeholder = itemDescription.textContent;
                editItemDescription.value = itemDescription.textContent;
                
                $('#editBoardItem').modal('show');
            }
    
            //bring up modal to confirm deletion
            else if (state === "delete"){
                let boardName = document.getElementById("board-item-" + index + "-title");
                let board_id = boardName.getAttribute("data-id");
                let deleteModalText = document.getElementById("deleteModalWarning");

                deleteModalText.textContent = "Are you sure you want to delete the item titled: " + boardName.textContent + "?";
                deleteModalText.setAttribute("data-id", board_id);

                $('#deleteItem').modal('show');
            }
        });
    })(i);
    //keep track of the number of items
    assignBoardId = assignBoardId + 1;
    numberOfBoardItems = numberOfBoardItems + 1;
    i = i + 1;
}
