document.addEventListener("DOMContentLoaded", (Event) =>{

    //get elements from DOM
    let rows = document.getElementById("data").querySelectorAll("tr");
    let search_txt = document.getElementById("search-txt");
    let field_dropdown = document.getElementById("field");
    let check_boxes = document.getElementById("data").querySelectorAll(".checkB");
    let form = document.getElementById("update_form");

    //set search events
    search_txt.addEventListener("keyup", () =>{
        search(field_dropdown, rows, search_txt);
    });
    search_txt.addEventListener("search", () =>{
        search(field_dropdown, rows, search_txt);
    });
    field_dropdown.addEventListener("change", () =>{
        search(field_dropdown, rows, search_txt);
    });

    //set update and delete events
    if(location.pathname == "/categories"){
        document.querySelector("#update").addEventListener("click", () =>{
            sendForm(rows, check_boxes, form, ["name","type"], "id");
        });
        document.querySelector("#remove").addEventListener("click", ()=> {
            remove(check_boxes, "/categories/remove");
        });
    }
    else if(location.pathname == "/transactions"){
        document.querySelector("#update").addEventListener("click", () =>{
            sendForm(rows, check_boxes, form, ["date", "ammount", "currency", "category_name"], "id");
        });
        document.querySelector("#remove").addEventListener("click", ()=> {
            remove(check_boxes, "/transactions/remove");
        });
    }

    colorTable(rows, "#063688", "#004FD6");
});

function search(dropdown, rows, search_txt){
    switch(dropdown.value){
        case "Name":
            search_by_text("name", rows, search_txt);
            break;
        case "Type":
            search_by_text("type", rows, search_txt);
            break;
    }
}
