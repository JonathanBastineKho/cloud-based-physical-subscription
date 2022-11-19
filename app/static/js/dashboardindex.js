async function loadChart(){
   var requestData = await fetch("/dashboard_content/dashboardindexgraph")
   .then(function(res){
      return res.json()
   });
   var processedLabels = [];
   var processedData = [];

   for(var i=0; i<requestData.length; i++){
      processedLabels.push(requestData[i]["transaction_date"])
      processedData.push(requestData[i]["value"]);
   }

   const labels = processedLabels;
   const data = {
      labels: labels,
      datasets: [
         {
         label: "My First dataset",
         backgroundColor: "#1C64F2",
         borderColor: "#1C64F2",
         data: processedData,
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