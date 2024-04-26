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
let assignBoardId = 1;

// Variable to keep track of the number of board items
let numberOfBoardItems = 0;

// Set the initial state to "view", state is used for function that occurs when a item is clicked
state = "view";
document.getElementById("modes").value = "view";

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
 * Accounts for the following cases:
 * 1 - add new item to board (add details to changesToBoard array)
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
                changeType: "add",
                title: title,
                description: description,
                item_index: String(assignBoardId),
            }
        );

        // Create new elements
        let colDiv = document.createElement("div");
        colDiv.classList.add("col-md-4", "px-3", "py-3", "text-center");
        colDiv.id = "board-item-container-" + assignBoardId;
        
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
                    editItemTitle.setAttribute("data-index", index);
    
                    let editItemDescription = document.getElementById("editItemDescriptionInput");
                    editItemDescription.placeholder = itemDescription.textContent;
                    editItemDescription.value = itemDescription.textContent;
                    
                    $('#editBoardItem').modal('show');
                }
        
                //bring up modal to confirm deletion
                else if (state === "delete"){
                    let boardName = document.getElementById("board-item-" + index + "-title");
                    let boardDescription = document.getElementById("board-item-" + index + "-description");
                    let board_id = boardName.getAttribute("data-id");
                    let deleteModalText = document.getElementById("deleteModalWarning");
    
                    deleteModalText.textContent = "Are you sure you want to delete the item titled: " + boardName.textContent + "?";
                    deleteModalText.setAttribute("data-id", board_id);
                    deleteModalText.setAttribute("data-index", index);
                    deleteModalText.setAttribute("data-delete-item-name", boardName.textContent);
                    deleteModalText.setAttribute("data-delete-item-description", boardDescription.textContent);
    
                    $('#deleteItem').modal('show');
                }
            });
        })(assignBoardId); // Pass assignBoardId as an argument to the IIFE

        // Add the new card to the "row" div
        document.getElementById("boardItems").appendChild(colDiv);

        // Create the "New Note" button
        let createNewItemButton = document.createElement("button");
        createNewItemButton.changeType = "button";
        createNewItemButton.classList.add("btn", "btn-primary");
        createNewItemButton.id = "create-new-item-button";
        createNewItemButton.setAttribute("data-toggle", "modal");
        createNewItemButton.setAttribute("data-target", "#createBoardItem");
        createNewItemButton.textContent = "New Note";

        // Create the "Save Board" button
        let saveBoardButton = document.createElement("button");
        saveBoardButton.changeType = "button";
        saveBoardButton.classList.add("btn", "btn-primary");
        saveBoardButton.id = "save-board-button";
        saveBoardButton.textContent = "Save Board";

        // Add the buttons to the document
        boardItems = document.getElementById("boardItems");
        boardItems.appendChild(createNewItemButton);
        boardItems.appendChild(saveBoardButton);

        // Increment the assignBoardId and numberOfBoardItems
        assignBoardId = assignBoardId + 1;
        numberOfBoardItems = numberOfBoardItems + 1;

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
 * Edit an item on the board using javascript if the form is valid
 * 
 * WARNING - Edited objects will not be saved to the board if the
 * "Save Board" button is not clicked
 * 
 * Accounts for the following cases:
 * 2 - edit existing item on board (add edit details to changesToBoard array)
 * 4 - edit item that was added (replace add details with edited names and description)
 * 6 - edited item was previously edited but not saved to database
 * 
 * Author: Nathaniel Clark
 * ********************************************************************/
document.getElementById("edit-item-button").addEventListener("click", function() {

    let itemToEdit = document.getElementById("editItemTitleInput").getAttribute("data-id");
    let itemIndex = document.getElementById("editItemTitleInput").getAttribute("data-index");
    let newTitle = document.getElementById("editItemTitleInput").value;
    let newDescription = document.getElementById("editItemDescriptionInput").value;

    /*************************************
    * case 4 - edit item that was added  *
    **************************************/
    let isCase2 = true;
    for (item in changesToBoard) {
        if (changesToBoard[item].changeType === "add" && changesToBoard[item].item_index === itemIndex){
            changesToBoard[item].title = newTitle;
            changesToBoard[item].description = newDescription;
            return;
        }
        /*************************************
        * case 6 - edit past edit request  *
        **************************************/
        if (changesToBoard[item].changeType === "edit" && changesToBoard[item].item_index === itemIndex){
            changesToBoard[item].title = newTitle;
            changesToBoard[item].description = newDescription;
            isCase2 = false;
            break;
        }
    }
    
    // Make sure input is valid, else give error modal
    if (newTitle !== "" && newTitle.length <= 64) {

        /********************************************
        * case 2 - edit item exisiting on the board *
        *********************************************/
        if (isCase2){
            changesToBoard.push(
                {
                    changeType: "edit",
                    item_id: itemToEdit,
                    title: newTitle,
                    description: newDescription,
                    item_index: itemIndex
                }
            );
        }

        // Update the title and description of the item
        document.getElementById("board-item-" + itemIndex + "-title").textContent = newTitle;
        document.getElementById("board-item-" + itemIndex + "-description").textContent = newDescription;

        // Close the modal
        $('#editBoardItem').modal('hide');
    }
    else if (newTitle.length > 64){
        document.getElementById("error-modal-text").innerHTML = "Title must be less than 64 characters";
        $('#editBoardItem').modal('hide');
        $('#errorModel').modal('show');
    }
    else if (newTitle.length <= 0){
        document.getElementById("error-modal-text").innerHTML = "Title field can't be empty";
        $('#editBoardItem').modal('hide');
        $('#errorModel').modal('show');
    }
    else {
        document.getElementById("error-modal-text").innerHTML = "Unknown error has occured, please contact the site administrator";
        $('#editBoardItem').modal('hide');
        $('#errorModel').modal('show');
    }
});

