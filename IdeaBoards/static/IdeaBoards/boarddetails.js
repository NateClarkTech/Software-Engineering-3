/**
 * Date Created: 4/09/2024
 * Date Modified: 4/29/2024
 * 
 * Author: Nathaniel Clark
 * Purpose: This file is used to handle the javascript for the board details page
 */

console.log('script loaded');

//saves changes to be done to board
let changesToBoard = [];
let labelNames = [];

//Used for assigning a unique id to each board item
let assignBoardId = 1;

// Variable to keep track of the number of board items
let numberOfBoardItems = 0;

let boardSaved = true;

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
 * Allows the board to be edited by the user (changes must be saved)
 * 
 * Author: Nathaniel Clark
 * ********************************************************************/
document.getElementById("edit-board-button").addEventListener("click", function() {
    let newTitle = document.getElementById("editBoardTitleInput").value;
    let newDescription = document.getElementById("editBoardDescriptionInput").value;

    //if the input is valid, update the board details
    if (newTitle !== "" && newTitle.length <= 64 && newDescription.length <= 128) {
        boardSaved = false;
        changesToBoard.push(
            {
                changeType: "editBoardDetails",
                title: newTitle,
                description: newDescription,
                privacy_setting: document.getElementById("privacy_setting").checked,
            }
        );

        document.getElementById("board-title").textContent = "Project Board: " + newTitle;
        if (newDescription.length > 0) {
            document.getElementById("board-description").textContent = "Description: " + newDescription;

            if (document.getElementById("board-description").classList.contains("d-none")){
                document.getElementById("board-description").classList.remove("d-none");
            }
        }
        else {
            document.getElementById("board-description").classList.add("d-none");
        }
        
        $('#editBoard').modal('hide');       
    }
    //else show proper error modal
    else if (newTitle.length > 64){
        document.getElementById("error-modal-text").innerHTML = "Board title must be less than 64 characters";
        $('#editBoard').modal('hide');
        $('#errorModel').modal('show');
    }
    else if (newDescription.length > 128){
        document.getElementById("error-modal-text").innerHTML = "Board description must be less than 128 characters";
        $('#editBoard').modal('hide');
        $('#errorModel').modal('show');
    }
    else if (newTitle.length <= 0){
        document.getElementById("error-modal-text").innerHTML = "Board must have a title";
        $('#editBoard').modal('hide');
        $('#errorModel').modal('show');
    }
    else {
        document.getElementById("error-modal-text").innerHTML = "Unknown error has occured, please contact the site administrator";
        $('#editBoard').modal('hide');
        $('#errorModel').modal('show');
    }
});


/**********************************************************************
 * Deletes the board and redirects the user to the boards page
 * 
 * WARNING - Board will be deleted as soon as the button is clicked and cannot be undone
 * 
 * Author: Nathaniel Clark
 * ********************************************************************/
