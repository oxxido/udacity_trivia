import React, { Component } from 'react'

class Search extends Component {
  state = {
    query: '',
  }

  getInfo = (event) => {
    event.preventDefault();
    this.props.submitSearch(this.state.query)
  }

  handleInputChange = () => {
    this.setState({
      query: this.search.value
    })
  }

  render() {
    return (
      <form className="pure-form" onSubmit={this.getInfo}>
        <fieldset>
          <input
            placeholder="Search questions..."
            ref={input => this.search = input}
            onChange={this.handleInputChange}
          /> &nbsp;
          <button type="submit" class="pure-button pure-button-primary">
            Search
          </button>
        </fieldset>
      </form>
    )
  }
}

export default Search
