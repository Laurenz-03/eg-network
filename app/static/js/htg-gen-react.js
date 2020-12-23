class SearchInput extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      keywords: "",
    };
  }

  handleKeywordsChange = (event) => {
    this.setState({
      keywords: event.target.value,
    });
  };

  handleSubmit = (event) => {
    event.preventDefault();
  };

  render() {
    return (
      <div className={"search-input"}>
        <form onSubmit={this.handleSubmit}>
          <input
            type="text"
            value={this.state.keywords}
            onChange={this.handleKeywordsChange}
          />
        </form>
      </div>
    );
  }
}

class SearchButton extends React.Component {
  render() {
    return (
      <button className={"search-button"}>
        <i className={"material-icons"}>search</i>
      </button>
    );
  }
}

class SearchField extends React.Component {
  render() {
    return (
      <div className={"search-field"}>
        <SearchInput />
        <SearchButton />
      </div>
    );
  }
}

function ActionButtons() {
  return (
    <div className={"action-buttons"}>
      <div className={"icon-buttons"}>
        <button>
          <i className={"material-icons"}>delete_outline</i>
        </button>

        <button>
          <i className={"material-icons"}>shuffle</i>
        </button>

        <button>
          <i className={"material-icons"}>sort</i>
        </button>
      </div>

      <button className={"copy-button"}>Kopieren</button>
    </div>
  );
}

function OutputContainer(props) {
  return (
    <div className={"output-container"}>
      <div className={"htg-count"}>
        <h4>Ausgewählte Hashtags:</h4>
        <p>30/30</p>
      </div>
      <p>{props.hashtags_output}</p>
      <ActionButtons />
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
  handleExpandedButtonClick = () => {
    this.setState({
      expanded: !this.state.expanded,
    });
  };
  handleSelectButtonClick = () => {
    this.setState({
      selected: !this.state.selected,
    });
  };
  render() {
    let selectButton;
    if (this.state.selected === false) {
      selectButton = <button className={"htg-checkbox"}></button>;
    } else {
      selectButton = <button className={"htg-checkbox selected"}></button>;
    }

    if (this.state.expanded === false) {
      return (
        <div className={"hashtag-info"}>
          <div className={"main-info"}>
            <div className={"left-area"}>
              {selectButton}
              <p>{this.props.htg["htg"]}</p>
            </div>
            <div className={"right-area"}>
              <p>{this.props.htg["posts_count"]} Beiträge</p>
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
            <div className={"left-area"}>
              <div className={"htg-checkbox"}></div>
              <p>{this.props.htg["htg"]}</p>
            </div>
            <div className={"right-area"}>
              <p>{this.props.htg["posts_count"]} Beiträge</p>
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
            <div className={"more-info-element"}>
              <p>Competition Score:</p>
              <div className={"info-container"}>
                <div className={"outer-info-bar"}>
                  <div
                    className={"inner-info-bar"}
                    style={{ width: this.props.htg["comp_score"] + "%" }}
                  ></div>
                </div>
                <p>{this.props.htg["comp_score"]}% (high)</p>
              </div>
            </div>

            <div className={"more-info-element"}>
              <p>Avg. Likes:</p>
              <div className={"info-container"}>
                <div className={"outer-info-bar"}>
                  <div
                    className={"inner-info-bar"}
                    style={{ width: this.props.htg["avg_likes_score"] + "%" }}
                  ></div>
                </div>
                <p>{this.props.htg["avg_likes"]} (medium)</p>
              </div>
            </div>

            <div className={"more-info-element"}>
              <p>Post Frequency:</p>
              <div className={"info-container"}>
                <div className={"outer-info-bar"}>
                  <div
                    className={"inner-info-bar"}
                    style={{ width: this.props.htg["post_freq_score"] + "%" }}
                  ></div>
                </div>
                <p>{this.props.htg["post_freq"]}/h (high)</p>
              </div>
            </div>

            <div className={"more-info-element"}>
              <p>Potential Reach:</p>
              <div className={"info-container"}>
                <div className={"outer-info-bar"}>
                  <div
                    className={"inner-info-bar"}
                    style={{ width: this.props.htg["pot_reach"] + "%" }}
                  ></div>
                </div>
                <p>{this.props.htg["pot_reach"]}% (low)</p>
              </div>
            </div>
          </div>
        </div>
      );
    }
  }
}

function FetchedHashtags() {
  var htgs = [
    {
      htg: "#erfolg",
      posts_count: "1.6m",
      comp_score: 85,
      avg_likes: 380,
      avg_likes_score: 60,
      post_freq: 65,
      post_freq_score: 65,
      pot_reach: 35,
    },
    {
      htg: "#mindset",
      posts_count: "27m",
      comp_score: 85,
      avg_likes: 380,
      avg_likes_score: 60,
      post_freq: 65,
      post_freq_score: 65,
      pot_reach: 35,
    },
    {
      htg: "#erfolgsmindset",
      posts_count: "180k",
      comp_score: 50,
      avg_likes: 150,
      avg_likes_score: 40,
      post_freq: 35,
      post_freq_score: 25,
      pot_reach: 55,
    },
    {
      htg: "#success",
      posts_count: "1.6m",
      comp_score: 85,
      avg_likes: 380,
      avg_likes_score: 60,
      post_freq: 65,
      post_freq_score: 65,
      pot_reach: 35,
    },
    //{ htg: "#mindset", posts_count: "27m" },
    //{ htg: "#erfolgsmindset", posts_count: "180k" },
    //{ htg: "#success", posts_count: "1.6m" },
    //{ htg: "#successmindset", posts_count: "27m" },
    //{ htg: "#erfolgsmensch", posts_count: "180k" },
    //{ htg: "#unternehmer", posts_count: "1.6m" },
    //{ htg: "#fokus", posts_count: "27m" },
    //{ htg: "#vision", posts_count: "180k" },
    //{ htg: "#wachstum", posts_count: "1.6m" },
    //{ htg: "#zeitfürmich", posts_count: "27m" },
    //{ htg: "#keineausreden", posts_count: "180k" },
  ];
  return (
    <div className={"fetched-hashtags-container"}>
      {htgs.map((htg) => (
        <HashtagInfo key={htg["htg"]} htg={htg} />
      ))}
    </div>
  );
}

class HashtagGenerator extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      hashtags_output:
        "#fokus #vision #motivation #lebensfreude #unternehmer #disziplin #keineausreden #derwegistdasziel #zeitfürmich #weiterbildung #börse #wachstum #erfolgsmensch #wertschätzung #wille #kopfhoch #glaubenssätze #mehrwert #träumewerdenwahr #chancengeber #erfolgreichillustrator #erfolgssprüche #inspirierend #weiterkommen #erfolgistplanbar #erfolgcompany #entwickeln #erfolgreichleben #erfolgmagazin #erfolgsmaster",
    };
  }

  render() {
    return (
      <div>
        <SearchField />
        <OutputContainer hashtags_output={this.state.hashtags_output} />
        <FetchedHashtags />
      </div>
    );
  }
}

const domContainer = document.querySelector("#htg-gen-react");
ReactDOM.render(React.createElement(HashtagGenerator), domContainer);
