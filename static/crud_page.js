document.addEventListener("DOMContentLoaded", (Event) =>{

    //get elements from DOM
    let rows = document.getElementById("data").querySelectorAll("tr");
    let search_txt = document.getElementById("search-txt");
    let field_dropdown = document.getElementById("field");
    let check_boxes = document.getElementById("data").querySelectorAll(".checkB");
    let form = document.getElementById("update_form");

    let start_date = document.getElementById("start_date");
    let end_date = document.getElementById("end_date");

    set_search_events(field_dropdown, rows, search_txt, start_date, end_date);

    //set update and delete events
    switch(location.pathname){
        case "/categories":
            set_update_button_event(rows, check_boxes, form, ["name","type"], "id");
            set_remove_button_event(check_boxes, "/categories/remove");
            break;
        case "/transactions":
            set_update_button_event(rows, check_boxes, form, ["date", "amount", "currency", "category_name"], "id");
            set_remove_button_event(check_boxes, "/transactions/remove");
            set_date_listening_events(field_dropdown, rows, search_txt, start_date, end_date);   
            break;
        case "/exchanges":
            set_update_button_event(rows, check_boxes, form, ["date", "source_currency", "source_amount", "destination_currency", "destination_amount"], "id");
            set_remove_button_event(check_boxes, "/exchanges/remove");
            set_date_listening_events(field_dropdown, rows, search_txt, start_date, end_date);   
    }

    colorTable(rows, "#063688", "#004FD6");
});

function set_update_button_event(rows, check_boxes, form, fields, id){
    document.querySelector("#update").addEventListener("click", () =>{
        sendForm(rows, check_boxes, form, fields, id);
    });
}

function set_date_listening_events(field_dropdown, rows, search_txt, start_date, end_date){
    start_date.addEventListener("change", () =>{
        search(field_dropdown, rows, search_txt, start_date, end_date);
    });
    end_date.addEventListener("change", () =>{
        search(field_dropdown, rows, search_txt, start_date, end_date);
    });
}

function set_remove_button_event(check_boxes, redirect_url){
    document.querySelector("#remove").addEventListener("click", ()=> {
        remove(check_boxes, redirect_url);
    });
}

function set_search_events(field_dropdown, rows, search_txt, start_date, end_date){
    search_txt.addEventListener("keyup", () =>{
        search(field_dropdown, rows, search_txt, start_date, end_date);
    });
    search_txt.addEventListener("search", () =>{
        search(field_dropdown, rows, search_txt, start_date, end_date);
    });
    field_dropdown.addEventListener("change", () =>{
        search(field_dropdown, rows, search_txt, start_date, end_date);
    });
}

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
        case "Amount":
            header = "amount";
            type = "number";
            break;
        case "Date":
            header = "date";
            type = "date";
            break;
        //exchanges
        case "Source Currency":
            header = "source_currency";
            type = "string";
            break;
        case "Source Amount":
            header = "source_amount";
            type = "number";
            break;
        case "Destination Currency":
            header = "destination_currency";
            type = "string";
            break;
        case "Destination Amount":
            header = "destination_amount";
            type = "number";
            break;
        default:
            if(start_date == null && end_date == null){
                return;
            }
            header = "date";
            type = "date_no_key";
            break;
    }
    
    if(location.pathname == "/categories"){
        search_by_type(header, rows, search_txt, type);
    }
    else{
        search_by_type_date(header, rows, search_txt, type, start_date, end_date);
    }
}