document.getElementById("delete-board-button").addEventListener("click", function() {
    changesToBoard = [];
    boardSaved = true;
    changesToBoard.push(
        {
            changeType: "deleteBoard",
            board_id: document.getElementById("delete-board-button").getAttribute("data-id"),
        }
    );


    // Perform DELETE request
    fetch(window.location.pathname, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify(changesToBoard)
    }).then(data => {
        console.log(data);
        window.location.href = "/boards";
    });
});

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
    // Get title, description, and uploaded files from the form
    let title = document.getElementById("title").value;
    let description = document.getElementById("description").value;
    let item_image = document.getElementById("item_image").files[0];
    let item_sound = document.getElementById("item_sound").files[0];
    let item_label = document.getElementById("labelSelect").value;

    if (title !== "" && title.length <= 64) {
        boardSaved = false;

        changesToBoard.push(
            {   
                changeType: "add",
                title: title,
                description: description,
                item_index: String(assignBoardId),
                item_image: item_image,
                item_sound: item_sound,
                note_label: item_label,
            }
        );

        // Div for new card
        let colDiv = document.createElement("div");
        colDiv.classList.add("col-md-4", "px-3", "py-3", "text-center");
        colDiv.id = "board-item-container-" + assignBoardId;
        
        //Add the card to contain everything
        let button = document.createElement("button");
        button.id = "board-item-" + assignBoardId;
        button.classList.add("btn", "btn-outline-primary", "btn-size");
        let card = document.createElement("div");
        card.classList.add("card", "card-custom");
        let cardBody = document.createElement("div");
        cardBody.classList.add("card-body");

        //If there is an image/sound/label file, add the icon to show it
        if (item_image || item_sound || item_label) {
            let rowDiv = document.createElement("div");
            rowDiv.classList.add("row", "justify-content-end", "mt-auto");

            if (item_image) {
                let imgIcon = document.createElement("img");
                imgIcon.setAttribute("id", "board-item-" + assignBoardId + "-img-icon");
                imgIcon.classList.add("col-3", "img-icon", "px-1", "mr-3");
                if (item_sound){
                    imgIcon.classList.remove("mr-3");
                }
                imgIcon.src = "/static/images/imageiconwhite.png";
                imgIcon.alt = "img icon";
                rowDiv.appendChild(imgIcon);
            }

            if (item_sound) {
                let audioIcon = document.createElement("img");
                audioIcon.src = "/static/images/audioiconwhite.png";
                audioIcon.classList.add("audio-icon", "mr-3", "px-1");
                rowDiv.appendChild(audioIcon);
            }
            if (item_label) {
                    /* FIX */
                    let label = document.createElement("p");
                    label.textContent = item_label;
                    rowDiv.appendChild(label);
                }
            cardBody.appendChild(rowDiv);
        }
        
        // Add the title to the card
        let cardTitle = document.createElement("h2");
        cardTitle.id = "board-item-" + assignBoardId + "-title";
        cardTitle.classList.add("card-title", "pb-2");
        cardTitle.textContent = title;
        if (item_image){
            cardTitle.setAttribute("data-img-src", URL.createObjectURL(item_image));
        }
        if (item_sound){
            cardTitle.setAttribute("data-sound-src", URL.createObjectURL(item_sound));
        }
        // May need FIX
        if (item_label){
            cardTitle.setAttribute("data-label", item_label);
        }
        
        // Add the description to the card
        let cardDescription = document.createElement("p");
        cardDescription.id = "board-item-" + assignBoardId + "-description";
        cardDescription.classList.add("card-description", "pb-2");
        cardDescription.textContent = description;

        // Add the new item via Javascript
        cardBody.appendChild(cardTitle);
        cardBody.appendChild(cardDescription);
        card.appendChild(cardBody);
        button.appendChild(card);
        colDiv.appendChild(button);
        
        // Add an event listener to the new item
        (function(index) {
            colDiv.addEventListener("click", function() {
            
            // Get all the items from the clicked item
            let itemTitle = document.getElementById("board-item-" + index + "-title");
            let itemDescription = document.getElementById("board-item-" + index + "-description");
            let item_id = document.getElementById("board-item-" + index + "-title").getAttribute("data-id");
            let img_src = itemTitle.getAttribute("data-img-src");
            let sound_src = itemTitle.getAttribute("data-sound-src");
            let label_name = document.getAttribute("data-label")

            document.getElementById("view-item-description").textContent = itemDescription.textContent;

            let modalTitle = document.getElementById("view-item-title");
            modalTitle.textContent = itemTitle.textContent;
            modalTitle.setAttribute("data-id", item_id);
            modalTitle.setAttribute("data-index", index);

            let modalImage = document.getElementById("view-item-image");
            if (img_src){
                modalImage.classList.remove("d-none");
                modalImage.setAttribute("src", img_src);
            }
            else{
                modalImage.classList.add("d-none");
            }
            
            let modalSound = document.getElementById("view-item-sound");
            if (sound_src){
                modalSound.classList.remove("d-none");
                modalSound.setAttribute("src", sound_src);
            }
            else{
                modalSound.classList.add("d-none");
            }
            
            let modalLabel = document.getElementById("view-item-label");
            if (label_name){
                modalLabel.classList.remove("d-none");
                modalLabel.textContent = label_name.textContent;
            }
            else{
                modalLabel.classList.add("d-none");
            }

            // Show the modal
            $('#viewBoardItem').modal('show');
            console.log(changesToBoard);
            });
        })(assignBoardId);

        // Add the new card to the "row" div
        document.getElementById("boardItems").appendChild(colDiv);

        // Increment the assignBoardId and numberOfBoardItems
        assignBoardId = assignBoardId + 1;
        numberOfBoardItems = numberOfBoardItems + 1;

        if (document.getElementById("no-items-found")) {
            document.getElementById("no-items-found").remove();
        }

        // Close the modal
        $('#createBoardItem').modal('hide');
    }
    // Show error modal if the title is too long or empty
    else if (title.length > 64){  
        document.getElementById("error-modal-text").innerHTML = "Title must be less than 64 characters";
        $('#createBoardItem').modal('hide');
        $('#errorModel').modal('show');
    }
    else if (title.length <= 0) {
        document.getElementById("error-modal-text").innerHTML = "Item must have a title";
        $('#createBoardItem').modal('hide');
        $('#errorModel').modal('show');
    }
    //Fallback case, if this happens something went terribly wrong
    else{
        document.getElementById("error-modal-text").innerHTML = "Unknown error has occured, please contact the site administrator";
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
    let itemToEdit = document.getElementById("view-item-title").getAttribute("data-id");
    let itemIndex = document.getElementById("view-item-title").getAttribute("data-index");
    let itemTitle = document.getElementById("board-item-" + itemIndex + "-title");
    let newTitle = document.getElementById("editItemTitleInput").value;
    let newDescription = document.getElementById("editItemDescriptionInput").value;
    let newImage = document.getElementById("editItemImage").files[0];
    let newSound = document.getElementById("editItemSound").files[0];
    let newLabel = document.getElementById("labelSelect").value;
    let removeImage = document.getElementById("removeImage").checked;
    let removeSound = document.getElementById("removeSound").checked;
    let removeLabel = document.getElementById("removeLabel").checked;

    // Make sure input is valid, else give error modal
    if (newTitle !== "" && newTitle.length <= 64) {

        /*************************************
        * case 4 - edit item that was added  *
        **************************************/
        let isCase2 = true;
        for (item in changesToBoard) {
            if (changesToBoard[item].changeType === "add" && changesToBoard[item].item_index === itemIndex){
                changesToBoard[item].title = newTitle;
                changesToBoard[item].description = newDescription;

                if (document.getElementById("editItemImage").files[0]){
                    changesToBoard[item].item_image = newImage;
                }
                if (document.getElementById("editItemSound").files[0]){
                    changesToBoard[item].item_sound = newSound;
                }

                if (removeImage){
                    changesToBoard[item].item_image = null;
                }

                if (removeSound){
                    changesToBoard[item].item_sound = null;
                }
                
                itemTitle.textContent = newTitle;
                if (newImage){
                    itemTitle.setAttribute("data-img-src", URL.createObjectURL(newImage));
                }
                if (newSound){
                    itemTitle.setAttribute("data-sound-src", URL.createObjectURL(newSound));
                }

                if (document.getElementById("removeImage").checked){
                    itemTitle.removeAttribute("data-img-src");
                }
                if (document.getElementById("removeSound").checked){
                    itemTitle.removeAttribute("data-sound-src");
                }

                $('#editBoardItem').modal('hide');

                return;
            }
            /*************************************
            * case 6 - edit past edit request  *
            **************************************/
            if (changesToBoard[item].changeType === "edit" && changesToBoard[item].item_index === itemIndex){
                changesToBoard[item].title = newTitle;
                changesToBoard[item].description = newDescription;
                
                if (newImage){
                    changesToBoard[item].item_image = newImage;
                    itemTitle.setAttribute("data-img-src", URL.createObjectURL(newImage));
                }
                if (newSound){
                    changesToBoard[item].item_sound = newSound;
                    itemTitle.setAttribute("data-sound-src", URL.createObjectURL(newSound));
                }

                if (removeImage){
                    changesToBoard[item].item_image = null;
                    itemTitle.removeAttribute("data-img-src");
                }

                if (removeSound){
                    changesToBoard[item].item_sound = null;
                    itemTitle.removeAttribute("data-sound-src");
                }

                isCase2 = false;

                break;
            }
        }

        /********************************************
        * case 2 - edit item exisiting on the board *
        *********************************************/
        if (isCase2){
            // Add the edit to the changesToBoard array
            changesToBoard.push({
                changeType: "edit",
                item_id: itemToEdit,
                title: newTitle,
                description: newDescription,
                item_index: itemIndex,
                item_image: removeImage ? null : newImage, // If removeImage is true set the image to null
                item_sound: removeSound ? null : newSound, // If removeSound is true set the sound to null
            });
        

            if (newImage){
                itemTitle.setAttribute("data-img-src", URL.createObjectURL(newImage));
            }
            if (newSound){
                itemTitle.setAttribute("data-sound-src", URL.createObjectURL(newSound));
            }

            if (removeImage){
                itemTitle.removeAttribute("data-img-src");
            }
            if (removeSound){
                itemTitle.removeAttribute("data-sound-src");
            }

            boardSaved = false;
        }

        // Update the title and description of the item
        document.getElementById("board-item-" + itemIndex + "-title").textContent = newTitle;
        document.getElementById("board-item-" + itemIndex + "-description").textContent = newDescription;

        // Close the modal
        $('#editBoardItem').modal('hide');
    }
    // Show error modal if the title is too long or empty
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
    //Fallback case, if this happens something went terribly wrong
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
    let itemToDelete = document.getElementById("view-item-title").getAttribute("data-id");
    let itemIndex = document.getElementById("view-item-title").getAttribute("data-index");
    let itemTitle = document.getElementById("view-item-title").textContent;
    let itemDescription = document.getElementById("view-item-description").textContent;

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

        boardSaved = false;
    }


    // Remove the item from the board
    document.getElementById("board-item-container-" + itemIndex).remove();
    numberOfBoardItems = numberOfBoardItems - 1;
        
    if (numberOfBoardItems === 0) {
        let noItemsFoundDiv = document.createElement("div");
        noItemsFoundDiv.className = "card mx-auto";
        noItemsFoundDiv.id = "no-items-found";

        let cardBodyDiv = document.createElement("div");
        cardBodyDiv.className = "card-body";

        let cardTextH1 = document.createElement("h1");
        cardTextH1.className = "card-text text-center";
        cardTextH1.textContent = "You don't have any notes yet.";

        cardBodyDiv.appendChild(cardTextH1);
        noItemsFoundDiv.appendChild(cardBodyDiv);
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
    if (changesToBoard.length === 0) {
        return;
    }

    // Create a new FormData object
    let formData = new FormData();

    formData.append("numChanges", changesToBoard.length);

    // Iterate over each change to append file data
    changesToBoard.forEach((change, index) => {
        if (change.changeType === "add") {
            // Append each change individually
            formData.append(`${index}_change_type`, change.changeType);
            formData.append(`${index}_title`, change.title);
            formData.append(`${index}_description`, change.description);
            formData.append(`${index}_item_index`, change.item_index);
            formData.append(`${index}_item_image`, change.item_image || null);
            formData.append(`${index}_item_sound`, change.item_sound || null);
            formData.append(`${index}_item_label`, change.note_label || null);
        }
        
        if (change.changeType === "edit") {
            formData.append(`${index}_change_type`, change.changeType);
            formData.append(`${index}_item_id`, change.item_id);
            formData.append(`${index}_title`, change.title);
            formData.append(`${index}_description`, change.description);
            formData.append(`${index}_item_index`, change.item_index);
            formData.append(`${index}_item_label`, change.note_label || null);
            if (change.item_image){
                formData.append(`${index}_item_image`, change.item_image);
            }
            if (change.item_image === null){
                formData.append(`${index}_remove_image`, true);
            }

            if (change.item_sound){
                formData.append(`${index}_item_sound`, change.item_sound);
            }
            if (change.item_sound === null){
                formData.append(`${index}_remove_sound`, true);
            }

            if (change.note_label){
                formData.append(`${index}_item_label`, change.note_label);
            }
            if (change.note_label === null){
                formData.append(`${index}_remove_label`, true);
            }
        }

        if (change.changeType === "delete") { 
            formData.append(`${index}_change_type`, change.changeType);
            formData.append(`${index}_item_id`, change.item_id);
            formData.append(`${index}_item_index`, change.item_index);
        }

        if (change.changeType === "editBoardDetails") {
            formData.append(`${index}_change_type`, change.changeType);
            formData.append(`${index}_title`, change.title);
            formData.append(`${index}_description`, change.description);
            formData.append(`${index}_privacy_setting`, change.privacy_setting);
        }

        if (change.changeType === "addLabel") {
            formData.append(`${index}_change_type`, change.changeType);
            formData.append(`${index}_labelName`, change.labelName);
        }

    });

    // Send the POST request
    fetch(window.location.pathname, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: formData,

    }).then(response => {
        console.log(response);
        boardSaved = true;
        location.reload();
    }).catch(error => {
        console.error('Error:', error);
    });
});

