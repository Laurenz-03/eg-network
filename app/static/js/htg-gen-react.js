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



function HashtagInfo() {
  return (
    <div className={"hashtag-info"}>
    </div>
  );
}

function FetchedHashtags() {

  var htgs = ["test", "test", "test"]
  htgs.forEach(element => {
    return (
      <div className={"fetched-hashtags-container"}>
        <HashtagInfo/>
      </div>
    );
    
  });

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
        <FetchedHashtags/>
      </div>
    );
  }
}

const domContainer = document.querySelector("#htg-gen-react");
ReactDOM.render(React.createElement(HashtagGenerator), domContainer);
