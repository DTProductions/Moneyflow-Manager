document.addEventListener("DOMContentLoaded", (Event) =>{
    document.querySelector("#submit").addEventListener("click", ()=> {
        add_register(document.getElementById("add_form"),"/categories/add", "/categories");
    });
});