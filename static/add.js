document.addEventListener("DOMContentLoaded", (Event) =>{
    document.getElementById("submit").addEventListener("click", ()=> {
        add_register(document.getElementById("add_form"),location.pathname.replace("/forms",""), "/" + location.pathname.split("/")[1]);
    });
});
