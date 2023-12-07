import React from 'react'
import { Link } from 'react-router-dom';
import { useState, useEffect } from 'react';


import govmark from './assets/gov.png';
import chatmenu from './assets/chat.svg';
import searchmenu from './assets/search.svg';
import homemenu from './assets/home.svg';
import user from './assets/user.svg';
import logout from './assets/logout.svg';


  
const UserInfo = () => {
  const [birth, setBirth] = useState(null);
  const [gender, setGender] = useState(null);
  const [job, setJob] = useState(null);
  const [region, setRegion] = useState(null);
  const [money, setMoney] = useState(null);

  useEffect(() => {
    // 각 정보를 가져오는 함수 호출
    fetchUserData();
  }); // 빈 배열을 넣어 한 번만 실행되도록 설정

  // 각 정보를 가져오는 함수 정의
  const fetchData = async (url, stateSetter) => {
    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          authorization: `Bearer ${localStorage.getItem('token')}`,
          // 다른 헤더가 필요하다면 여기에 추가
        },
      });
      if (!response.ok) {
        throw new Error('Data fetch failed');
      }

      const data = await response.json();
      stateSetter(data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const fetchUserData = () => {
    fetchData(`${process.env.REACT_APP_SERVER}/userinfo/detail`, setUserData);
  };

  const setUserData = (data) => {
    // 받아온 데이터에서 필요한 정보 추출 및 상태 업데이트
    setBirth(data.birth);
    setGender(data.gender);
    setJob(data.job);
    setRegion(data.region);
    setMoney(data.money);
  };

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
        <div className="PersonalInfoTitle" style={{width: 197.14, height: 41, color: '#484848', fontSize: 32, fontFamily: 'Roboto', fontWeight: '800', wordWrap: 'break-word'}}>Personal Info</div>
        {/* Personal Info */}
        <div className="PersonalInfoSettings" style={{paddingBottom: 73, paddingRight: 436.67, left: -8, top: 108, position: 'absolute', justifyContent: 'flex-start', alignItems: 'center', display: 'inline-flex'}}>
            <div className="Settings" style={{width: 437.33, alignSelf: 'stretch', paddingBottom: 91, paddingLeft: 8, flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', display: 'inline-flex'}}>
                <div className="BirthContainer" style={{width: 595.33, height: 91, paddingTop: 24, paddingBottom: 25, borderBottom: '1px #EBEBEB solid', justifyContent: 'center', alignItems: 'center', display: 'flex'}}>
                    <div className="BirthOption" style={{width: 595.33, height: 42, position: 'relative', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', display: 'flex'}}>
                        <div className="BirthRow" style={{width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start'}}>
                            <div className="Birth" style={{color: '#222222', fontSize: 16, fontFamily: 'Roboto', fontWeight: '400', wordWrap: 'break-word'}}>Birth</div>
                        </div>
                        <div className="BirthInfo" style={{color: '#717171', fontSize: 14, fontFamily: 'Roboto', fontWeight: '400', wordWrap: 'break-word'}}>{birth}</div>
                    </div>
                </div>

                <div className="GenderContainer" style={{width: 595.33, height: 91, paddingTop: 24, paddingBottom: 25, borderBottom: '1px #EBEBEB solid', justifyContent: 'center', alignItems: 'center', display: 'flex'}}>
                    <div className="GenderOption" style={{width: 595.33, height: 42, position: 'relative', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', display: 'flex'}}>
                        <div className="GenderRow" style={{width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start'}}>
                            <div className="Gender" style={{color: '#222222', fontSize: 16, fontFamily: 'Roboto', fontWeight: '400',  wordWrap: 'break-word'}}>Gender</div>
                        </div>
                        <div className="GenderInfo" style={{color: '#717171', fontSize: 13, fontFamily: 'Roboto', fontWeight: '400', wordWrap: 'break-word'}}>{gender}</div>
                    </div>
                </div>
                <div className="JobContainer" style={{width: 595.33, height: 109, paddingTop: 24, paddingBottom: 25, borderBottom: '1px #EBEBEB solid', justifyContent: 'center', alignItems: 'center', display: 'flex'}}>
                    <div className="JobOption" style={{width: 595.33, height: 42, position: 'relative', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', display: 'flex'}}>
                        <div className="JobRow" style={{width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start'}}>
                            <div className="Job" style={{color: '#222222', fontSize: 16, fontFamily: 'Roboto', fontWeight: '400', wordWrap: 'break-word'}}>Occupation</div>
                        </div>
                        <div className="JobInfo" style={{color: '#717171', fontSize: 14, fontFamily: 'Roboto', fontWeight: '400', wordWrap: 'break-word'}}>{job}</div>
                    </div>
                </div>
                <div className="RegionContainer" style={{width: 595.33, height: 91, paddingTop: 24, paddingBottom: 25, borderBottom: '1px #EBEBEB solid', justifyContent: 'center', alignItems: 'center', display: 'flex'}}>
                    <div className="RegionOption" style={{width: 595.33, height: 42, position: 'relative', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', display: 'flex'}}>
                        <div className="RegionRow" style={{width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start'}}>
                            <div className="RegionTitle" style={{color: '#222222', fontSize: 16, fontFamily: 'Roboto', fontWeight: '400',  wordWrap: 'break-word'}}>Region/Address</div>
                        </div>
                        <div className="RegionInfo" style={{color: '#717171', fontSize: 14, fontFamily: 'Roboto', fontWeight: '400',  wordWrap: 'break-word'}}>{region}</div>
                    </div>
                </div>
                <div className="MoneyContainer" style={{width: 595.33, height: 91, paddingTop: 24, paddingBottom: 25, borderBottom: '1px #EBEBEB solid', justifyContent: 'center', alignItems: 'center', display: 'flex'}}>
                    <div className="MoneyOption" style={{width: 595.33, height: 42, position: 'relative', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', display: 'flex'}}>
                        <div className="MoneyRow" style={{width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start'}}>
                            <div className="Money" style={{color: '#222222', fontSize: 16, fontFamily: 'Roboto', fontWeight: '400',  wordWrap: 'break-word'}}>Profit</div>
                        </div>
                        <div className="MoneyInfo" style={{color: '#717171', fontSize: 14, fontFamily: 'Roboto', fontWeight: '400',  wordWrap: 'break-word'}}>{money}</div>
                    </div>
                </div>
            </div>
        </div>
        {/* Edit Button */}
        <Link to="/DetailEdit">
        <div className="EditButton" style={{ width: 470, height: 45, left: '50%', bottom: 20, position: 'absolute', transform: 'translateX(-50%)' }}>
            <div className="Rectangle4" style={{ width: '50%', height: '100%', position: 'absolute', background: '#35CCED', borderRadius: 10 }}></div>
            <div className="Edit" style={{ left: '95px', bottom: '50%', position: 'absolute', width: '100%', transform: 'translateY(50%)', color: 'white', fontSize: 24, fontFamily: 'Roboto', fontWeight: '900', wordWrap: 'break-word' }}>Edit </div>
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
          {!isLogin && (
                <Link to ="/Login">
                <img className="UserIcon" style={{width: 45, height: 68}} src={user} alt ="UserIcon"/>      
                </Link>)}

                {isLogin && (
                <div>
                  <img className="Logout" style={{width: 45, height: 68}} src={logout} alt ="ExitIcon" onClick={() => handleLogout(true)}/>      
                </div>
                )}
          </div>

      </div>
    </div>
  )
}

export default UserInfo