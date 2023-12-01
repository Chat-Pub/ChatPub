import React from 'react'
import './App.css';


function Home() {
  return (
    <div className="HomePage" style={{width: 1440, height: 1024, position: 'relative', background: 'white'}}>
          <div className="HomeFrame" style={{width: 1440, height: 1024, left: 0, top: 0, position: 'absolute'}}>
            <div className="MainFrame" style={{width: 800, height: 675, left: 381, top: 175, position: 'absolute', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start', gap: 64, display: 'inline-flex'}}>
                <div className="ChatPubTitle" style={{height: 219, flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'center', gap: 12, display: 'flex'}}>

                </div>

            </div>


        </div>

    </div>


  );
}

export default Home;