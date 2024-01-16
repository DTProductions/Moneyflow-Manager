/**
 * matches values in search_txt with data inside rows
 * hides rows where values don't match
 * NOTE 1: each row needs to have an "rd" with a checkbox with the "checkB" class inside it
 * NOTE 2: each "rd" should have its header tag set
 * (check boxes are automatically closed when values don't match)
 * @param {string} header 
 * @param {NodeListOf<HTMLTableRowElement>} rows
 * @param {HTMLInputElement}  search_txt
 */
function search_by_text(header, rows, search_txt){
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

/**
 * Sends an array of ids to url with the "id" key in JSON
 * NOTE: check boxes names should contain the reffered id
 * @param {NodeListOf<HTMLInputElement>} check_boxes 
 * @param {string} id 
 * @param {string} method 
 * @param {string} url
 */
async function remove(check_boxes, url, id="id", method="POST"){
    let selected_rows = [];
    for(let i = 0; i < check_boxes.length; i++){
        if(check_boxes[i].checked == true){
            selected_rows.push(check_boxes[i].name);
        }
    }

    json_params = JSON.stringify({id : selected_rows});

    const response = await fetch(url ,{
        method: method,
        headers:{
            "Content-Type": "application/json"
        },
        body: json_params
    });

    let json = await response.json();
    if(json["status"] == "fail"){
        alert(json["message"]);
    }
    else{
        location.reload();
    }
}

/**
 * Sends a form to the specified url and redirects the user if return is sucessfull
 * @param {HTMLFormElement} form 
 * @param {string} url 
 * @param {string} redirect_url 
 * @param {string} method 
 */
async function add_register(form, url, redirect_url, method="POST"){
    const form_data = new FormData(form);
    let response = await fetch(url, {
        method: method,
        body: form_data
    });

    let json = await response.json();
    if(json["status"] == "fail"){
        alert(json["message"]);
    }
    else{
        location.replace(redirect_url);
    }
}
