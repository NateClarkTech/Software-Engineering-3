/**
 * Date Created: 4/09/2024
 * Date Modified: 4/27/2024
 * 
 * Author: Nathaniel Clark
* Purpose: This script is used to handle the functionality of the idea board page.
*/


console.log('script loaded');

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
            window.location.href = board.getAttribute("data-url");
        });
    })(i);
    i = i + 1;
}


/* 
****** Spotify Song Reccommendation ********
*/
// JavaScript to handle form submission and displaying result
document.getElementById('getRecc').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission
      
    // Get input value
    var genreName = document.getElementById('genreNameInput').value;
    console.log(genreName)
    fetch(window.location.pathname, {
        method: "GETRECC",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")  // Include the CSRF token in the headers
        },
        body: JSON.stringify([{genreName: genreName}]),
    }).then(response => response.json())
    .then(data => {
        /*
        reccResult = document.getElementById("reccResult");
        reccResult.textContent = data.message;
        */
        url = 'https://open.spotify.com/oembed?url=' + data;
        iframe.setAttribute("src", url);
        $('#getRecc').modal('hide');
        $('#displayReccResults').modal('show');
    })
    
});