document.addEventListener("DOMContentLoaded", ()=>{
    initialize_page();
});

async function initialize_page(){
    let income_canvas = document.getElementById("income_canvas");
    let expenses_canvas = document.getElementById("expenses_canvas");
    let total_expenses = document.getElementById("total_expenses");
    let total_income = document.getElementById("total_income");
    let total = document.getElementById("total");
    let dropdown = document.getElementById("view_dropdown");

    let exchange_rate_impact = document.getElementById("exchange_rate_impact");
    
    if(dropdown.value == ""){
        total.innerHTML = "0.00";
        total_expenses.innerHTML = "0.00";
        total_income.innerHTML = "0.00";
        document.getElementById("total_str").style.visibility = "visible";
        return;
    }

    let charts = await initialize_display(income_canvas, expenses_canvas, total, total_expenses, total_income, exchange_rate_impact, dropdown);
    dropdown.addEventListener("change", ()=>{
        update_chart(charts[0], charts[1], total, total_expenses, total_income, exchange_rate_impact, dropdown);
    });
}

async function update_chart(income_chart, expenses_chart, total, total_expenses, total_income, exchange_rate_impact ,dropdown){
    let overview_data = await fetch_overview(dropdown);
    income_chart.data.labels = overview_data["income_labels"];
    income_chart.data.datasets[0].data = overview_data["income_data"];
    income_chart.update();

    expenses_chart.data.labels = overview_data["expenses_labels"];
    expenses_chart.data.datasets[0].data = overview_data["expenses_data"];
    expenses_chart.update();

    set_totals(total, total_expenses, total_income, exchange_rate_impact, overview_data);
}

async function fetch_overview(dropdown){
    json_params = JSON.stringify({selected_currency : dropdown.value});

    const response = await fetch("/overview" ,{
        method: "POST",
        headers:{
            "Content-Type": "application/json"
        },
        body: json_params
    });

    return await response.json();
}

async function initialize_display(income_canvas, expenses_canvas, total, total_expenses, total_income, exchange_rate_impact, dropdown){
    let overview_data = await fetch_overview(dropdown);

    let chart_colors = [
        '#004FD6',
        '#A80093',
        '#00BF63',
        '#36A2EB',
        '#F86800',
        '#063688',
        '#5E17EB',
        '#FF3131'
    ]

    let income_chart = new_doughnut_chart(income_canvas, overview_data["income_labels"], overview_data["income_data"], "Income", chart_colors);
    let expenses_chart = new_doughnut_chart(expenses_canvas, overview_data["expenses_labels"], overview_data["expenses_data"], "Expenses", chart_colors);

    set_totals(total, total_expenses, total_income, exchange_rate_impact, overview_data);

    document.getElementById("total_str").style.visibility = "visible";

    return [income_chart, expenses_chart];
}

function set_totals(total, total_expenses, total_income, exchange_rate_impact, overview_data){
    total.innerHTML = overview_data["total"];
    total_expenses.innerHTML = overview_data["total_expenses"];
    total_income.innerHTML = overview_data["total_income"];
    if (overview_data.hasOwnProperty("exchange_rate_impact")){
        document.querySelector(".exchange-rate-impact-style").style.display = "block";
        exchange_rate_impact.innerHTML = overview_data["exchange_rate_impact"];
    }
    else{
        document.querySelector(".exchange-rate-impact-style").style.display = "none";
    }
}

function new_doughnut_chart(canvas, labels, dataset_data, dataset_label, colors){
    let chart_data = {
        labels: labels,
        datasets: [{
        label: dataset_label,
        data: dataset_data,
        backgroundColor: colors,
        hoverOffset: 4
        }]
    };

    return ret_chart = new Chart(canvas, {
        type : "doughnut",
        data : chart_data,
        options : {
            maintainAspectRatio: false
        }
    });
}
