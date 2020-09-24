import React, { Component } from 'react';
import '../stylesheets/Question.css';

class Question extends Component {
  constructor(){
    super();
    this.state = {
      visibleAnswer: false
    }
  }

  flipVisibility() {
    this.setState({visibleAnswer: !this.state.visibleAnswer});
  }

  render() {
    const { question, answer, category, difficulty } = this.props;
    return (
      <div className="Question-holder">
        <div className="question-icon">
          <img className="category" src={`${category}.svg`} alt="category"/>
        </div>
        <div className="Question">{question}</div>
        <div className="question-actions">
          <img
            src="delete.png"
            className="delete"
            onClick={() => this.props.questionAction('DELETE')}
            alt="Del"
            />
        </div>
        <div className="Question-status">
          
          <div className="difficulty">Difficulty: {difficulty}</div>
            
          
        </div>
        <div 
          className="answer-holder"
          style={{"display": this.state.visibleAnswer ? 'block' : 'none'}}>
             <strong>Answer:</strong> {answer}
        </div>
        <div className="show-answer"
            onClick={() => this.flipVisibility()}>
          {this.state.visibleAnswer ? 'Hide' : 'Show'} Answer
        </div>
      </div>
    );
  }
}

export default Question;
