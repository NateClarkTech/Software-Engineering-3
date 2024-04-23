console.log('script loaded');

let state = "view";
const csrftoken = getCookie('csrftoken');

/**********************************************************************
 * Adds an event listener to each board to do a specified action when clicked
 * What action that occurs is based on the current state
 * 
 * - view: Redirects to the board's detail page
 * - edit: brings up modal to edit the name and description of the board
 * - delete: brings up modal to confirm deletion
 **********************************************************************/
let i = 1;
while (document.getElementById("board-" + i)) {
    //add an event listener to each board
    (function(index) {
        let board = document.getElementById("board-" + index)

        document.getElementById("board-" + index).addEventListener("click", function() {
            //redirect to the board's detail page
            if (state === "view"){
                window.location.href = board.getAttribute("data-url");
            }
            
            //bring up modal to edit the name and description of the board
            if (state === "edit"){}

            //bring up modal to confirm deletion
            if (state === "delete"){
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
 * Sends a Post request to delete the board with the given board_id.
 **********************************************************************/
document.getElementById("delete-board-button").addEventListener("click", function() {
    // Send the POST request with the CSRF token included in the headers

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

// Get the CSRF token from the cookie
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