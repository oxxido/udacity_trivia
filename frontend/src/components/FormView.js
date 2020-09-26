import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/FormView.css';

class FormView extends Component {
  constructor(props){
    super();
    this.state = {
      question: "",
      answer: "",
      difficulty: 1,
      category: 1,
      categories: {},
      showSuccess: false,
    }
  }

  componentDidMount(){
    $.ajax({
      url: `/categories`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({ categories: result.categories })
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again')
        return;
      }
    })
  }


  submitQuestion = (event) => {
    event.preventDefault();
    $.ajax({
      url: '/questions', //TODO: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        question: this.state.question,
        answer: this.state.answer,
        difficulty: this.state.difficulty,
        category: this.state.category
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        document.getElementById("add-question-form").reset();
        this.setState({ showSuccess: true });
        return;
      },
      error: (error) => {
        alert('Unable to add question. Please try your request again')
        return;
      }
    })
  }

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value})
  }

  hideAlert = () => {
    // this.setState({visibleAnswer: !this.state.visibleAnswer});
    this.setState({ showSuccess: false })
  }

  render() {
    return (
      <div id="add-form">
        <h2>Add a New Trivia Question</h2>
        <div className="content">
        <div className="pure-alert"
          style={this.state.showSuccess ? {} : { display: 'none' }}
          onClick={() => this.hideAlert()} >
            <label>Trivia Question Succesfully Added</label>
        </div>
        <form className="pure-form pure-form-aligned" id="add-question-form" onSubmit={this.submitQuestion}>
          <fieldset>
            <div className="pure-control-group">
              <label htmlFor="question">Question</label>
              <input type="text" name="question" className="pure-input-2-3"
                placeholder="Add your question"
                onChange={this.handleChange} required="required"/>
            </div>
            <div className="pure-control-group">
              <label htmlFor="answer">Answer</label>
              <input type="text" name="answer" 
                placeholder="Add your answer" 
                onChange={this.handleChange} required="required"/>
            </div>
            <div className="pure-control-group">
              <label htmlFor="difficulty">Difficulty</label>
              <select name="difficulty" onChange={this.handleChange} className="pad_3">
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
              </select>
            </div>
            <div className="pure-control-group">
              <label htmlFor="category">Category</label>
              <select name="category" onChange={this.handleChange} className="pad_3">
                {Object.keys(this.state.categories).map(id => {
                  return (
                    <option key={id} value={id}>{this.state.categories[id]}</option>
                  )
                })}
              </select>
            </div>
            <div className="pure-controls">
              <button type="submit" className="pure-button pure-button-primary">Submit</button>
            </div>
          </fieldset>
        </form>
        </div>
      </div>
    );
  }
}

export default FormView;
