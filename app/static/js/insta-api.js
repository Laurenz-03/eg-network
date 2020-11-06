
/*
function apiTest(){
    let headers = new Headers({
        "User-Agent"   : "Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)"
    });
    fetch('https://i.instagram.com/api/v1/users/516679301/info/', {
        headers: headers
    })
    .then(res => res.json())
    .then(data => console.log(data));
    
}

// Instagram API
function get_user_information_by_username(username){
    var user_info = {};
    var url = 'https://www.instagram.com/'+username+'/?__a=1';
    var data;
    fetch(url)
        .then(res => res.json())
        .then(data => {
            var userdata = data["graphql"]["user"];
            user_info["id"] = userdata["id"];
            user_info["username"] = username;
            user_info["followers"] = userdata["edge_followed_by"]["count"];
            user_info["following"] = userdata["edge_follow"]["count"];
            user_info["profile_pic_url"] = userdata["profile_pic_url"];
            console.log(user_info);
        })
}
*/