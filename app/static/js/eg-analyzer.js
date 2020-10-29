function FetchData(username) {
  return new Promise((resolve, reject) => {
    fetch("https://www.instagram.com/" + username + "/?__a=1")
      .then((account) => account.json())
      .then((accountJson) => {
        fetch(
          "https://www.instagram.com/graphql/query/?query_id=17888483320059182" +
            "&id=" +
            accountJson.graphql.user.id +
            "&first=" +
            50
        )
          .then((account_media) => account_media.json())
          .then((account_mediaJson) => {
            //Get Medias
            var Result = {};

            //Prepare data to return
            Result.Account = accountJson.graphql.user;
            Result.Medias =
              account_mediaJson.data.user.edge_owner_to_timeline_media;

            return resolve(Result);
          })
          .catch((error) => {
            console.error(error);
          });
      })
      .catch((error) => {
        window.history.back();
        console.error(error);
      });
  });
}

function analyze(result){
  document.getElementById("username").innerHTML = "@" + result.Account.username
        document.getElementById("username").setAttribute("href", "https://instagram.com/" + result.Account.username)
        document.getElementById("full_name").innerHTML = result.Account.full_name

        // Variablen für die Stats
        var followers = result.Account.edge_followed_by.count
        var following = result.Account.edge_follow.count
        var post_number = result.Account.edge_owner_to_timeline_media.count

        // CountUps für die Stats
        var followersCountup = new CountUp("followers", 0, followers, 0, 3, {
            separator: '.',
        })
        var followingCountup = new CountUp("following", 0, following, 0, 1.5, {
            separator: '.',
        })
        var post_numberCountup = new CountUp("post_number", 0, post_number, 0, 2, {
            separator: '.',
        })
        followersCountup.start()
        followingCountup.start()
        post_numberCountup.start()

        document.getElementById("profile_pic").setAttribute("src", result.Account.profile_pic_url_hd)


        var Likes = result.Medias.edges.map(x => {
            return x.node.edge_media_preview_like.count;
        });
        var Comments = result.Medias.edges.map(x => {
            return x.node.edge_media_to_comment.count;
        });

        // durchschnittliche Likes und Kommentare berechnen
        var AverageLikes =
            Math.floor(Likes.reduce((a, b) => a + b, 0) / result.Medias.edges.length);
        var AverageComments =
            Math.floor(Comments.reduce((a, b) => a + b, 0) / result.Medias.edges.length);

        // Engagement Rate berechnen
        var TotalEngagement =
            ((Likes.reduce((a, b) => a + b, 0) + Comments.reduce((a, b) => a + b, 0)) /
                result.Medias.edges.length /
                followers) * 100;

        // Engagement Rate auf zwei Nachkommastellen kürzen
        var engagementRate = TotalEngagement.toFixed(2)

        // CountUps für die Engagement Rate
        var eg_rateCountup = new CountUp("eg_rate_count", 0, engagementRate, 2, 2, {
            separator: '.',
            decimal: ',',
            suffix: '%',
        })
        eg_rateCountup.start()

        // Engagement Rate anzeigen
        document.getElementById("eg_rate_count").innerHTML = engagementRate + "%"

        // durchschnittliche Likes und Kommentare anzeigen
        document.getElementById("average_likes").innerHTML = "&#x2205; " + AverageLikes
        document.getElementById("average_comments").innerHTML = "&#x2205; " + AverageComments

        //console.log(result)

        var mentions = [];
        result.Account.edge_owner_to_timeline_media.edges.forEach(x => {
            x.node.edge_media_to_tagged_user.edges.forEach(y => {
                var mentioned_username = y.node.user.username
                mentions.push(mentioned_username)
            })
        })

        mentions = mentions.sort();
        var countedmentions = [];
        var current = null;
        var cnt = 0;
        for (var i = 0; i < mentions.length; i++) {
            if (mentions[i] !== current) {
                if (cnt > 0) {
                    countedmentions.push({
                        username: current,
                        count: cnt
                    });
                }
                current = mentions[i];
                cnt = 1;
            } else {
                cnt++;
            }
        }
        if (cnt > 0) {
            countedmentions.push({
                username: current.trim(),
                count: cnt
            });
        }
        countedmentions.sort((a, b) => (a.count < b.count ? 1 : -1));
        // nur 7 top mentions anzeigen
        //countedmentions.length = 7
        countedmentions.forEach(function (mention) {
            var tablerow = document.createElement("tr");
            var username = document.createElement("td");
            var count = document.createElement("td");

            username.innerHTML = "@" + mention.username;
            count.innerHTML = mention.count;
            tablerow.appendChild(username);
            tablerow.appendChild(count);
            document.getElementById("top_mentions_table").appendChild(tablerow)
            console.log(mention.username);
            console.log(mention.count);
        })
}
