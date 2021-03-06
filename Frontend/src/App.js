import React, { useState } from "react";
import {RadioGroup, Radio} from "react-radio-group"
import axios from 'axios';
import "./App.css";
import { useSpring, animated } from "react-spring";

function App() {

  const [file_path, setFilePath] = useState("343");
  const [param, setParam] = useState(" ");


  const [registrationFormStatus, setRegistartionFormStatus] = useState(false);
  const loginProps = useSpring({ 
    left: registrationFormStatus ? -500 : 0, // Login form sliding positions
  });
  const registerProps = useSpring({
    left: registrationFormStatus ? 0 : 500, // Register form sliding positions 
  });

  const loginBtnProps = useSpring({
    borderBottom: registrationFormStatus 
      ? "solid 0px transparent"
      : "solid 2px #1059FF",  //Animate bottom border of login button
  });
  const registerBtnProps = useSpring({
    borderBottom: registrationFormStatus
      ? "solid 2px #1059FF"
      : "solid 0px transparent", //Animate bottom border of register button
  });

  function registerClicked() {
    setRegistartionFormStatus(true);
  }
  function loginClicked() {
    setRegistartionFormStatus(false);

  }



  function onPcaSend(){
    console.log(param)
    var file_path_str = file_path;
    file_path_str = file_path_str.replaceAll("\\", " ") 
    file_path_str = file_path_str.replace("fakepath","\\Users\\safee")
    console.log(file_path_str)

    const payload = {
      "file_path": file_path_str,
      "param": param
    }

    console.log(payload)

    axios.post('http://127.0.0.1:5000/pca', payload)
    .then((response) => {
      console.log(response);
      window.alert("file compressed! kindly check");
    }, (error) => {
      console.log(error);
    });
  }

  function onKmeansSend(){
    var file_path_str = file_path;
    file_path_str = file_path_str.replaceAll("\\", " ") 
    file_path_str = file_path_str.replace("fakepath","\\Users\\safee")
    console.log(file_path_str)

    const payload = {
      "file_path": file_path_str,
      "param": param
    }
    console.log(payload)
    axios.post('http://127.0.0.1:5000/kMeans', payload)
    .then((response) => {
      console.log(response);
      window.alert("file compressed! kindly check");
    }, (error) => {
      console.log(error);
    });
    window.alert("sending file, kindly wait");
  }


  return (
    <div>
  <div>
    <h1 style={registerBtnProps}>Hello</h1>
  </div>
  <div className="login-register-wrapper">
      <div className="nav-buttons">
        <animated.button
          onClick={loginClicked}
          id="loginBtn"
          style={loginBtnProps}
        >
          PCA
        </animated.button>
        <animated.button
          onClick={registerClicked}
          id="registerBtn"
          style={registerBtnProps}
        >
          K Means
        </animated.button>
      </div>
      <div className="form-group">
        <animated.form action="" id="loginform" style={loginProps}>
        <h1>Principal Component Analysis</h1>
          <InputFile/>
          <LoginForm />
        </animated.form>
        <animated.form action="" id="registerform" style={registerProps}>
        <h1>K-Means Algorithm</h1>
          <InputFile/>
          <RegisterForm />
        </animated.form>
      </div>
    </div>
    </div>
  );


function LoginForm() {
  return (
    <React.Fragment>
      
      <h2 style={{padding:5}}>Enter number of Principal components</h2>
      <input type="text" value={param} onChange={(e)=>{setParam(e.target.value)}} />
      <input type="button" value="submit" className="submit" onClick={()=>{
        console.log(file_path)
        console.log(param)
        onPcaSend()
      }}/>
    </React.Fragment>
  );
}

function InputFile(){
  return (
    <div>
      <h4 style={{padding:5}}>Select your image to be compressed</h4>
      <input style={{paddingTop: 6}} type='file' id="image" onChange={
        (e)=>{
        setFilePath(e.target.value)
        console.log(e.target.value)
        console.log(file_path)
      }}/>

    </div>
  )
}

function RegisterForm() {
  return (
    <React.Fragment>
      <h2 style={{padding:5}}>Enter number of Clusters </h2>
      <h3 style={{paddingLeft:5}}>Color Bit Rate</h3>
      <input type="text" value={param} onChange={(e)=>{setParam(e.target.value)}} />
      <input  type="button" value="send"  onClick={()=>{onKmeansSend()}} />
    </React.Fragment>
  );
}
}

export default App;
