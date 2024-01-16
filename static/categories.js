let search_txt;
let field_dropdown;
let rows;
let check_boxes;

document.addEventListener("DOMContentLoaded", (Event) =>{
    rows = document.getElementById("data").querySelectorAll("tr");
    colorTable();

    search_txt = document.getElementById("search-txt");
    field_dropdown = document.getElementById("field");
    check_boxes = document.getElementById("data").querySelectorAll(".checkB");

    search_txt.addEventListener("keyup", search);
    search_txt.addEventListener("search", search);
    field_dropdown.addEventListener("change", search);

    document.querySelector("#update").addEventListener("click", sendForm);
    document.querySelector("#remove").addEventListener("click", ()=> {
        remove(check_boxes, "/categories/remove");
    });
});

function sendForm(){
    let chk_count = 0;
    let form = document.getElementById("update_form");
    for(let i = 0; i < rows.length && chk_count < 2; i++){
        if(check_boxes[i].checked){
            form.querySelector("[name='id']").value = check_boxes[i].name;
            form.querySelector("[name='name']").value = rows[i].querySelector("[headers='name']").innerHTML;
            form.querySelector("[name='category_type']").value = rows[i].querySelector("[headers='type']").innerHTML;
            chk_count++;
        }
    }

    if(chk_count == 0){
        alert("No rows selected");
        return;
    }
    else if(chk_count > 1){
        alert("Only one row may be selected");
        return;
    }
    form.submit();
}

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
