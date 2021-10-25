function get_token(){
    var token = "";
    $.ajax({
        url: "/api/token/", 
        type: "POST",
        async: false,
        data: {"username": "XcenaX", "password": "Dagad582#"},
        success: function(data){
            if(data["error"]){
                console.log(data["error"]);
            }else{
                console.log(data);
                token = data["token"];
            }
        }
    });
    return token;
}