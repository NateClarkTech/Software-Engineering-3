/**
 * Date Created: 4/09/2024
 * Date Modified: 4/27/2024
 * 
 * Author: Nathaniel Clark
* Purpose: This script is used to handle the functionality of the idea board page.
*/


console.log('script loaded');


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
