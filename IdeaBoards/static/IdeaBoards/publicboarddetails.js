/**
 * Date Created: 4/09/2024
 * Date Modified: 5/10/2024
 * 
 * Author: Nathaniel Clark
 * Purpose: This file is used to handle the javascript for the public board view.
 */

console.log('script loaded');

//saves changes to be done to board
let changesToBoard = [];

//Used for assigning a unique id to each board item
let assignBoardId = 1;

/**********************************************************************
 * Adds an event listener to each item so when they are clicked they open up in the view modal
 * 
 * Author: Nathaniel Clark
 **********************************************************************/
let i = 1;
while (document.getElementById("board-item-" + i)) {
    // Add an event listener to the item
    (function(index) {
        let item = document.getElementById("board-item-" + index);
        
        item.addEventListener("click", function() {
            //get the item's title, description, image, sound, and label
            let itemTitle = document.getElementById("board-item-" + index + "-title");
            let itemDescription = document.getElementById("board-item-" + index + "-description");
            let item_id = document.getElementById("board-item-" + index + "-title").getAttribute("data-id");
            let img_src = itemTitle.getAttribute("data-img-src");
            let item_label = itemTitle.getAttribute("data-label");

            //set the modal's title, description, image, sound, and label
            let modalTitle = document.getElementById("view-item-title");
            modalTitle.textContent = itemTitle.textContent;
            modalTitle.setAttribute("data-id", item_id);
            modalTitle.setAttribute("data-index", index);
            document.getElementById("view-item-description").textContent = itemDescription.textContent;

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
            
            //show the modal
            $('#viewBoardItem').modal('show');
        });
    
    })(i);
    //keep track of the number of items
    assignBoardId = assignBoardId + 1;
    i = i + 1;
}


/************************************************************************************************************
 * Add an event listener to each label so that when they are clicked only items with that label are shown   *
 *                                                                                                          *
 * The label will loop through each item and check if the label matches the item's label                    *
 * If the label matches the item's label then the item will be shown                                        *
 * Else the item will be hidden                                                                             *
 *                                                                                                          *
 * Author: Nathaniel Clark                                                                                  *
 ************************************************************************************************************/
i = 1;
while (document.getElementById("sort-label-" + i)) {
    (function (index){
        // Get the label
        let label = document.getElementById("sort-label-" + index);
        let labelName = label.getAttribute("data-label");

        // Add an event listener to the label
        label.addEventListener("click", function() {
            // Loop through each item
            // using j < assignBoardId insures that even if items are deleted via other functions the function still works
            let j = 1;
            while (j < assignBoardId){
                // Check an item at the current index exists
                if (document.getElementById("board-item-container-" + j)){

                    // Get the item and its label
                    let itemContainer = document.getElementById("board-item-container-" + j);
                    let item = document.getElementById("board-item-" + j + "-title");
                    let itemLabel = item.getAttribute("data-label");

                    // If the labels match show the item
                    if (itemLabel === labelName){
                        itemContainer.classList.remove("d-none");
                    }
                    // else hide the item
                    else{
                        itemContainer.classList.add("d-none");
                    }
                }
                j = j + 1;
            }
        });
    })(i);
    i = i + 1;
}

/****************************************************************
 * Add an event listener to the show all items button           *
 *                                                              *
 * The function loops through each item and unhides all items   *
 *                                                              *
 * Author: Nathaniel Clark                                      *
 ***************************************************************/
document.getElementById("show-all-items").addEventListener("click", function() {
    let index = 0;
    //loop though each item and unhide them, assignBoardId insures that 
    //even if items are deleted via other functions the function still unhides all items
    while(index < assignBoardId){
        if (document.getElementById("board-item-container-" + index)){
            document.getElementById("board-item-container-" + index).classList.remove("d-none");
        }
        index = index + 1;
    }
});


