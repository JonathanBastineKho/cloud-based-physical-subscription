var drawer;
// Drawer function
$(document).ready(function(){
    // requestDashboardPage("dashboardindex");
    const aside = document.getElementById("sidebar");

    const options = {
        backdrop: true,
        bodyScrolling: false,
        edge: false,
        edgeOffset: '',
        backdropClasses: 'bg-gray-900 bg-opacity-50 dark:bg-opacity-80 fixed inset-0 z-20',
        onHide: () => {
            $("#open").removeClass("hidden");
            $("#close").addClass("hidden");
        },
        onShow: () => {
            $("#open").addClass("hidden");
            $("#close").removeClass("hidden");
        },
    };
    drawer = new Drawer(aside, options);
});

function toggleDrawer(){
    drawer.toggle();
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

