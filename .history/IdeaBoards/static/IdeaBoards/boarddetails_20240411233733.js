console.log('script loaded');

document.getElementById("addItemForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Call the addFormItem function
    addFormItem();
});

function addFormItem() {
    // JavaScript function to handle adding form item
    // You can implement your logic here
    console.log("Form submitted! Now calling addFormItem function...");
    // Example: You can retrieve form data and process it here
    let title = document.getElementById("title").value;
    let description = document.getElementById("description").value;
    console.log("Title:", title);
    console.log("Description:", description);

    // You can perform additional actions or send the form data to a server using AJAX here
}