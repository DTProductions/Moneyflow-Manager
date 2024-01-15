let table_rows;
let search_txt;
let field_dropdown;
let rows;

document.addEventListener("DOMContentLoaded", (Event) =>{
    if(document.querySelector("#submit") != null){
        document.querySelector("#submit").addEventListener("click", ()=> {
            add_register(document.getElementById("add_form"),"/categories/add", "/categories");
        });
    }
    
    rows = document.getElementById("data").querySelectorAll("tr");
    colorTable();

    table_rows = document.getElementById("data");
    search_txt = document.getElementById("search-txt");
    field_dropdown = document.getElementById("field");

    search_txt.addEventListener("keyup", search);
    search_txt.addEventListener("search", search);
    field_dropdown.addEventListener("change", search);

    document.querySelector("#update").addEventListener("click", update);
    document.querySelector("#remove").addEventListener("click", ()=> {
        remove(document.getElementById("data").querySelectorAll(".checkB"), "/categories/remove");
    });
});

function colorTable(){
    for(let i = 0; i < rows.length; i++){
        if(i % 2 == 0){
            rows[i].style.backgroundColor = "#063688";
        }
        else{
            rows[i].style.backgroundColor = "#004FD6";
        }
    }
}

function search(e){
    switch(field_dropdown.value){
        case "Name":
            search_by_text("name", rows, search_txt);
            break;
        case "Type":
            search_by_text("type", rows, search_txt);
            break;
    }
}
