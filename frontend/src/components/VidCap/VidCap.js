import React, { Component } from "react";
import './VidCap.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';
import TextTransition, { presets } from "react-text-transition";
import ReactPlayer from 'react-player'

class VidCap extends Component {

  constructor(props) {
    super(props);
    this.state = {result: "", file: ""};
  }

  onChangeFile(event) {
      event.stopPropagation();
      event.preventDefault();
      var file = event.target.files[0];
      console.log(file);
      this.setState({result: "Generating Caption!"})

      var formData = new FormData();
      formData.append("file", file);
      this.setState({file: URL.createObjectURL(file)})
      formData.append("beam_index", "3");
      axios.post('http://localhost:5000/success', formData, {
        headers: {
        'Content-Type': 'multipart/form-data'
      }})
        .then(res => {
            console.log({res});
            this.setState({result: res.data.beam_search_3.caption})
        }).catch(err => {
            console.error({err});
        });
  }
    
  render() {
    return (
        <div className="background">
          <div className="waveWrapper waveAnimation">
              <div className="waveWrapperInner bgTop">
                <div className="wave waveTop" style={{backgroundImage: `url('http://front-end-noobs.com/jecko/img/wave-top.png')`}}></div>
              </div>
              <div className="waveWrapperInner bgMiddle">
                <div className="wave waveMiddle" style={{backgroundImage: `url('http://front-end-noobs.com/jecko/img/wave-mid.png')`}}></div>
              </div>
              <div className="waveWrapperInner bgBottom">
              <div className="wave waveBottom" style={{backgroundImage: `url('http://front-end-noobs.com/jecko/img/wave-bot.png')`}}></div>
              </div>
            </div>
          <div>
          <div className="audio-class">
            <div className="wrapper">
              <div className="main">
                <div className="card-div">
                  <h1 className="label">{"Video Summarization"}</h1>
                  <input id="myInput"
                    style={{display: "none"}}
                    type="file"
                    ref={(ref) => this.upload = ref}
                    style={{display: 'none'}}
                    onChange={this.onChangeFile.bind(this)}
                    />
                    <button className="button" onClick={()=>{this.upload.click();this.setState({result: ""})}}>Upload a video (.mp4, .avi)</button>
                    <ReactPlayer
                      className='react-player video'
                      url= {this.state.file}
                      width='30%'
                      height='30%'
                      controls = {true}
                    />
                    <TextTransition className="results"
                      text={ this.state.result }
                      springConfig={ presets.wobbly }
                    />               
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
    )
  }
}

export default VidCap;