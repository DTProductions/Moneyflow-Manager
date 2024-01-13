let table_rows;
let search_txt;
let field_dropdown;
let rows;

document.addEventListener("DOMContentLoaded", (Event) =>{
    rows = document.getElementById("data").querySelectorAll("tr");
    colorTable();

    table_rows = document.getElementById("data");
    search_txt = document.getElementById("search-txt");
    field_dropdown = document.getElementById("field");

    search_txt.addEventListener("keyup", search);
    search_txt.addEventListener("search", search);
    field_dropdown.addEventListener("change", search);
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
            search_by_text("name");
            break;
        case "Type":
            search_by_text("type");
            break;
    }
}

function search_by_text(header){
    for(let i = 0; i < rows.length; i++){
        let data = rows[i].querySelector("[headers='" + header + "']");
        let check_box = rows[i].querySelector(".checkB");

        if(!data.innerHTML.toLowerCase().includes(search_txt.value.toLowerCase())){
            rows[i].style.display = "none";
            check_box.disabled = true;
            check_box.checked = false;
        }
        else{
            rows[i].style.display = "table-row";
            check_box.disabled = false;
        }
    }
}