/**********************************************************************
 * Adds an event listener to each item so when they are clicked they open up in the view modal
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
            let itemTitle = document.getElementById("board-item-" + index + "-title");
            let itemDescription = document.getElementById("board-item-" + index + "-description");
            let item_id = document.getElementById("board-item-" + index + "-title").getAttribute("data-id");
            let img_src = itemTitle.getAttribute("data-img-src");
            let item_label = itemTitle.getAttribute("data-label");

            let modalTitle = document.getElementById("view-item-title");
            modalTitle.textContent = itemTitle.textContent;
            modalTitle.setAttribute("data-id", item_id);
            modalTitle.setAttribute("data-index", index);

            let modalImage = document.getElementById("view-item-image");
            if (itemTitle.getAttribute("data-img-src")){
                modalImage.classList.remove("d-none");
                modalImage.setAttribute("src", img_src);
            }
            else{
                modalImage.classList.add("d-none");
            }
            
            let modalSound = document.getElementById("view-item-sound");
            if (itemTitle.getAttribute("data-sound-src")){
                modalSound.classList.remove("d-none");
                modalSound.setAttribute("src", itemTitle.getAttribute("data-sound-src"));
            }
            else{
                modalSound.classList.add("d-none");
            }

            let modalLabel = document.getElementById("view-item-label");
            if (itemTitle.getAttribute("data-label")){
                modalLabel.classList.remove("d-none");
                modalLabel.textContent = item_label;
            }
            else{
                modalLabel.classList.add("d-none");
            }

            document.getElementById("view-item-description").textContent = itemDescription.textContent;
            
            $('#viewBoardItem').modal('show');
            console.log(changesToBoard);
        });
    
    })(i);
    //keep track of the number of items
    assignBoardId = assignBoardId + 1;
    numberOfBoardItems = numberOfBoardItems + 1;
    i = i + 1;
}

/**********************************************************************
 * Adds an event listener to the edit item button
 * Takes the currently viewed item and opens the edit modal with the item's details
 * 
 * Author: Nathaniel Clark 
 * ********************************************************************/
