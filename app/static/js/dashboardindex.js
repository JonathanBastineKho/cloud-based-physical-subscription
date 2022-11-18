$(document).ready(function(){
  loadChart();
});

function loadChart(){
  const labels = ["January", "February", "March", "April", "May", "June"];
  const data = {
     labels: labels,
     datasets: [
        {
        label: "My First dataset",
        backgroundColor: "#1C64F2",
        borderColor: "#1C64F2",
        data: [0, 10, 5, 2, 20, 30, 45],
        },
     ],
  };
 
  const configLineChart = {
     type: "line",
     data,
     options: {
        maintainAspectRatio: false,
        plugins: {
           legend: {
              display: false,
              labels: {
                font: {
                  size: 40
                }
              }
           },
        },
        
     },
  };
 
  var chartLine = new Chart(
     document.getElementById("myChart"),
     configLineChart
  );
}