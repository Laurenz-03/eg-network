// Fetch Functions:
async function fetchReq(keyword) {
  const req = await fetch(
    `https://www.instagram.com/web/search/topsearch/?context=blended&count=10&query=%23${keyword}&rank_token=5&include_reel=true`,
    {
      mode: "no-cors",
    }
  );
  const res = await req.json();
  const hashtag = res.hashtags
    .map((hash) => ({
      htg: "#" + hash.hashtag.name,
      posts_count: hash.hashtag.search_result_subtitle,
      count: hash.hashtag.media_count,
      comp_score: 85,
      avg_likes: 380,
      avg_likes_score: 60,
      post_freq: 65,
      post_freq_score: 65,
      pot_reach: 35,
    }))
    .sort((a, b) => b.count - a.count);
  return hashtag;
}

class SearchInput extends React.Component {
  handleSubmit = (event) => {
    event.preventDefault();
    this.props.fetchHashtags();
  };

  render() {
    return (
      <div className={"search-input"}>
        <form onSubmit={this.handleSubmit}>
          <input
            type="text"
            value={this.props.keyword}
            onChange={this.props.handleKeywordsChange}
          />
        </form>
      </div>
    );
  }
}

class SearchButton extends React.Component {
  render() {
    return (
      <button onClick={this.props.fetchHashtags} className={"search-button"}>
        <i className={"material-icons"}>search</i>
      </button>
    );
  }
}

class SearchField extends React.Component {
  render() {
    return (
      <div className={"search-field"}>
        <SearchInput
          fetchHashtags={this.props.fetchHashtags}
          handleKeywordsChange={this.props.handleKeywordsChange}
          keyword={this.props.keyword}
        />
        <SearchButton fetchHashtags={this.props.fetchHashtags} />
      </div>
    );
  }
}

function ActionButtons(props) {
  return (
    <div className={"action-buttons"}>
      <div className={"icon-buttons"}>
        <button onClick={props.deleteAll}>
          <i className={"material-icons"}>delete_outline</i>
        </button>

        <button onClick={props.shuffleHashtags}>
          <i className={"material-icons"}>shuffle</i>
        </button>

        <button onClick={props.sortHashtags}>
          <i className={"material-icons"}>sort</i>
        </button>
      </div>

      <button onClick={props.copyHashtags} className={"copy-button"}>
        Kopieren
      </button>
    </div>
  );
}

function OutputContainer(props) {
  let output;
  if (props.selected_htgs.length == 0) {
    output = <p>Hier werden deine ausgewählten Hashtags angezeigt.</p>;
  } else {
    output = <p>{props.selected_htgs.join(" ")}</p>;
  }
  return (
    <div className={"output-container"}>
      <div className={"htg-count"}>
        <h4>Ausgewählte Hashtags:</h4>
        <p>{props.selected_htgs.length}/30</p>
      </div>
      {output}
      <ActionButtons
        deleteAll={props.deleteAll}
        sortHashtags={props.sortHashtags}
        shuffleHashtags={props.shuffleHashtags}
        deleteAll={props.deleteAll}
        copyHashtags={props.copyHashtags}
      />
    </div>
  );
}

class HashtagInfo extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      expanded: false,
      selected: false,
    };
  }
  componentDidMount() {
    if (this.props.selected_htgs.includes(this.props.htg["htg"])) {
      this.setState({
        selected: true,
      });
    } else {
      this.setState({
        selected: false,
      });
    }
  }
  removeItemAll(arr, value) {
    var i = 0;
    while (i < arr.length) {
      if (arr[i] === value) {
        arr.splice(i, 1);
      } else {
        ++i;
      }
    }
    return arr;
  }
  handleExpandedButtonClick = () => {
    this.setState({
      expanded: !this.state.expanded,
    });
  };
  handleSelectButtonClick = () => {
    if (this.state.selected == false) {
      this.props.selectHashtag(this.props.htg["htg"]);
    } else {
      this.props.unselectHashtag(this.props.htg["htg"]);
    }
    this.setState({
      selected: !this.state.selected,
    });
  };
  render() {
    let selectButton;
    if (this.state.selected === false) {
      selectButton = (
        <button onClick={this.handleSelectButtonClick} className={"left-area"}>
          <div className={"htg-checkbox"}></div>
          <p>{this.props.htg["htg"]}</p>
        </button>
      );
    } else {
      selectButton = (
        <button onClick={this.handleSelectButtonClick} className={"left-area"}>
          <div className={"htg-checkbox selected"}>
            <i className={"fas fa-check"}></i>
          </div>
          <p className={"blue-text"}>{this.props.htg["htg"]}</p>
        </button>
      );
    }

    if (this.state.expanded === false) {
      return (
        <div className={"hashtag-info"}>
          <div className={"main-info"}>
            {selectButton}
            <div className={"right-area"}>
              <p>{this.props.htg["posts_count"]}</p>
              <button
                className={"expand-button"}
                onClick={this.handleExpandedButtonClick}
              >
                <i className={"fas fa-chevron-down"}></i>
              </button>
            </div>
          </div>
        </div>
      );
    } else {
      return (
        <div className={"hashtag-info"}>
          <div className={"main-info"}>
            {selectButton}
            <div className={"right-area"}>
              <p>{this.props.htg["posts_count"]}</p>
              <button
                className={"expand-button"}
                onClick={this.handleExpandedButtonClick}
              >
                <i
                  className={"fas fa-chevron-down"}
                  style={{ transform: "rotate(180deg)", paddingTop: "2px" }}
                ></i>
              </button>
            </div>
          </div>
          <div className={"more-info"}>
            <div>
              <p>
                Erweiterte Informationen sind nur für Premium-Mitglieder
                verfügbar.
              </p>
            </div>
            <a href={"https://eg-network.co/mgb/premium"}>
              <button className={"blue-button"}>Jetzt kaufen</button>
            </a>
          </div>
        </div>
      );
    }
  }
}

