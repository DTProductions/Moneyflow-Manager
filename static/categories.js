document.addEventListener("DOMContentLoaded", (Event) =>{
    let data = document.getElementById("data").querySelectorAll("tr");
    for(let i = 0; i < data.length; i++){
        if(i % 2 == 0){
            data[i].style.backgroundColor = "#063688";
        }
        else{
            data[i].style.backgroundColor = "#004FD6";
        }
    }
});