console.log('script loaded');

let changesToBoard = [];
const csrftoken = getCookie('csrftoken');

// Function to add a new item to the board
function addFormItem() {
    // Example: Get the title and description values from the form
    let title = document.getElementById("title").value;
    let description = document.getElementById("description").value;

    if (title !== "" && description !== "") {
        changesToBoard.push(
            {   
                type: "add",
                title: title,
                description: description
            }
        );
        console.log(changesToBoard);

        // Create new elements
        let colDiv = document.createElement("div");
        colDiv.classList.add("col-md-4");

        let button = document.createElement("button");
        button.id = "board-item-" + changesToBoard.length;
        button.classList.add("btn", "btn-outline-primary");

        let card = document.createElement("div");
        card.classList.add("card");

        let cardBody = document.createElement("div");
        cardBody.classList.add("card-body");

        let cardTitle = document.createElement("h2");
        cardTitle.id = "board-item-" + changesToBoard.length + "-title";
        cardTitle.classList.add("card-title");
        cardTitle.style.color = "black";
        cardTitle.textContent = title;

        let cardDescription = document.createElement("p");
        cardDescription.id = "board-item-" + changesToBoard.length + "-description";
        cardDescription.classList.add("card-description");
        cardDescription.style.color = "black";
        cardDescription.textContent = description;

        // Build the hierarchy
        cardBody.appendChild(cardTitle);
        cardBody.appendChild(cardDescription);
        card.appendChild(cardBody);
        button.appendChild(card);
        colDiv.appendChild(button);

        // Add the new card to the "row" div
        document.getElementById("boardItems").appendChild(colDiv);

        // Close the modal
        $('#createBoardItem').modal('hide');

        if (document.getElementById("no-items-found")) {
            document.getElementById("no-items-found").remove();
        }
    }
}

// Add an event listener to the form so items can be added to the board
document.getElementById("addItemForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Call the addFormItem function
    addFormItem();

    // Reset the form
    document.getElementById("addItemForm").reset();
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

document.getElementById("saveChanges").addEventListener("click", function() {
    // Send the POST request with the CSRF token included in the headers
    fetch(window.location.pathname, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken  // Include the CSRF token in the headers
        },
        body: JSON.stringify(changesToBoard),
    })
});

let i = 1;
while (document.getElementById("board-item-" + i)) {
    (function(index) {
        document.getElementById("board-item-" + index).addEventListener("click", function() {
            let title = document.getElementById("board-item-" + index + "-title").textContent;
            let description = document.getElementById("board-item-" + index + "-description").textContent;

            document.getElementById("view-item-title").textContent = title;
            document.getElementById("view-item-text").textContent = description;

            $('#viewBoardItem').modal('show');
        });
    })(i);
    i = i + 1;
}