document.getElementById("edit-item-modal-button").addEventListener("click", function() {
    let itemTitle = document.getElementById("view-item-title");
    let itemDescription = document.getElementById("view-item-description");
    let item_id = itemTitle.getAttribute("data-id");
    
    //set the title input field to the current title
    let editItemTitle = document.getElementById("editItemTitleInput");
    editItemTitle.placeholder = itemTitle.textContent.trim();
    editItemTitle.value = itemTitle.textContent.trim();
    editItemTitle.setAttribute("data-id", item_id);

    //set the description input field to the current description
    let editItemDescription = document.getElementById("editItemDescriptionInput");
    editItemDescription.placeholder = itemDescription.textContent;
    editItemDescription.value = itemDescription.textContent;
        
    //enable the image and sound inputs
    let img_upload = document.getElementById("editItemImage");
    img_upload.disabled = false;
    let sound_upload = document.getElementById("editItemSound");
    sound_upload.disabled = false;

    //reset the remove image and sound checkboxes
    document.getElementById("removeImage").checked = false;
    document.getElementById("removeSound").checked = false;

    //if there is no image or sound, disable the input fields
    if (document.getElementById("view-item-image").classList.contains("d-none")){
        document.getElementById("modal-item-remove-image").classList.add("d-none");
    }
    else{
        document.getElementById("modal-item-remove-image").classList.remove("d-none");
    }

    if (document.getElementById("view-item-sound").classList.contains("d-none")){
        document.getElementById("modal-item-remove-sound").classList.add("d-none");
    }
    else{
        document.getElementById("modal-item-remove-sound").classList.remove("d-none");
    }

    //reset the image and sound inputs
    document.getElementById("editItemImage").value = "";
    document.getElementById("editItemSound").value = "";
    
    $('#viewBoardItem').modal('hide');
    $('#editBoardItem').modal('show');
});

