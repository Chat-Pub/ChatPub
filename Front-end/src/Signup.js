import mainchat from './assets/mainchat.png';
import govmark from './assets/gov.png';
import React, { useState } from 'react';




const CreateAccount = () => {

  const [Name, setName] = useState('');
  const [EmailInput, setEmailInput] = useState('');
  const [Password1, setPassword1] = useState('');
  const [Password2, setPassword2] = useState('');
  
  async function requestRegister() {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/user/create', {
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
      });
  
      if (!response.ok) {
        throw new Error('Failed : Already Existed');
      }
  
      // Handle the successful response
      const responseData = await response.json();
      console.log('Account created successfully:', responseData);
      
      // Login page로 넘어가기
    } catch (error) {
      console.error('Error creating account:', error.message);
    }

  }
  return (
    <div className="LoginFrame" style={{width: 1152, height: 700, position: 'relative', background: '#35CCED', boxShadow: '8px 6px 25px rgba(83.94, 83.94, 83.94, 0.36)', borderRadius: 30, overflow: 'hidden', border: '6px white solid'}}>
      <div className="SignupBox" style={{width: 793, height: 700, left: 373, top: 0,position: 'relative',background: 'white', borderRadius: 40}}>
          <div className="Relogin" style={{left: 129, top: 538, position: 'absolute'}}>
              <div className="AlreadyHaveAnAccount" style={{left: 0, top: 0, position: 'absolute', textAlign: 'center', color: '#C1C1C1', fontSize: 20, fontFamily: 'Roboto', fontWeight: '300', wordWrap: 'break-word',whiteSpace: 'nowrap'}}>Already have an account?</div>
              {/* login link */}
              <div className="Login" style={{left: 233, top: 0, position: 'absolute', textAlign: 'center', color: '#35CCED', fontSize: 20, fontFamily: 'Roboto', fontWeight: '300', wordWrap: 'break-word'}}>Login</div>
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
                <input type="Password1" placeholder="Password" value = {Password1} onChange={(e) => setPassword1(e.target.value)} style={{ width: '470px', border: 'none', borderBottom: 'none', outline: 'none', color :'gray',fontSize: '18px', fontFamily: 'Righteous',fontWeight: '400'}} />
                <div className="Line3" style={{width: 470, height: 0, left: 0, top: 25, position: 'absolute', border: '1px #C1C1C1 solid'}}></div>
              </div>
              <div className="Password2" value = {Password2} onChange={(e) => setPassword2(e.target.value)} style={{width: 470, height: 44, left: 0, top: 167, position: 'absolute'}}>
                {/* Age Input */}
                <input type="Password2" placeholder="Re-type your password" style={{ width: '470px', border: 'none', borderBottom: 'none', outline: 'none', color :'gray',fontSize: '18px', fontFamily: 'Righteous',fontWeight: '400'}} />
                <div className="Line3" style={{width: 470, height: 0, left: 0, top: 25, position: 'absolute', border: '1px #C1C1C1 solid'}}></div>
              </div>

          </div>
          <div className="CreateAccountTitle" style={{left: 47, top: 62, position: 'absolute', textAlign: 'center', color: 'black', fontSize: 36, fontFamily: 'Roboto', fontWeight: '700', wordWrap: 'break-word'}}>Create Account</div>
      </div>
      {/* Create Account Btn */}
      <div className="Createaccount" style={{width: 470, height: 45, left: 556, top: 467, position: 'absolute'}}>
          <div className="Rectangle4" style={{width: 470, height: 45, left: 0, top: 0, position: 'absolute', background: '#35CCED', borderRadius: 10}}></div>
          <div className="CreateAccount" onClick={requestRegister} style={{left: 151, top: 9, position: 'absolute', textAlign: 'center', color: 'white', fontSize: 24, fontFamily: 'Roboto', fontWeight: '900', wordWrap: 'break-word'}} >
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
  )
}
  export default CreateAccount