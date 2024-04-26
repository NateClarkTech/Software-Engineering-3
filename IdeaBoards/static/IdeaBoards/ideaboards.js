/**
 * Date Created: 4/24/2024
 * Date Modified: 4/24/2024
 * 
 * Author: Nathaniel Clark
* Purpose: This script is used to handle the functionality of the idea board page.
*/


console.log('script loaded');

// Set the initial state to "view"
let state = "view";
document.getElementById("modes").value = "view";

const csrftoken = getCookie('csrftoken');

/**********************************************************************
 * Adds an event listener to each board to do a specified action when clicked
 * What action that occurs is based on the current state
 * 
 * - view: Redirects to the board's detail page
 * - edit: brings up modal to edit the name and description of the board
 * - delete: brings up modal to confirm deletion
 * 
 * Author: Nathaniel Clark
 **********************************************************************/
let i = 1;
while (document.getElementById("board-" + i)) {
    //add an event listener to each board
    (function(index) {
        let board = document.getElementById("board-" + index)

        board.addEventListener("click", function() {
            //redirect to the board's detail page
            if (state === "view"){
                window.location.href = board.getAttribute("data-url");
            }
            
            //bring up modal to edit the name and description of the board
            else if (state === "edit"){
                let boardName = document.getElementById("board-" + index + "-title").textContent;
                let boardDescription = document.getElementById("board-" + index + "-description").textContent;
                let board_id = board.getAttribute("data-url");

                editBoardTitle = document.getElementById("editBoardTitleInput");
                editBoardTitle.placeholder = boardName;
                editBoardTitle.value = boardName;
                editBoardTitle.setAttribute("data-id", board_id);

                editBoardDescription = document.getElementById("editBoardDescriptionInput");
                editBoardDescription.placeholder = boardDescription;
                editBoardDescription.value = boardDescription;

                $('#editBoard').modal('show');
            }

            //bring up modal to confirm deletion
            else if (state === "delete"){
                let boardName = document.getElementById("board-" + index + "-title").textContent;
                let board_id = board.getAttribute("data-url");
                let deleteModalText = document.getElementById("deleteModalWarning");
                deleteModalText.textContent = "Are you sure you want to delete the board: " + boardName + "?";
                deleteModalText.setAttribute("data-id", board_id);

                $('#deleteBoard').modal('show');
            }
        });
    })(i);
    i = i + 1;
}

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
 * Sends a DELETE request to delete the board with the given board_id.
 * 
 * Author: Nathaniel Clark
 * formate gotten from chat GPT
 * https://chat.openai.com/share/274e26c2-df74-4548-926b-cde8ff1216b0
 **********************************************************************/
document.getElementById("delete-board-button").addEventListener("click", function() {
    // Send the DELETE request with the CSRF token included in the headers

    let boardToDelete = document.getElementById("deleteModalWarning").getAttribute("data-id");

    fetch(window.location.pathname, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken  // Include the CSRF token in the headers
        },
        body: JSON.stringify([{type: "delete", board_id: boardToDelete}]),
    }).then(data => {
        console.log(data);
        window.location.href = "/";
    })
});

/**********************************************************************
 * Sends a PATCH request to edit the board with the given board_id.
 * 
 * Author: Nathaniel Clark
 * formate gotten from chat GPT
 * https://chat.openai.com/share/274e26c2-df74-4548-926b-cde8ff1216b0
 **********************************************************************/
document.getElementById("edit-board-button").addEventListener("click", function() {
    // Send the PATCH request with the CSRF token included in the headers

    let boardToEdit = document.getElementById("editBoardTitleInput").getAttribute("data-id");
    let newTitle = document.getElementById("editBoardTitleInput").value;
    let newDescription = document.getElementById("editBoardDescriptionInput").value;

    //Throw error if title is too long
    if (newTitle.length > 64){
        errorText = document.getElementById("errorText");
        errorText.textContent = "Title must be less than 64 characters";

        $('#editBoard').modal('hide');
        $('#errorModal').modal('show');
    }
    else if (newDescription.length > 128){
        errorText = document.getElementById("errorText");
        errorText.textContent = "Description must be less than 128 characters";

        $('#editBoard').modal('hide');
        $('#errorModal').modal('show');
    }
    //Throw error if a field is empty
    else if (newTitle === "") {
        errorText = document.getElementById("errorText");
        errorText.textContent = "Project board must have a title";

        $('#editBoard').modal('hide');
        $('#errorModal').modal('show');
    }
    //If the two above tests
    else if (newTitle !== ""){
        fetch(window.location.pathname, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken  // Include the CSRF token in the headers
            },
            body: JSON.stringify([{type: "edit", board_id: boardToEdit, newTitle: newTitle, newDescription: newDescription}]),
        }).then(data => {
            $('#editBoard').modal('hide');
            console.log(data);
            window.location.href = "/";
        })
    }
    //Something has gone very wrong
    else {
        errorText = document.getElementById("errorText");
        errorText.textContent = "An Unknown Error has occured, please contact the site administrator";

        $('#editBoard').modal('hide');
        $('#errorModel').modal('show');
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


// JavaScript to handle form submission and displaying result
document.getElementById('get-recc-button').addEventListener('click', function(event) {
    console.log("Form submitted");
      
    // Get input value
    var inputData = document.getElementById('genreName').value;
      
    // Send input data to Django view using AJAX
    $.ajax({
        url: '/get_recc/',
        method: 'POST',
        dataType: 'json',
        data: {
        input_data: inputData,
        csrfmiddlewaretoken: '{{ csrf_token }}' // Adding CSRF token for security
        },
        success: function(data) {
            var recommendations = data.result;
            var recommendationsList = $('#recommendationsList');
            recommendationsList.empty(); // Clear previous recommendations

            // Append each recommendation to the list
            recommendations.forEach(function(recommendation) {
                recommendationsList.append('<li>' + recommendation + '</li>');
            });

            // Show the recommendations modal
            $('#recommendationsModal').modal('show');
        console.log("success");
        // Display the result from backend
        document.getElementById('resultText').innerText = data.result;
        document.getElementById('resultArea').style.display = 'block';
        },
        error: function(xhr, status, error) {
        console.error('Error:', error);
        }
    });
});