import React, { useEffect } from 'react'
import {Link} from 'react-router-dom';
import { useState } from 'react';

import mainchat from './assets/mainchat.png';
import govmark from './assets/gov.png';
import chatmenu from './assets/chat.svg';
import searchmenu from './assets/search.svg';
import logout from './assets/logout.svg';
import homemenu from './assets/home.svg';
import user from './assets/user.svg';
import comet from './assets/comet.svg';
import bolt from './assets/bolt.svg';
import sparkles from './assets/sparkles.svg';

function Home() {
  const [isLogin, setIsLogin] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token === null) {
      setIsLogin(false);
    }
    else {
      setIsLogin(true);
    }
  }, []);

 const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLogin(false);
    window.location.href = "/HomePage";
  }
 

  

  return (
    <div className="HomePage" style={{width: '100vw', height: '100vh', position: 'relative', background: 'white'}}>
      <div className="MainFrame" style={{width: 800, height: 675, position: 'absolute', left: '50%', top: '50%', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'center', gap: 64, display: 'inline-flex', transform: 'translate(-50%, -50%)',}}>
        <div className="ChatPubTitle" style={{height: 219, flexDirection: 'column', justifyContent: 'center', alignItems: 'center', gap: 12, display: 'flex'}}>
          <img className="Chatpub" alt="mainChat" style={{width: 120, height: 115}} src={mainchat} />
          <div className="ChatPub" style={{color: 'black', fontSize: 40, fontFamily: 'Poppins', fontWeight: 800, wordWrap: 'break-word'}}>CHAT-PUB</div>
          <div className="VersionInfo" style={{color: '#919191', fontSize: 16, fontFamily: 'Inter', fontWeight: '400', lineHeight: 2, wordWrap: 'break-word'}}>Ver. 1.0.1</div>
        </div>
        <div className="Homeinfo" style={{width: 800, justifyContent: 'flex-start', alignItems: 'flex-start', gap: 24, display: 'inline-flex'}}>
          <div className="Examples" style={{flex: '1 1 0', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', gap: 16, display: 'inline-flex'}}>
            <div className="Example1" style={{alignSelf: 'stretch', height: 185, paddingLeft: 24, paddingRight: 24, paddingTop: 20, paddingBottom: 20, background: 'white', borderRadius: 12, overflow: 'hidden', border: '2px #E7E7E7 solid', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', gap: 10, display: 'flex'}}>
              <div className="Examplemain" style={{alignSelf: 'stretch', height: 145, flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', gap: 20, display: 'flex'}}>
                <div className="Exampleicon" style={{padding: 12, background: '#F8F8F8', borderRadius: 90, justifyContent: 'flex-start', alignItems: 'flex-start', gap: 10, display: 'inline-flex'}}>
                  <div className="Sparkles" style={{width: 24, height: 24, padding: 3, justifyContent: 'center', alignItems: 'center', display: 'flex'}}>
                    <img className='sparkles' src={sparkles} alt='sparkles'></img>
                  </div>
                </div>
                <div className="Exampleinfo" style={{alignSelf: 'stretch', height: 77, flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', gap: 12, display: 'flex'}}>
                  <div className="Examples" style={{alignSelf: 'stretch', color: 'black', fontSize: 18, fontFamily: 'Poppins', fontWeight: '600', wordWrap: 'break-word'}}>Examples</div>
                  <div className="Text" style={{alignSelf: 'stretch', color: '#919191', fontSize: 14, fontFamily: 'Poppins', fontWeight: '400', wordWrap: 'break-word'}}> What are some policies that will benefit me?</div>
                </div>
              </div>
            </div>
            <div className="Exapmle2" style={{alignSelf: 'stretch', height: 78, paddingLeft: 24, paddingRight: 24, paddingTop: 17, paddingBottom: 20, background: 'white', borderRadius: 12, overflow: 'hidden', border: '2px #E7E7E7 solid', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', gap: 10, display: 'flex'}}>
              <div className="Exampleinfo" style={{alignSelf: 'stretch'}}>
                <span style={{color: '#919191', fontSize: 14, fontFamily: 'Poppins', fontWeight: '400',wordWrap: 'break-word'}}>How can I apply for housing aid for Seoul residents? </span>
                </div>
            </div>
            <div className="Example3" style={{alignSelf: 'stretch', height: 97, paddingLeft: 24, paddingRight: 24, paddingTop: 15, paddingBottom: 20, background: 'white', borderRadius: 12, overflow: 'hidden', border: '2px #E7E7E7 solid', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', gap: 10, display: 'flex'}}>
              <div className="Exampleinfo" style={{alignSelf: 'stretch'}}>
                <span style={{color: '#919191', fontSize: 14, fontFamily: 'Poppins', fontWeight: '400', wordWrap: 'break-word'}}>Can you tell me about any job education that is available for me? </span>
                </div>
            </div>
          </div>
          <div className="Capabilities" style={{flex: '1 1 0', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', gap: 16, display: 'inline-flex'}}>
            <div className="Capability1" style={{alignSelf: 'stretch', height: 180, paddingLeft: 24, paddingRight: 24, paddingTop: 20, paddingBottom: 20, background: 'white', borderRadius: 12, overflow: 'hidden', border: '2px #E7E7E7 solid', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', gap: 10, display: 'flex'}}>
              <div className="Capabilitymain" style={{alignSelf: 'stretch', height: 149, flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', gap: 20, display: 'flex'}}>
                <div className="Capabilityicon" style={{padding: 12, background: '#F8F8F8', borderRadius: 90, justifyContent: 'flex-start', alignItems: 'flex-start', gap: 10, display: 'inline-flex'}}>
                  <div className="Star" style={{width: 24, height: 24, paddingTop: 2.24, paddingBottom: 3.91, paddingLeft: 2.66, paddingRight: 2.66, justifyContent: 'center', alignItems: 'center', display: 'flex'}}>
                    <img className='bolt' src={bolt} alt='bolt'></img>
                  </div>
                </div>
                <div className="Capabilityinfo" style={{alignSelf: 'stretch', height: 81, flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', gap: 12, display: 'flex'}}>
                  <div className="Capabilities" style={{alignSelf: 'stretch', color: 'black', fontSize: 18, fontFamily: 'Poppins', fontWeight: '600', wordWrap: 'break-word'}}>Capabilities</div>
                  <div className="Text" style={{alignSelf: 'stretch', color: '#919191', fontSize: 14, fontFamily: 'Poppins', fontWeight: '400', wordWrap: 'break-word'}}>Remembers what user said earlier in the conversation</div>
                </div>
              </div>
            </div>
            <div className="Capapbility2" style={{alignSelf: 'stretch', height: 78, paddingLeft: 24, paddingRight: 24, paddingTop: 20, paddingBottom: 20, background: 'white', borderRadius: 12, overflow: 'hidden', border: '2px #E7E7E7 solid', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', gap: 10, display: 'flex'}}>
              <div className="Capabilityinfo" style={{alignSelf: 'stretch', color: '#919191', fontSize: 14, fontFamily: 'Poppins', fontWeight: '400', wordWrap: 'break-word'}}>Allows user to provide follow-up corrections</div>
            </div>
            <div className="Capapbility3" style={{alignSelf: 'stretch', height: 78, paddingLeft: 24, paddingRight: 24, paddingTop: 20, paddingBottom: 20, background: 'white', borderRadius: 12, overflow: 'hidden', border: '2px #E7E7E7 solid', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', gap: 10, display: 'flex'}}>
              <div className="Capabilityinfo" style={{alignSelf: 'stretch', color: '#919191', fontSize: 14, fontFamily: 'Poppins', fontWeight: '400', wordWrap: 'break-word'}}>Trained to decline inappropriate requests</div>
            </div>
          </div>
          <div className="Limitations" style={{flex: '1 1 0', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', gap: 16, display: 'inline-flex'}}>
            <div className="Limitation1" style={{alignSelf: 'stretch', height: 180, paddingLeft: 24, paddingRight: 24, paddingTop: 20, paddingBottom: 20, background: 'white', borderRadius: 12, overflow: 'hidden', border: '2px #E7E7E7 solid', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', gap: 10, display: 'flex'}}>
              <div className="Limitationmain" style={{alignSelf: 'stretch', height: 141, flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', gap: 20, display: 'flex'}}>
                <div className="Limitationicon" style={{padding: 12, background: '#F8F8F8', borderRadius: 90, justifyContent: 'flex-start', alignItems: 'flex-start', gap: 10, display: 'inline-flex'}}>
                  <div className="Exclamation" style={{width: 24, height: 24, paddingTop: 3, paddingBottom: 5, paddingLeft: 3.07, paddingRight: 3.07, justifyContent: 'center', alignItems: 'center', display: 'flex'}}>
                    <img className='comet' src={comet} alt='comet'></img>
                  </div>
                </div>
                <div className="Limitationinfo" style={{alignSelf: 'stretch', height: 73, flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', gap: 12, display: 'flex'}}>
                  <div className="Limitations" style={{alignSelf: 'stretch', color: 'black', fontSize: 18, fontFamily: 'Poppins', fontWeight: '600', wordWrap: 'break-word'}}>Limitations</div>
                  <div className="Text" style={{alignSelf: 'stretch', color: '#919191', fontSize: 14, fontFamily: 'Inter', fontWeight: '400', wordWrap: 'break-word'}}>May occasionally generate incorrect information</div>
                </div>
              </div>
            </div>
            <div className="Limitation2" style={{alignSelf: 'stretch', height: 78, paddingLeft: 24, paddingRight: 24, paddingTop: 20, paddingBottom: 20, background: 'white', borderRadius: 12, overflow: 'hidden', border: '2px #E7E7E7 solid', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', gap: 10, display: 'flex'}}>
              <div className="Limitationinfo" style={{alignSelf: 'stretch', color: '#919191', fontSize: 14, fontFamily: 'Inter', fontWeight: '400', wordWrap: 'break-word'}}>It does not guarantee. Please use with caution.</div>
            </div>
            <div className="Limitation3" style={{alignSelf: 'stretch', height: 78, paddingLeft: 24, paddingRight: 24, paddingTop: 20, paddingBottom: 20, background: 'white', borderRadius: 12, overflow: 'hidden', border: '2px #E7E7E7 solid', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', gap: 10, display: 'flex'}}>
              <div className="Limitationinfo" style={{alignSelf: 'stretch', color: '#919191', fontSize: 14, fontFamily: 'Poppins', fontWeight: '400',wordWrap: 'break-word'}}>Limited knowledge of policy <br/></div>
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
              {!isLogin && (
              <Link to ="/Login">
              <img className="UserIcon" style={{width: 45, height: 68}} src={user} alt ="UserIcon"/>      
              </Link>)}

              {isLogin && (
              <div>
                <Link to ="/Detail">
                  <img className="UserIcon" style={{width: 45, height: 68}} src={user} alt ="UserIcon"/>      
                </Link>
                <img className="Logout" style={{width: 45, height: 68}} src={logout} alt ="ExitIcon" onClick={() => handleLogout(true)}/>      
              </div>
              )}
          </div>
      </div>
    </div>
  );
}

export default Home;