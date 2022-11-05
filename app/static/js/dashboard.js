// Drawer function
// $(document).ready(function(){
//     requestDashboardPage("dashboard");
// });

function switchDrawer(btn){
    if (btn == "open"){
        $("#open").addClass("hidden");
        $("#close").removeClass("hidden");
    } else {
        $("#open").removeClass("hidden");
        $("#close").addClass("hidden");
    }
}

function requestDashboardPage(dashboardPage){
    fetch(`/dashboard_content/${dashboardPage}`)
    .then(function (response){
        return response.text();
    }).then(function(html){
        // change content html
        $("#main-content").empty();
        $("#main-content").append(html);
    });
}