function FetchedHashtags(props) {
  return (
    <div className={"fetched-hashtags-container"}>
      {props.htgs.map((htg) => (
        <HashtagInfo
          key={htg["htg"]}
          htg={htg}
          selected_htgs={props.selected_htgs}
          selectHashtag={props.selectHashtag}
          unselectHashtag={props.unselectHashtag}
        />
      ))}
    </div>
  );
}

class HashtagGenerator extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      keyword: "",
      htgs: [],
      selected_htgs: [],
    };
  }

  fetchHashtags = () => {
    var keywords = this.state.keyword.split(",");
    var hashtags = [];
    for (var i = 0; i < keywords.length; i++) {
      console.log(keywords[i]);
      fetchReq(keywords[i]).then((result) => {
        for (var j = 0; j < result.length; j++) {
          console.log(result[j]);
          hashtags.push(result[j]);
          this.setState({ htgs: hashtags });
        }
      });
    }
    console.log(hashtags);
    this.setState({ htgs: hashtags });
  };

  handleKeywordsChange = (event) => {
    this.setState({
      keyword: event.target.value,
    });
  };

  selectHashtag = (htg) => {
    this.setState((state) => {
      const list = this.state.selected_htgs.push(htg);
      return {
        list,
      };
    });
  };
  removeItemAll(arr, value) {
    var i = 0;
    while (i < arr.length) {
      if (arr[i] === value) {
        arr.splice(i, 1);
      } else {
        ++i;
      }
    }
    return arr;
  }
  unselectHashtag = (htg) => {
    this.setState((state) => {
      const list = this.removeItemAll(this.state.selected_htgs, htg);
      return {
        list,
      };
    });
  };
  deleteAll = () => {
    this.setState({
      selected_htgs: [],
    });
    window.location.reload();
  };
  sortHashtags = () => {
    this.setState({
      selected_htgs: this.state.selected_htgs.sort(),
    });
  };
  copyHashtags = () => {
    navigator.clipboard.writeText(this.state.selected_htgs.join(" "));
  };
  shuffleHashtags = () => {
    var array = this.state.selected_htgs;
    var currentIndex = array.length,
      temporaryValue,
      randomIndex;

    // While there remain elements to shuffle...
    while (0 !== currentIndex) {
      // Pick a remaining element...
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex -= 1;

      // And swap it with the current element.
      temporaryValue = array[currentIndex];
      array[currentIndex] = array[randomIndex];
      array[randomIndex] = temporaryValue;
    }

    this.setState({
      selected_htgs: array,
    });
  };

  render() {
    return (
      <div>
        <SearchField
          fetchHashtags={this.fetchHashtags}
          handleKeywordsChange={this.handleKeywordsChange}
          keyword={this.state.keyword}
        />
        <OutputContainer
          selected_htgs={this.state.selected_htgs}
          deleteAll={this.deleteAll}
          sortHashtags={this.sortHashtags}
          shuffleHashtags={this.shuffleHashtags}
          copyHashtags={this.copyHashtags}
        />
        <FetchedHashtags
          htgs={this.state.htgs}
          selected_htgs={this.state.selected_htgs}
          keyword={this.state.keyword}
          selectHashtag={this.selectHashtag}
          unselectHashtag={this.unselectHashtag}
        />
      </div>
    );
  }
}

const domContainer = document.querySelector("#htg-gen-react");
ReactDOM.render(React.createElement(HashtagGenerator), domContainer);
