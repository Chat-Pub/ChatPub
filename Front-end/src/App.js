 import './App.css';
 import mainchat from './assets/mainchat.png';
 import addBtn from './assets/add-30.png';
 import msgIcon from './assets/message.svg';
 import home from './assets/home.png';
 import chatimg from './assets/chat.png';
 import searchimg from './assets/search.png';
 import sendBtn from './assets/send.svg';
 import userIcon from './assets/user.svg';
 import gptImgLogo from './assets/chatgptLogo.svg';
 import {sendMsgToOpenAI} from './openai';
 import {useEffect, useRef,useState} from 'react';



function App() {
  const msgEnd = useRef(null);
  

  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    {
    text: 'Hi, I am ChatPub. I am here to help you with your queries.',
    isBot : true,
  }
]);

// auto scroll
  useEffect(() => {
    msgEnd.current.scrollIntoView({behavior: 'smooth'});
  }, [messages])


  // chatgpt message
  const handleSend = async () => {
    const text = input;
    setInput('');
    setMessages([
      ...messages, 
      {text, isBot : false},
      {text: 'Loading...', isBot : true}
    ])

    //back이랑 소통해서 answer, reference 받아오기
    
    // const res = await sendMsgToOpenAI(text)
    // setMessages([
    //   ...messages, 
    //   {text: input, isBot : false},
    //   {text: res, isBot : true}
    // ])

    // console.log(res)
  }

  // scroll to bottom
  const handleEnter = (e) => {
    if(e.key === 'Enter'){
      handleSend();
    }
   }

  //qeury, auto question and answer
  const handleQuery = async (e) => {
    const text = e.target.value;
    setMessages([
      ...messages, 
      {text, isBot : false}
    ])

    const res = await sendMsgToOpenAI(text)
    setMessages([
      ...messages, 
      {text: input, isBot : false},
      {text: res, isBot : true}
    ])
  }

  return (
    <div className="App">
      {/* side bar */}
      <div className="sidebar">
        <div className = "upperSide">
          <div className='upperSideTop'><img src = {mainchat} alt ="Logo" className='logo'/><span className='brand'>Chat Pub</span></div>
          <button className='midBtn' onClick={()=>{window.location.reload()}}><img src ={addBtn} alt ='' className='addBtn'/>New Chat</button>
          <div className='upperSideBottom'>
            <button className='query'><img src ={msgIcon} alt ='Query'onClick={handleQuery} value = {"how to use an API?"}/>What is Programming?</button>
            <button className='query'><img src ={msgIcon} alt ='Query' onClick={handleQuery} value ={'what is Programming?'}/>What is Programming?</button>
          </div>
        </div>
        <div className = "lowerSide">
          {/* menu - onClick send to each pages */}
          <div className='listItems'><img src= {home} alt ="" className='listItemsImg'/>Home</div>
          <div className='listItems'><img src= {chatimg} alt ="" className='listItemsImg'/>Chat</div>
          <div className='listItems'><img src= {searchimg} alt ="" className='listItemsImg'/>Search</div>
        </div>
      </div>

      {/* main */}
      <div className="main">
        <div className='chats'>
          {/* <div className='chat'> */}
            {messages.map((message, i) => 
              <div key ={i} className={message.isBot?'chat bot':"chat"}>
                <img className='chatImg' src = {message.isBot?gptImgLogo:userIcon} alt ="" /> <p className='txt'>{message.text}</p>
              </div>
            )}
            <div ref={msgEnd}/>
          {/* </div> */}
        </div>

        <div className='chatFooter'>
          <div className='inp'>
            <input type ="text" placeholder='Send a Message ...' value = {input} onKeyDown = {handleEnter} onChange={(e)=> {setInput(e.target.value)}} />
            <button className='send' onClick={handleSend}><img src ={sendBtn} alt ="Send"/></button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
