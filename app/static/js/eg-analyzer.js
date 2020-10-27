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
        console.error(error);
      });
  });
}

