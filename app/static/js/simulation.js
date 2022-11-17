var gStatus = document.getElementById('status').innerHTML;
function checkDoor(status)
{
    var image = document.getElementById("doorIMG");
    status=String(status);
    gStatus=status
    if (status == "Open")
    {
        image.src="../static/img/openDoor.png";
        image.alt="Door Opened";
    }
    else if (status == "Close")
    {
        image.src="../static/img/closeDoor.png";
        image.alt="Door Closed";
    }
    else
    {
        image.src="";
        image.alt="Door Not Found";
    }
}

window.setInterval('refresh()', 30000); 
function refresh() {
    window .location.reload();
}

console.log(gStatus);
checkDoor(gStatus);