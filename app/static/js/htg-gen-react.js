// Fetch Functions:
async function fetchReq(keyword) {
  const req = await fetch(
    `https://www.instagram.com/web/search/topsearch/?context=blended&count=10&query=%23${keyword}&rank_token=5&include_reel=true`
  );
  const res = await req.json();
  const hashtag = res.hashtags
    .map(hash => ({
      htg: hash.hashtag.name,
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
    console.log(hashtag);
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
        <SearchInput fetchHashtags={this.props.fetchHashtags} handleKeywordsChange={this.props.handleKeywordsChange} keyword={this.props.keyword}/>
        <SearchButton />
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
  let output;
  if(props.selected_htgs.length == 0){
    output = <p>Hier werden deine ausgewählten Hashtags angezeigt.</p>
  }else{
    output = <p>{props.selected_htgs.join(" ")}</p>
  }
  return (
    <div className={"output-container"}>
      <div className={"htg-count"}>
        <h4>Ausgewählte Hashtags:</h4>
        <p>{props.selected_htgs.length}/30</p>
      </div>
      {output}
      <ActionButtons deleteAll={props.deleteAll}/>
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
  componentDidMount(){
    if(this.props.selected_htgs.includes(this.props.htg["htg"])){
      console.log("moin")
      this.setState({
        selected: true,
      });
    }else{
      console.log("asfe")
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
    if (this.state.selected == false){
      this.props.selectHashtag(this.props.htg["htg"]);
    }else{
      this.props.unselectHashtag(this.props.htg["htg"])
    }
    this.setState({
      selected: !this.state.selected,
    });
  };
  render() {
    let selectButton;
    if (this.state.selected === false) {
      selectButton = <button onClick={this.handleSelectButtonClick} className={"htg-checkbox"}></button>;
    } else {
      selectButton = <button onClick={this.handleSelectButtonClick} className={"htg-checkbox selected"}>
         <i className={"fas fa-check"}></i>
      </button>;
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
            <div className={"left-area"}>
              <div className={"htg-checkbox"}></div>
              <p>{this.props.htg["htg"]}</p>
            </div>
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

function FetchedHashtags(props) {
  
  return (
    <div className={"fetched-hashtags-container"}>
      {props.htgs.map(htg => <HashtagInfo key={htg["htg"]} htg={htg} selected_htgs={props.selected_htgs} selectHashtag={props.selectHashtag} unselectHashtag={props.unselectHashtag}/>)
      }
    </div>
  );
}

class HashtagGenerator extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      keyword: "",
      htgs: [
      ],
      selected_htgs: []
    };
  }

  fetchHashtags = () => {
    fetchReq(this.state.keyword).then(result => (this.setState({htgs: result})));
  }

  handleKeywordsChange = (event) => {
    this.setState({
      keyword: event.target.value,
    });
  };

  selectHashtag = (htg) => {
    this.setState(state => {
      const list = this.state.selected_htgs.push(htg);
      return{
        list
      }
    })
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
  unselectHashtag = (htg) => {
    this.setState(state => {
      const list = this.removeItemAll(this.state.selected_htgs, htg);
      return{
        list
      }
    })
  }
  deleteAll = () => {
    this.setState({
      selected_htgs: []
    })
    window.location.reload();
  }

  render() {
    return (
      <div>
        <SearchField fetchHashtags={this.fetchHashtags} handleKeywordsChange={this.handleKeywordsChange} keyword={this.state.keyword}/>
        <OutputContainer selected_htgs={this.state.selected_htgs} deleteAll={this.deleteAll} />
        <FetchedHashtags htgs={this.state.htgs} selected_htgs={this.state.selected_htgs} keyword={this.state.keyword} selectHashtag={this.selectHashtag} unselectHashtag={this.unselectHashtag}/>
      </div>
    );
  }
}

const domContainer = document.querySelector("#htg-gen-react");
ReactDOM.render(React.createElement(HashtagGenerator), domContainer);
