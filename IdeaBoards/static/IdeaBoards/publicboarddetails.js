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

//Used for assigning a unique id to each board item
let assignBoardId = 1;

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
            let img_src = itemTitle.getAttribute("data-img-src");

            console.log(img_src);

            let modalTitle = document.getElementById("view-item-title");
            modalTitle.textContent = itemTitle.textContent;
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

            document.getElementById("view-item-description").textContent = itemDescription.textContent;
            
            $('#viewBoardItem').modal('show');
            console.log(changesToBoard);
        });
    
    })(i);
    //keep track of the number of items
    assignBoardId = assignBoardId + 1;
    i = i + 1;
}
