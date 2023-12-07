import mainchat from './assets/mainchat.png';
import govmark from './assets/gov.png';
import React, { useState } from 'react';
import { Link,useNavigate } from 'react-router-dom';




const CreateAccount = () => {

  const [Name, setName] = useState('');
  const [EmailInput, setEmailInput] = useState('');
  const [Password1, setPassword1] = useState('');
  const [Password2, setPassword2] = useState('');
  
  async function requestRegister() {
    try {
      await fetch(`${process.env.REACT_APP_SERVER}/user/create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Add any additional headers if needed
        },
        // Add the request body if needed
        body: JSON.stringify({         
          username : Name, 
          password1: Password1,
          password2 : Password2,
          email: EmailInput }),
      })
      .then(response => {
        if (response.status === 204) {
          alert("회원가입 성공");
          window.location.href = "/Login";
        } else {  
          alert("회원가입 실패");
        }
      })

      // Login page로 넘어가기
    } catch (error) {
      console.error('Error creating account:', error.message);
    }

  }



  return (
    <div style={{minWidth: '1000px', minHeight: '800px', width : '100vw', height: '100vh', background: '#35CCED57'}}>
      <div className="LoginFrame" style={{width: 1152, height: 700, position: 'absolute', left: 'calc(50%)', transform: 'translate(-50%, -50%)', top: '50%', background: '#35CCED', boxShadow: '8px 6px 25px rgba(83.94, 83.94, 83.94, 0.36)', borderRadius: 30, overflow: 'hidden', border: '6px white solid'}}>
        <div className="SignupBox" style={{width: 793, height: 700, left: 373, top: 0,position: 'relative',background: 'white', borderRadius: 40}}>
            <div className="Relogin" style={{width: 269, height: 31, left: 127, top: 457, position: 'absolute'}}>
                <div className="AlreadyHaveAnAccount" style={{left: 0, top: 0, position: 'absolute', textAlign: 'center', color: '#C1C1C1', fontSize: 20, fontFamily: 'Poppins', fontWeight: '300', wordWrap: 'break-word',whiteSpace: 'nowrap'}}>Already have an account?</div>
                {/* login link */}
                <Link to = "/Login">
                  <div className="Login" style={{left: 233, top: 0, position: 'absolute', textAlign: 'center', color: '#35CCED', fontSize: 20, fontFamily: 'Poppins', fontWeight: '300', wordWrap: 'break-word'}}>Login</div>
                </Link>
                <Link to="/HomePage">
                <div className="Home" style={{width: 90, height: 30, left: 388, top: 0, position: 'absolute', textAlign: 'center', color: '#35CCED', fontSize: 18, fontFamily: 'Poppins', fontWeight: '300', wordWrap: 'break-word'}}>Go Home</div>
              </Link>
            </div>   
            {/* 회원 가입을 위한 정보 통신  */}
            <div className="Personalinfo" style={{width: 470, height: 276, left: 126, top: 169, position: 'absolute'}}>
                <div className="FullName" style={{width: 470, height: 27, left: 0, top: 0, position: 'absolute'}}>
                  {/* Name Input */}
                  <input type="Name" placeholder="Full Name" value = {Name} onChange={(e) => setName(e.target.value)} style={{ width: '470px', border: 'none', borderBottom: 'none', outline: 'none', color :'gray',fontSize: '18px', fontFamily: 'Righteous',fontWeight: '400'}} />
                  <div className="Line1" style={{width: 470, height: 0, left: 0, top: 27, position: 'absolute', border: '1px #C1C1C1 solid'}}></div>
                </div>
                <div className="EmailAddress" style={{width: 470, height: 27, left: 0, top: 54, position: 'absolute'}}>
                  {/* Email Input */}
                  <input type="EmailInput" placeholder="Email Adress" value = {EmailInput} onChange={(e) => setEmailInput(e.target.value)} style={{ width: '470px', border: 'none', borderBottom: 'none', outline: 'none', color :'gray',fontSize: '18px', fontFamily: 'Righteous',fontWeight: '400'}} /> 
                  <div className="Line2" style={{width: 470, height: 0, left: 0, top: 27, position: 'absolute', border: '1px #C1C1C1 solid'}}></div>
                </div>
                <div className="Password1" style={{width: 470, height: 25, left: 0, top: 108, position: 'absolute'}}>
                  {/* Password Input */}
                  <input type="password" placeholder="Password" value = {Password1} onChange={(e) => setPassword1(e.target.value)} style={{ width: '470px', border: 'none', borderBottom: 'none', outline: 'none', color :'gray',fontSize: '18px', fontFamily: 'Righteous',fontWeight: '400'}} />
                  <div className="Line3" style={{width: 470, height: 0, left: 0, top: 25, position: 'absolute', border: '1px #C1C1C1 solid'}}></div>
                </div>
                <div className="Password2" value = {Password2} onChange={(e) => setPassword2(e.target.value)} style={{width: 470, height: 44, left: 0, top: 167, position: 'absolute'}}>
                  {/* Age Input */}
                  <input type="password" placeholder="Re-type your password" style={{ width: '470px', border: 'none', borderBottom: 'none', outline: 'none', color :'gray',fontSize: '18px', fontFamily: 'Righteous',fontWeight: '400', paddingTop:'3px'}} />
                  <div className="Line3" style={{width: 470, height: 0, left: 0, top: 25, position: 'absolute', border: '1px #C1C1C1 solid'}}></div>
                </div>

            </div>
            <div className="CreateAccountTitle" style={{left: 127, top: 62, position: 'absolute', textAlign: 'center', color: 'black', fontSize: 36, fontFamily: 'Poppins', fontWeight: '700', wordWrap: 'break-word'}}>Create Account</div>
        </div>
        {/* Create Account Btn */}
        <div className="Createaccount" onClick={requestRegister} style={{width: 470, height: 45, left: 500, top: 400, position: 'absolute'}}>
            <div className="Rectangle4" style={{width: 470, height: 45, left: 0, top: 0, position: 'absolute', background: '#35CCED', borderRadius: 10}}></div>
            <div className="CreateAccount"  style={{left: 151, top: 9, position: 'absolute', textAlign: 'center', color: 'white', fontSize: 24, fontFamily: 'Poppins', fontWeight: '900', wordWrap: 'break-word'}} >
              Create Account
            </div>


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
  export default CreateAccount