/**********************************************************************
 * Delete an item on the board using javascript
 * 
 * WARNING - Deleted objects will not be removed from the board if the
 * "Save Board" button is not clicked
 * 
 * Accounts for the following cases:
 * 3 - delete existing item on board (add delete details to changesToBoard array)
 * 5 - delete item that was added (remove add details from changesToBoard array)
 * 
 * Author: Nathaniel Clark
 * ********************************************************************/

document.getElementById("delete-item-button").addEventListener("click", function() {
    let itemToDelete = document.getElementById("deleteModalWarning").getAttribute("data-id");
    let itemIndex = document.getElementById("deleteModalWarning").getAttribute("data-index");
    let itemTitle = document.getElementById("deleteModalWarning").getAttribute("data-delete-item-name");
    let itemDescription = document.getElementById("deleteModalWarning").getAttribute("data-delete-item-description");

    /******************************************
    * case 5 - delete item that was added      *
    *******************************************/
    let isCase3 = true;
    for (item in changesToBoard) {
        //delete item that was added but not saved to the database
        if (changesToBoard[item].changeType === "add" && changesToBoard[item].item_index === itemIndex && changesToBoard[item].title === itemTitle && changesToBoard[item].description === itemDescription){
            changesToBoard.pop(item);
            isCase3 = false;
            break;
        }
        //remove edit to an item being deleted
        if (changesToBoard[item].changeType === "edit" && changesToBoard[item].item_index === itemIndex){
            changesToBoard.pop(item);
            break;
        }
    }

    /******************************************
    * case 3 - delete existing item on board  *
    *******************************************/
    if (isCase3){
        changesToBoard.push(
            {
                changeType: "delete",
                item_id: itemToDelete,
                item_index: itemIndex,
            }
        );
    }


    // Remove the item from the board
    document.getElementById("board-item-container-" + itemIndex).remove();
    numberOfBoardItems = numberOfBoardItems - 1;
        
    if (numberOfBoardItems === 0) {
        let noItemsFoundDiv = document.createElement("div");
        noItemsFoundDiv.id = "no-items-found";
        noItemsFoundText = document.createElement("p");
        noItemsFoundText.textContent = "No items found";
        noItemsFoundDiv.appendChild(noItemsFoundText);
        document.getElementById("boardItems").appendChild(noItemsFoundDiv);
    }
        
    // Close the modal
    $('#deleteItem').modal('hide');
});

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
 * Adds an event listener to each item to do a specified action when clicked
 * What action that occurs is based on the current state
 * 
 * - view: Opens a modal to show the item's title and description
 * - edit: brings up modal to edit the name and description of the item
 * - delete: brings up modal to confirm deletion
 * 
 * Cases:  formate: case number, explanation of case, solution (not saved unless Save Board button pressed)
 *  1 - add new item to board (add details to changesToBoard array)
 *  2 - edit existing item on board (add edit details to changesToBoard array)
 *  3 - delete existing item on board (add delete details to changesToBoard array)
 *  4 - edit item that was added (replace add details with edited names and description)
 *  5 - delete item that was added (remove add details from changesToBoard array)
 *  6 - edited item was previously edited but not saved to database (replace edit details with new edit details)
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
                editItemTitle.setAttribute("data-index", index);

                let editItemDescription = document.getElementById("editItemDescriptionInput");
                editItemDescription.placeholder = itemDescription.textContent;
                editItemDescription.value = itemDescription.textContent;
                
                $('#editBoardItem').modal('show');
            }
    
            //bring up modal to confirm deletion
            else if (state === "delete"){
                let boardName = document.getElementById("board-item-" + index + "-title");
                let boardDescription = document.getElementById("board-item-" + index + "-description");
                let board_id = boardName.getAttribute("data-id");
                let deleteModalText = document.getElementById("deleteModalWarning");

                deleteModalText.textContent = "Are you sure you want to delete the item titled: " + boardName.textContent + "?";
                deleteModalText.setAttribute("data-id", board_id);
                deleteModalText.setAttribute("data-index", index);
                deleteModalText.setAttribute("data-delete-item-name", boardName.textContent);
                deleteModalText.setAttribute("data-delete-item-description", boardDescription.textContent);

                $('#deleteItem').modal('show');
            }
            console.log(changesToBoard);
        });
    })(i);
    //keep track of the number of items
    assignBoardId = assignBoardId + 1;
    numberOfBoardItems = numberOfBoardItems + 1;
    i = i + 1;
}
