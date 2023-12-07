import React from 'react'
import { Link } from 'react-router-dom';

import govmark from './assets/gov.png';
import chatmenu from './assets/chat.svg';
import searchmenu from './assets/search.svg';
import homemenu from './assets/home.svg';
import user from './assets/user.svg';


function Detail() {
  return (
    <div className="HomePage" style={{width: '100vw', height: '100vh', position: 'relative', background: 'white'}}>
      <div className="MainFrame" style={{width: 800, height: 675, position: 'absolute', left: '50%', top: '50%', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'center', gap: 64, display: 'inline-flex', transform: 'translate(-50%, -50%)',}}>
        <div className="PersonalInfoTitle" style={{width: 197.14, height: 41, color: '#484848', fontSize: 32, fontFamily: 'Roboto', fontWeight: '800', wordWrap: 'break-word'}}>Personal info</div>
        <div className="PersonalInfoSettings" style={{paddingBottom: 73, paddingRight: 436.67, left: -8, top: 108, position: 'absolute', justifyContent: 'flex-start', alignItems: 'center', display: 'inline-flex'}}>
            <div className="Settings" style={{width: 437.33, alignSelf: 'stretch', paddingBottom: 91, paddingLeft: 8, flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', display: 'inline-flex'}}>
                <div className="LegalNameContainer" style={{width: 595.33, height: 91, paddingTop: 24, paddingBottom: 25, borderBottom: '1px #EBEBEB solid', justifyContent: 'center', alignItems: 'center', display: 'flex'}}>
                    <div className="LegalNameOption" style={{width: 595.33, height: 42, position: 'relative', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', display: 'flex'}}>
                        <div className="LegalNameRow" style={{width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start'}}>
                            <div className="LegalName" style={{color: '#222222', fontSize: 16, fontFamily: 'Roboto', fontWeight: '400', wordWrap: 'break-word'}}>Legal name</div>
                            <div className="Edit" style={{color: '#222222', fontSize: 14, fontFamily: 'Roboto', fontWeight: '600', textDecoration: 'underline', wordWrap: 'break-word'}}>Edit</div>
                        </div>
                        <div className="Name" style={{color: '#717171', fontSize: 14, fontFamily: 'Roboto', fontWeight: '400', wordWrap: 'break-word'}}>John Doe</div>
                    </div>
                </div>

                <div className="EmailContainer" style={{width: 595.33, height: 91, paddingTop: 24, paddingBottom: 25, borderBottom: '1px #EBEBEB solid', justifyContent: 'center', alignItems: 'center', display: 'flex'}}>
                    <div className="EmailAddressOption" style={{width: 595.33, height: 42, position: 'relative', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', display: 'flex'}}>
                        <div className="EmailRow" style={{width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start'}}>
                            <div className="EmailAddress" style={{color: '#222222', fontSize: 16, fontFamily: 'Roboto', fontWeight: '400',  wordWrap: 'break-word'}}>Email address</div>
                            <div className="Edit" style={{color: '#222222', fontSize: 14, fontFamily: 'Roboto', fontWeight: '600', textDecoration: 'underline', wordWrap: 'break-word'}}>Edit</div>
                        </div>
                        <div className="Email" style={{color: '#717171', fontSize: 13, fontFamily: 'Roboto', fontWeight: '400', wordWrap: 'break-word'}}>JohnDoe@gmail.com</div>
                    </div>
                </div>
                <div className="PhoneContainer" style={{width: 595.33, height: 109, paddingTop: 24, paddingBottom: 25, borderBottom: '1px #EBEBEB solid', justifyContent: 'center', alignItems: 'center', display: 'flex'}}>
                    <div className="PhoneNumbersOption" style={{width: 595.33, height: 60, position: 'relative', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', display: 'flex'}}>
                        <div className="PhoneNumbersRow" style={{width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start'}}>
                            <div className="PhoneNumbersTitle" style={{color: '#222222', fontSize: 16, fontFamily: 'Roboto', fontWeight: '400', wordWrap: 'break-word'}}>Phone numbers</div>
                            <div className="Add" style={{color: '#222222', fontSize: 14, fontFamily: 'Roboto', fontWeight: '600', textDecoration: 'underline', wordWrap: 'break-word'}}>Add</div>
                        </div>
                        <div className="PhoneNumber" style={{color: '#717171', fontSize: 14, fontFamily: 'Roboto', fontWeight: '400', wordWrap: 'break-word'}}>010-XXXX-XXXX</div>
                    </div>
                </div>

                <div className="AddressContainer" style={{width: 595.33, height: 91, paddingTop: 24, paddingBottom: 25, borderBottom: '1px #EBEBEB solid', justifyContent: 'center', alignItems: 'center', display: 'flex'}}>
                    <div className="AddressOption" style={{width: 595.33, height: 42, position: 'relative', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', display: 'flex'}}>
                        <div className="AddressRow" style={{width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start'}}>
                            <div className="AddressTitle" style={{color: '#222222', fontSize: 16, fontFamily: 'Roboto', fontWeight: '400',  wordWrap: 'break-word'}}>Address</div>
                            <div className="Edit" style={{color: '#222222', fontSize: 14, fontFamily: 'Roboto', fontWeight: '600', textDecoration: 'underline',  wordWrap: 'break-word'}}>Edit</div>
                        </div>
                        <div className="NotProvided" style={{color: '#717171', fontSize: 14, fontFamily: 'Roboto', fontWeight: '400',  wordWrap: 'break-word'}}>Not provided</div>
                    </div>
                </div>
            </div>
        </div>
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

export default Detail