document.getElementById("removeImage").addEventListener("click", function() {
    let removeImageToggle = document.getElementById("removeImage");
    if (removeImageToggle.checked === true){
        document.getElementById("editItemImage").disabled = true;
        document.getElementById("editItemImage").value = "";
    }
    else{
        document.getElementById("editItemImage").disabled = false;
    }
});

document.getElementById("removeSound").addEventListener("click", function() {
    let removeSoundToggle = document.getElementById("removeSound");
    if (removeSoundToggle.checked === true){
        document.getElementById("editItemSound").disabled = true;
        document.getElementById("editItemSound").value = "";
    }
    else{
        document.getElementById("editItemSound").disabled = false;
    }
});

/**********************************************************************
 * Adds an event listener to the delete item button
 * Takes the currently viewed item and opens the delete modal with the item's details
 * 
 * Author: Nathaniel Clark 
 * ********************************************************************/
document.getElementById("delete-item-modal-button").addEventListener("click", function() {
    let itemTitle = document.getElementById("view-item-title");
    let itemDescription = document.getElementById("view-item-description");
    let item_id = itemTitle.getAttribute("data-id");
    let deleteModalText = document.getElementById("deleteModalWarning");

    //set the text of the delete modal to the item's title
    deleteModalText.textContent = "Are you sure you want to delete the item titled: " + itemTitle.textContent + "?";
    deleteModalText.setAttribute("data-id", item_id);
    deleteModalText.setAttribute("data-index", itemTitle.getAttribute("data-index"));
    deleteModalText.setAttribute("data-delete-item-name", itemTitle.textContent);
    deleteModalText.setAttribute("data-delete-item-description", itemDescription.textContent);

    $('#viewBoardItem').modal('hide');
    $('#deleteItem').modal('show');
});


