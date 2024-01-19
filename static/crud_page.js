document.addEventListener("DOMContentLoaded", (Event) =>{

    //get elements from DOM
    let rows = document.getElementById("data").querySelectorAll("tr");
    let search_txt = document.getElementById("search-txt");
    let field_dropdown = document.getElementById("field");
    let check_boxes = document.getElementById("data").querySelectorAll(".checkB");
    let form = document.getElementById("update_form");

    let start_date = document.getElementById("start_date");
    let end_date = document.getElementById("end_date");

    //set search events
    search_txt.addEventListener("keyup", () =>{
        search(field_dropdown, rows, search_txt, start_date, end_date);
    });
    search_txt.addEventListener("search", () =>{
        search(field_dropdown, rows, search_txt, start_date, end_date);
    });
    field_dropdown.addEventListener("change", () =>{
        search(field_dropdown, rows, search_txt, start_date, end_date);
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
        start_date.addEventListener("change", () =>{
            search(field_dropdown, rows, search_txt, start_date, end_date);
        });
        end_date.addEventListener("change", () =>{
            search(field_dropdown, rows, search_txt, start_date, end_date);
        });
    }

    colorTable(rows, "#063688", "#004FD6");
});

function search(dropdown, rows, search_txt, start_date, end_date){
    let header;
    let type;

    switch(dropdown.value){
        //categories
        case "Name":
            header = "name";
            type = "string";
            break;
        case "Type":
            header = "type";
            type = "string";
            break;
        //transactions
        case "Category":
            header = "category_name";
            type = "string";
            break;
        case "Currency":
            header = "currency";
            type = "string";
            break;
        case "Ammount":
            header = "ammount";
            type = "number";
            break;
        case "Date":
            header = "date";
            type = "date";
            break;
        default:
            if(start_date == null && end_date == null){
                return;
            }
            header = "date";
            type = "date";
            break;
    }
    
    if(location.pathname == "/categories"){
        search_by_type(header, rows, search_txt, type);
    }
    else{
        search_by_type_date(header, rows, search_txt, type, start_date, end_date);
    }
}
