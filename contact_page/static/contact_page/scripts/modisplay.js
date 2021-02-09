import React from 'react';
import ReactDOM from 'react-dom';

class modisplay extends React.Component{
  constructor(props){
    super(props);
    this.state.inputs = true;
    this.state.fixed_elements = []
    this.state.input_elements = []
    this.state.hidden_elements = []
    this.state.determining_elements = []
    this.state.two_options = false
    for(var keys in props){
      const element = props[keys];
      if(element.category === 'fixed'){
        this.state.fixed_elements.push(element);
      }else if(element.category === 'input'){
        this.state.input_elements.push(element);
      }else if(element.category === 'hidden_elements'){
        this.state.hidden_elements.push(element);
      }else{
        if(element.category === 'determining'){
          this.state.determining_elements.push(element);
          if(element.value == true){
            this.state.two_options = false;
          }
        }
      }
    }
    console.log(this.state.fixed_elements);
    console.log(this.state.input_elements);
    console.log(this.state.hidden_elements);
    console.log(this.state.determining_elements);
  }
  render() {
    if(this.state.inputs === false || !this.state.two_options){
      return(
        <table>
            <thead>
              <tr>
                {this.state.fixed_elements.map(element => <td> {element.label} </td>)}
                {this.state.input_elements.map(element => <td> {element.label} </td>)}
                {this.state.determining_elements.map(element => <td> {element.label} </td>)}
              </tr>
            </thead>
            <tbody>
                {this.state.fixed_elements.map(element => <td> {element.value} </td>)}
                {this.state.input_elements.map(element => <td> {element.value} </td>)}
                {this.state.determining_elements.map(element => <td> {element.value} </td>)}
            </tbody>
            <tfoot>
              <tr><button onClick = {this.show_inputs}>Change details</button></tr>
            </tfoot>
        </table>
      );
    }else{
      return(
        <table>
            <thead>
              <tr>
                {this.state.fixed_elements.map(element => <td> {element.label} </td>)}
                {this.state.input_elements.map(element => <td> {element.label} </td>)}
                {this.state.determining_elements.map(element => <td> {element.label} </td>)}
              </tr>
            </thead>
            <tbody>
                {this.state.fixed_elements.map(element => <td> {element.value} </td>)}
                {this.state.fixed_elements.map(element => <td> <input name = {element.name} value = {element.value} placeholder = {element.placeholder} type = {element.type}/></td>)}
                {this.state.determining_elements.map(element => <td> {element.value} </td>)}
                {this.state.hidden_elements.map(element => <input name = {element.name} value = {element.value} />)}
            </tbody>
            <tfoot>
              <tr><input type = 'submit'/></tr>
            </tfoot>
        </table>
      );
    }
  }
  show_inputs = () => {
    this.setState((state) => ({
      inputs:true
    }));
  } 
}
