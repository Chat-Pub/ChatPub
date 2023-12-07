import React from 'react'
import { Link } from 'react-router-dom';

import govmark from './assets/gov.png';
import chatmenu from './assets/chat.svg';
import searchmenu from './assets/search.svg';
import homemenu from './assets/home.svg';
import user from './assets/user.svg';

import searchbarIcon from './assets/searchbar.svg'

function Search() {
  return (
    <div className="HomePage" style={{width: '100vw', height: '100vh', position: 'relative', background: 'white'}}>
      <div className="MainFrame" style={{width: 800, height: 675, position: 'absolute', left: '50%', top: '50%', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'center', gap: 64, display: 'inline-flex', transform: 'translate(-50%, -50%)',}}>
        <div className="SearchBar" style={{width: 1001, height: 91, position: 'relative'}}>
            <div className="Bar" placeholder='Search' style={{width: 930.42, height: 91, left: 54.67, top: 0, position: 'absolute', background: 'rgba(255, 255, 255, 0.02)', borderRadius: 299, border: '4px rgba(205.06, 200.79, 200.79, 0.40) solid', backdropFilter: 'blur(350px)'}} />
                <img className="SearchBarIcon" style={{width: 73.56, height: 72.41, background: '#EBE9E9'}} src={searchbarIcon} alt='SearchBarIcon'/>
            <div className="Search" style={{width: 519.88, height: 43.05, left: 0, top: 12.72, position: 'absolute', textAlign: 'center', color: 'rgba(229, 229, 229, 0.54)', fontSize: 51, fontFamily: 'Inter', fontWeight: '700', wordWrap: 'break-word'}}>Search</div>
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

export default Search