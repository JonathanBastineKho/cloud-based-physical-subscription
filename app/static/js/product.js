async function subscribe(event, doorID){
    event.preventDefault();

    var form = new FormData(event.target);
    form.append("door_id", Number(doorID));
    for (var pair of form.entries()){
        console.log(pair[0] + ' ' + pair[1]);
    }
    fetch("/subscribe",{
        method : "POST",
        body : form
    }).then(function(res){
        return res.text();
    }).then(function(url){
        window.open(url,
            "test",
            "width = 425, height = 812, top = 100, left = 200, location = no")
    });
}