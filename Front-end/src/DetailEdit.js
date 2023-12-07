import React, { useState } from 'react'
import { Link } from 'react-router-dom';


import govmark from './assets/gov.png';
import chatmenu from './assets/chat.svg';
import searchmenu from './assets/search.svg';
import homemenu from './assets/home.svg';
import user from './assets/user.svg';


function DetailEdit() {

    const [birth, setBirth] = useState('');
    const [gender, setGender] = useState('');
    const [job, setJob] = useState('');
    const [region, setRegion] = useState('');
    const [money, setMoney] = useState(''); 

    async function handlePersonalInfo () {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/userinfo/update', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            authorization: `Bearer ${localStorage.getItem('token')}`,

          },
          body: JSON.stringify({
            birth : birth,
            gender : gender,
            job : job,
            region : region,
            money : money
          }),
        });
  
        if (!response.ok) {
          throw new Error('Saving failed');
        }
    }    catch (error) {
      // Handle saving failure
      console.error('Error during saving:', error.message);
    }

  }

  return (
    <div className="HomePage" style={{width: '100vw', height: '100vh', position: 'relative', background: 'white'}}>
      <div className="MainFrame" style={{width: 800, height: 675, position: 'absolute', left: '50%', top: '50%', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'center', gap: 64, display: 'inline-flex', transform: 'translate(-50%, -50%)',}}>
        <div className="PersonalInfoTitle" style={{width: 197.14, height: 41, color: '#484848', fontSize: 32, fontFamily: 'Roboto', fontWeight: '800', wordWrap: 'break-word'}}>Personal info</div>
        {/* Personal Info */}
        <div className="PersonalInfoSettings" style={{paddingBottom: 73, paddingRight: 436.67, left: -8, top: 108, position: 'absolute', justifyContent: 'flex-start', alignItems: 'center', display: 'inline-flex'}}>
            <div className="Settings" style={{width: 437.33, alignSelf: 'stretch', paddingBottom: 91, paddingLeft: 8, flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', display: 'inline-flex'}}>
                <div className="BirthContainer" style={{width: 595.33, height: 91, paddingTop: 24, paddingBottom: 25, borderBottom: '1px #EBEBEB solid', justifyContent: 'center', alignItems: 'center', display: 'flex'}}>
                    <div className="BirthOption" style={{width: 595.33, height: 42, position: 'relative', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', display: 'flex'}}>
                        <div className="BirthRow" style={{width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start'}}>
                            <div className="Birth" style={{color: '#222222', fontSize: 16, fontFamily: 'Roboto', fontWeight: '400', wordWrap: 'break-word'}}>Birth</div>
                        </div>
                        <input className ="birthInput" type="text" placeholder ="Enter your birth day" value={birth} onChange ={(e) => {setBirth(e.target.value)}} style={{ width: '300px', border: 'none', borderBottom: 'none', outline: 'none' }}/>
                    </div>
                </div>

                <div className="GenderContainer" style={{width: 595.33, height: 91, paddingTop: 24, paddingBottom: 25, borderBottom: '1px #EBEBEB solid', justifyContent: 'center', alignItems: 'center', display: 'flex'}}>
                    <div className="GenderOption" style={{width: 595.33, height: 42, position: 'relative', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', display: 'flex'}}>
                        <div className="GenderRow" style={{width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start'}}>
                            <div className="Gender" style={{color: '#222222', fontSize: 16, fontFamily: 'Roboto', fontWeight: '400',  wordWrap: 'break-word'}}>Gender</div>
                        </div>
                        <input className ="GenderInput" type="text" placeholder ="Male or Female?" value={gender} onChange ={(e) => {setGender(e.target.value)}}style={{ width: '300px', border: 'none', borderBottom: 'none', outline: 'none' }}/>
                    </div>
                </div>
                <div className="JobContainer" style={{width: 595.33, height: 109, paddingTop: 24, paddingBottom: 25, borderBottom: '1px #EBEBEB solid', justifyContent: 'center', alignItems: 'center', display: 'flex'}}>
                    <div className="JobOption" style={{width: 595.33, height: 42, position: 'relative', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', display: 'flex'}}>
                        <div className="JobRow" style={{width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start'}}>
                            <div className="Job" style={{color: '#222222', fontSize: 16, fontFamily: 'Roboto', fontWeight: '400', wordWrap: 'break-word'}}>Occupation</div>
                        </div>
                        <input className ="JobInput" type="text" placeholder ="Enter your Occupation" value={job} onChange ={(e) => {setJob(e.target.value)}}style={{ width: '300px', border: 'none', borderBottom: 'none', outline: 'none' }}/>
                    </div>
                </div>
                <div className="RegionContainer" style={{width: 595.33, height: 91, paddingTop: 24, paddingBottom: 25, borderBottom: '1px #EBEBEB solid', justifyContent: 'center', alignItems: 'center', display: 'flex'}}>
                    <div className="RegionOption" style={{width: 595.33, height: 42, position: 'relative', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', display: 'flex'}}>
                        <div className="RegionRow" style={{width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start'}}>
                            <div className="RegionTitle" style={{color: '#222222', fontSize: 16, fontFamily: 'Roboto', fontWeight: '400',  wordWrap: 'break-word'}}>Region/Address</div>
                        </div>
                        <input className ="RegionInput" type="text" placeholder ="Enter your province or Adress" value={region} onChange ={(e) => {setRegion(e.target.value)}}style={{ width: '300px', border: 'none', borderBottom: 'none', outline: 'none' }}/>
                    </div>
                </div>
                <div className="MoneyContainer" style={{width: 595.33, height: 91, paddingTop: 24, paddingBottom: 25, borderBottom: '1px #EBEBEB solid', justifyContent: 'center', alignItems: 'center', display: 'flex'}}>
                    <div className="MoneyOption" style={{width: 595.33, height: 42, position: 'relative', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', display: 'flex'}}>
                        <div className="MoneyRow" style={{width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start'}}>
                            <div className="Money" style={{color: '#222222', fontSize: 16, fontFamily: 'Roboto', fontWeight: '400',  wordWrap: 'break-word'}}>Profit</div>
                        </div>
                        <input className ="MoneyInput" type="text" placeholder ="Enter your profit" value={money} onChange ={(e) => {setMoney(e.target.value)}}style={{ width: '300px', border: 'none', borderBottom: 'none', outline: 'none' }}/>
                    </div>
                </div>
            </div>
        </div>

        {/* Save Button */}
        <Link to="/Detail">
        <div className="SaveButton" style={{ width: 470, height: 45, left: '50%', bottom: 20, position: 'absolute', transform: 'translateX(-50%)' }}>
            <div className="Rectangle4" style={{ width: '50%', height: '100%', position: 'absolute', background: '#35CCED', borderRadius: 10 }}></div>
            <div className="Save" onClick={handlePersonalInfo} style={{ left: '95px', bottom: '50%', position: 'absolute', width: '100%', transform: 'translateY(50%)', color: 'white', fontSize: 24, fontFamily: 'Roboto', fontWeight: '900', wordWrap: 'break-word' }}>Save! </div>
        </div>
        </Link>
      </div>
                
      
      <div className="Sidebar" style={{width: 66, height: '100vh', paddingTop: 16, paddingBottom: 24, paddingLeft: 16, paddingRight: 16, left: 0, top: -1, position: 'absolute', background: 'white', boxShadow: '0px 0px 24px rgba(0, 0, 0, 0.08)', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'center', gap: 41, display: 'inline-flex'}}>
        <div className="Govmark" style={{width: 69, height: 68, justifyContent: 'center', alignItems: 'center', display: 'inline-flex'}}>
          <img className="Govmark" style={{width: 50, height: 50}} src={govmark} alt ="Govmenu"/>
        </div>
        <div className="MainMenu" style={{width: 54, height: 254, flexDirection: 'column', justifyContent: 'space-between', alignItems: 'center', display: 'flex'}}>
          <div style={{width: 54, height: 56.66, paddingTop: 4.76, paddingBottom: 4.74, paddingLeft: 4.50, paddingRight: 4.50, flexDirection: 'column', justifyContent: 'center', alignItems: 'center', display: 'flex'}}>
            <Link to = "/HomePage">
              <img className="HomeMenu" style={{width: 40, height: 68 }} src={homemenu} alt ="Homemenu"/>
            </Link>
          </div>
          <div style={{width: 54, height: 59.09, marginLeft:'11px', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', display: 'flex'}}>
            <div style={{width: 54, height: 59.09, position: 'relative', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', display: 'flex'}}>
                  <Link to = "/App">
                    <img className="ChatMenu" style={{width: 40, height: 68}} src={chatmenu} alt ="ChatMenu"/>
                  </Link>
            </div>
          </div>
          <div style={{width: 54, height: 56.66, flexDirection: 'column', justifyContent: 'center', alignItems: 'center', display: 'flex'}}>
            <div style={{width: 54, height: 56.66, paddingLeft: 4.50, paddingRight: 4.50, paddingTop: 4.72, paddingBottom: 4.72, flexDirection: 'column', justifyContent: 'center', alignItems: 'center', display: 'inline-flex'}}>
              <Link to = "/Search">
                <img className="SearchMenu" style={{width: 40, height: 68}} src={searchmenu} alt ="SearchMenu"/>   
              </Link>
            </div>         
          </div>
        </div>
          <div className ="userIcon" style={{ position:'absolute',bottom: 0, width: '100%', background: 'white', zIndex: 1000, display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '8px' }}>
              <Link to ="/Login">
                <img className="UserIcon" style={{width: 45, height: 68}} src={user} alt ="UserIcon"/>      
              </Link>
          </div>
      </div>
    </div>

  )
}

export default DetailEdit