/**********************************************************************
 * If the user has an unsaved board, ask user to confirm if they want to leave the page and remind to save
 * 
 * Author: Nathaniel Clark
 * Resource Used: https://stackoverflow.com/questions/2229942/how-to-block-users-from-closing-a-window-in-javascript
 * ********************************************************************/
window.onbeforeunload = function() {
    //if the board has not been saved, ask the user to confirm they want to leave the page
    if (!boardSaved) {
        return "Changes to the board have not been saved. Please save your changes before closing the page.";
    }
};


src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"

/*
//         Sort Label
//     @author: Bilge Akyol
*/
var labels = document.querySelectorAll('[id^="sort-label-"]');

// Loop through each label element and attach a click event listener
labels.forEach(function(label) {
    label.addEventListener('click', function() {
        var labelText = label.textContent;
        var labelId = label.getAttribute('data-id');
        var request = 'POST';
        
        // Construct the data to be sent
        var data = {
            request: request,
            id: labelId,
            label: labelText
        };
        
        // Construct the request
        var requestOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrfToken'),
            },
            body: JSON.stringify(data)
        };
        
        // Perform any necessary action with the label data here
        
        // Redirect to the specified URL
        window.location.href = labelText;
    });
});

/*
        Create Label
    @author: Bilge Akyol
*/ 
document.getElementById("create-label").addEventListener("click", function() {
    $('#createLabel').modal('show');
});

document.getElementById("add-label-button").addEventListener("click", function() {    

    new_label = document.getElementById("new-label-name").value;

    if (new_label.length <= 0){
        document.getElementById("error-modal-text").innerHTML = "Label can't be empty";
        $('#editBoardItem').modal('hide');
        $('#errorModel').modal('show');
    }
    duplicate_label=false;
    labels.forEach(function(label) {
        if(new_label = label.textContent){
            duplicate_label=true;
            document.getElementById("error-modal-text").innerHTML = "Label exists";
            $('#editBoardItem').modal('hide');
            $('#errorModel').modal('show');
        }
            
    });
    if(!duplicate_label){
        changesToBoard.push(
            {
                changeType: "addLabel",
                labelName: new_label,
            }
        );    
        boardSaved = false;
        
        let newLabelButton = document.createElement("button");
        newLabelButton.type = "button";
        newLabelButton.classList.add("btn", "btn-primary", "my-1", "col-md-1.5", "ml-1");
        newLabelButton.textContent = new_label;   

        let labelRow = document.getElementById("labelRow");
        labelRow.appendChild(newLabelButton);

        $('#createLabel').modal('hide');
    }
});
