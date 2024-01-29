/**
 * fills an empty form and submits it based on selected check boxes inside table
 * (id represents the data stored inside the checkbox's name, fields are the other form fields
 * stored inside the td as their innerHTML)
 * @param {NodeListOf<HTMLTableRowElement>} rows 
 * @param {NodeListOf<HTMLTableRowElement>} check_boxes 
 * @param {HTMLFormElement} form 
 * @param {Array} fields 
 * @param {string} id 
 * @returns 
 */
function sendForm(rows, check_boxes, form, fields, id){
    let chk_count = 0;
    for(let i = 0; i < rows.length && chk_count < 2; i++){
        if(check_boxes[i].checked){

            for(let j = 0; j < fields.length; j++){
                let field_value = rows[i].querySelector("[headers='" + fields[j] +"']").innerHTML;
                if(fields[j] == "amount" || fields[j] == "source_amount" || fields[j] == "destination_amount"){
                    field_value = field_value.replace(",", "");
                }
                form.querySelector("[name='" + fields[j] + "']").value = field_value;
            }
            form.querySelector("[name='" + id + "']").value = check_boxes[i].name;
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

/**
 * Color table rows with alternating colors
 * @param {NodeListOf<HTMLTableRowElement>} rows 
 * @param {string} color1 
 * @param {string} color2 
 */
function colorTable(rows, color1, color2){
    for(let i = 0; i < rows.length; i++){
        if(i % 2 == 0){
            rows[i].style.backgroundColor = color1;
        }
        else{
            rows[i].style.backgroundColor = color2;
        }
    }
}