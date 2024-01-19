/**
 * matches values in search_txt with data inside rows
 * hides rows where values don't match
 * NOTE 1: each row needs to have an "rd" with a checkbox with the "checkB" class inside it
 * NOTE 2: each "rd" should have its header tag set
 * (check boxes are automatically closed when values don't match)
 * @param {string} header 
 * @param {NodeListOf<HTMLTableRowElement>} rows
 * @param {HTMLInputElement}  search_txt
 * @param {string} type 
 */
function search_by_type(header, rows, search_txt, type){
    for(let i = 0; i < rows.length; i++){
        let data = rows[i].querySelector("[headers='" + header + "']").innerHTML;
        let check_box = rows[i].querySelector(".checkB");

        if(!data_matches(data, type, search_txt.value)){
            hide_row(rows[i], check_box);
        }
        else{
            display_row(rows[i], check_box);
        }
    }
}

/**
 * matches values in rows with search_txt value and make sure they are between the selected dates
 * (which are ignored if no date is selected)
 * @param {string} header 
 * @param {NodeListOf<HTMLTableRowElement>} rows 
 * @param {HTMLInputElement} search_txt 
 * @param {string} type 
 * @param {HTMLInputElement} start_date 
 * @param {HTMLInputElement} end_date 
 */
function search_by_type_date(header, rows, search_txt, type, start_date, end_date){
    for(let i = 0; i < rows.length; i++){
        let data = rows[i].querySelector("[headers='" + header + "']").innerHTML;
        let date = get_db_date_time(rows[i].querySelector("[headers='date']").innerHTML);
        let check_box = rows[i].querySelector(".checkB");

        if(!(data_matches(data, type, search_txt.value) && date_matches(date, new Date(start_date.value).getTime(), new Date(end_date.value).getTime()))){
            hide_row(rows[i], check_box);
        }
        else{
            display_row(rows[i], check_box);
        }
    }
}

function get_db_date_time(date_str){
    date_str = date_str.split("/").reverse();
    let new_str = date_str[0] + "-" + date_str[1] + "-" + date_str[2];
    return new Date(new_str).getTime();
}

/**
 * @param {string} data 
 * @param {string} type 
 * @param {string} search_key 
 * @returns bool
 */
function data_matches(data, type, search_key){
    switch(type){
        case "number":
            return data.toLowerCase().startsWith(search_key.toLowerCase());
        case "string":
            return data.toLowerCase().includes(search_key.toLowerCase());
        case "date":
            return true;
        }
    return false;
}

/**
 * Check if date is between the start and end dates
 * @param {number} date 
 * @param {number} start_date 
 * @param {number} end_date 
 * @returns bool
 */
function date_matches(date, start_date, end_date){
    if(isNaN(start_date) && isNaN(end_date)){
        return true;
    }
    if(isNaN(start_date)){
        return date <= end_date;
    }
    if(isNaN(end_date)){
        return date >= start_date;
    }
    if(end_date < start_date){
        return false;
    }
    return start_date <= date && date <= end_date;
}

function hide_row(row, check_box){
    row.style.display = "none";
    check_box.disabled = true;
    check_box.checked = false;
}

function display_row(row, check_box){
    row.style.display = "table-row";
    check_box.disabled = false;
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
