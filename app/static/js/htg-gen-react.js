"use strict";

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

  render() {
    return (
      <div className={"search-input"}>
        <form>
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
        <i className={"fas fa-search"} />
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

function OutputContainer(props) {
    return (
      <div className={"output-container"}>
        <h4>Ausgewählte Hashtags:</h4>
        <p>{props.hashtags_output}</p>
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
        <OutputContainer hashtags_output={this.state.hashtags_output}/>
      </div>
    );
  }
}

const domContainer = document.querySelector("#htg-gen-react");
ReactDOM.render(React.createElement(HashtagGenerator), domContainer);
