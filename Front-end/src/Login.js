import React from 'react';
import { Link } from 'react-router-dom';
import { useState } from 'react';


// 이미지 import
import mainchat from './assets/mainchat.png';
import govmark from './assets/gov.png';

const Login  = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  async function handleLogin() {
    try {
      console.log(process.env.REACT_APP_SERVER);
      await fetch(`${process.env.REACT_APP_SERVER}/user/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          "username" : username,
          "password" : password,
          "grant_type" : "password"
        }),
      })
      .then(response => {
        if (response.status !== 200) {
          alert("로그인 실패");
          throw Error("로그인 실패");
        } 
        return response.json();
      })
        .then(data => {
        const token = data.access_token
              localStorage.setItem('token', token);
              alert("로그인 성공");
        window.location.href = "/HomePage";
      })

    } catch (error) {
      // Handle login failure
      console.error('Error during login:', error.message);
    }
  };

  return (
  <div style={{minWidth: '1000px', minHeight: '800px', width : '100vw', height: '100vh', background: '#35CCED57'}}>
    <div className="LoginFrame" style={{width: 1152, height: 700, position: 'absolute', left: 'calc(50%)', transform: 'translate(-50%, -50%)', top: '50%', flexDirection: 'column', background: '#35CCED', boxShadow: '8px 6px 25px rgba(83.94, 83.94, 83.94, 0.36)', borderRadius: 30, overflow: 'hidden', border: '6px white solid'}}>
        <div className="LoginPage" style={{width: 793, height: 700, left: 373, top: 0, position: 'absolute', background: 'white', borderRadius: 40}}>
          <div className="Signup" style={{width: 269, height: 31, left: 105, top: 457, position: 'absolute'}}>
            <div className="NotAMember" style={{width: 159, height: 30, left: 0, top: 1, position: 'absolute', textAlign: 'center', color: '#C1C1C1', fontSize: 18, fontFamily: 'Roboto', fontWeight: '300', wordWrap: 'break-word'}}>Not a Member?</div>
              {/* signup */}
              <Link to="/signup">
                <div className="SignUp" style={{width: 70, height: 30, left: 139, top: 0, position: 'absolute', textAlign: 'center', color: '#35CCED', fontSize: 18, fontFamily: 'Roboto', fontWeight: '300', wordWrap: 'break-word'}}>Sign Up</div>
              </Link>
              {/* go home */}
              <Link to="/HomePage">
                <div className="Home" style={{width: 90, height: 30, left: 411, top: 0, position: 'absolute', textAlign: 'center', color: '#35CCED', fontSize: 18, fontFamily: 'Roboto', fontWeight: '300', wordWrap: 'break-word'}}>Go Home</div>
              </Link>
          </div>
          {/* id */}
          <div className="Id" style={{width: 470, height: 27, left: 126, top: 202, position: 'absolute'}}>
            <input type="Id" placeholder="ID" value = {username}  onChange={(e)=> {setUsername(e.target.value)}} style={{ width: '300px', border: 'none', borderBottom: 'none', outline: 'none' }} />
            <div className="IdLine" style={{width: 470, height: 0, left: 0, top: 27, position: 'absolute', border: '1px #C1C1C1 solid'}}></div>
          </div>
          {/* password */}
          <div className="Password" style={{height: 25, left: 126, top: 311, position: 'absolute'}}>
            <input type="password" placeholder="Password" value = {password} onChange={(e)=> {setPassword(e.target.value)}} style={{ width: '300px', border: 'none', borderBottom: 'none', outline: 'none' }} />
            <div className="PWLine" style={{width: 470, height: 0, left: 0, top: 25, position: 'absolute', border: '1px #C1C1C1 solid'}}></div>
          </div>
          <div className="LogInTitle" style={{left: 127, top: 62, position: 'absolute', textAlign: 'center', color: 'black', fontSize: 36, fontFamily: 'Roboto', fontWeight: '700', wordWrap: 'break-word'}}>Log in </div>
        </div>

        {/* login btn */}
          <div className="LoginButton" onClick = {handleLogin} style={{width: 470, height: 45, left: 500, top: 400, position: 'absolute'}}>
            <div className="Rectangle4"  style={{width: 470, height: 45, left: 0, top: 0, position: 'absolute', background: '#35CCED', borderRadius: 10}}></div>
            <div className="Login"  style={{left: 205, top: 9, position: 'absolute', textAlign: 'center', color: 'white', fontSize: 24, fontFamily: 'Roboto', fontWeight: '900', wordWrap: 'break-word'}}>Login </div>
          </div>
        <div className="GovMark" style={{width: 69, height: 68, left: 11, top: 14, position: 'absolute', justifyContent: 'center', alignItems: 'center', display: 'inline-flex'}}>
          <div className="GovMark" style={{width: 69, height: 68, justifyContent: 'center', alignItems: 'center', display: 'inline-flex'}}>
            <img className="GovMarkIcon" alt ="GovMark" style={{width: 69, height: 68}} src= {govmark} />
          </div>
        </div>
        <div className="HelperOfWelfarePolicyForYouth" style={{width: 394, height: 149, left: 36, top: 162, position: 'absolute', justifyContent: 'center', alignItems: 'center', display: 'inline-flex'}}>
          <div className="HelperOfWelfarePolicyForYouth" style={{width: 394, height: 149, color: 'white', fontSize: 36, fontFamily: 'Poppins', fontWeight: '600', wordWrap: 'break-word'}}>Helper of welfare policy for youth</div>
        </div>
        <div className="Mainchat" style={{width: 374, height: 375, left: 145, top: 379, position: 'absolute', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', display: 'inline-flex'}}>
          <img className="chaticon" alt = "MainIcon"style={{width: 374, height: 375}} src={mainchat} />
        </div>
    </div>
  </div>
  )
}

export default Login