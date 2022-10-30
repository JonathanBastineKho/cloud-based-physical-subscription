// Drawer function
function switchDrawer(btn){
    if (btn == "open"){
        console.log("opened");
        $("#open").addClass("hidden");
        $("#close").removeClass("hidden");
    } else {
        $("#open").removeClass("hidden");
        $("#close").addClass("hidden");
    }
}
