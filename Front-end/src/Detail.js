import React from 'react'

import govmark from './assets/gov.png';
import chatmenu from './assets/chat.svg';
import searchmenu from './assets/search.svg';
import homemenu from './assets/home.svg';
import user from './assets/user.svg';

function Detail() {
  return (
    <div className="Sidebar" style={{width: 85, height: 1025, paddingTop: 16, paddingBottom: 24, paddingLeft: 16, paddingRight: 16, left: 0, top: -1, position: 'absolute', background: 'white', boxShadow: '0px 0px 24px rgba(0, 0, 0, 0.08)', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'center', gap: 41, display: 'inline-flex'}}>
        <div className="Govmark" style={{width: 69, height: 68, justifyContent: 'center', alignItems: 'center', display: 'inline-flex'}}>
        <img className="Govmark" style={{width: 69, height: 68}} src={govmark} alt ="Govmenu"/>
        </div>
        <div className="MainMenu" style={{width: 54, height: 254, flexDirection: 'column', justifyContent: 'space-between', alignItems: 'center', display: 'flex'}}>
        <div style={{width: 54, height: 56.66, paddingTop: 4.76, paddingBottom: 4.74, paddingLeft: 4.50, paddingRight: 4.50, flexDirection: 'column', justifyContent: 'center', alignItems: 'center', display: 'flex'}}>
            <Link to = "/HomePage">
            <img className="HomeMenu" style={{width: 69, height: 68}} src={homemenu} alt ="Homemenu"/>
            </Link>
        </div>
        <div style={{width: 54, height: 59.09, flexDirection: 'column', justifyContent: 'center', alignItems: 'center', display: 'flex'}}>
            <div style={{width: 54, height: 59.09, position: 'relative', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', display: 'flex'}}>
            <Link to = "/App">
                <img className="ChatMenu" style={{width: 69, height: 68}} src={chatmenu} alt ="ChatMenu"/>
            </Link>
            </div>
        </div>
        <div style={{width: 54, height: 56.66, flexDirection: 'column', justifyContent: 'center', alignItems: 'center', display: 'flex'}}>
            <div style={{width: 54, height: 56.66, paddingLeft: 4.50, paddingRight: 4.50, paddingTop: 4.72, paddingBottom: 4.72, flexDirection: 'column', justifyContent: 'center', alignItems: 'center', display: 'inline-flex'}}>
            <Link to = "/Search">
                <img className="SearchMenu" style={{width: 69, height: 68}} src={searchmenu} alt ="SearchMenu"/>   
            </Link>
            </div>         
        </div>
        <div style={{position: 'fixed', bottom:0,width: 54, height: 56.66, flexDirection: 'column', justifyContent: 'center', alignItems: 'center', display: 'flex'}}>
            <div style={{width: 54, height: 56.66, paddingLeft: 4.50, paddingRight: 4.50, paddingTop: 4.72, paddingBottom: 4.72, flexDirection: 'column', justifyContent: 'center', alignItems: 'center', display: 'inline-flex'}}>
            <Link to ="/Login">
                <img className="UserIcon" style={{width: 69, height: 68}} src={user} alt ="SearchMenu"/>      
            </Link>
            </div>      
        </div>
        </div>
    </div>
  )
}

export default Detail