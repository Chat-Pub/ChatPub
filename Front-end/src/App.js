import './App.css';

import govmark from './assets/gov.png';
import chatmenu from './assets/chat.svg';
import searchmenu from './assets/search.svg';
import homemenu from './assets/home.svg';
import user from './assets/user.svg';
import mainchat from './assets/mainchat.png';

 import addBtn from './assets/add-30.png';
 import sendBtn from './assets/send.svg';
 import userIcon from './assets/user.svg';
 import gptImgLogo from './assets/chatgptLogo.svg';
 import editIcon from './assets/edit.svg';
 import {useEffect, useRef,useState} from 'react';
 import { Link } from 'react-router-dom';

 var selectedFolderId = 0;

function App() {
  const msgEnd = useRef(null);
  

  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    {
    text: 'Hi, I am ChatPub. I am here to help you with your queries.',
    isBot : true,
  }
]);

  const [conditionFolder, setConditionFolder] = useState(0);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newChatFolderName, setNewChatFolderName] = useState('');
  const [isModalOpen2, setIsModalOpen2] = useState(false);
  const [editFolderName, setEditFolderName] = useState('');
  
  //folder id fetch
  const [folders, setFolders] = useState([]);

  //folder data fetch
  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/folder/list', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    }).then(response => response.json())
      .then(data =>  {
        const extractedFolders = data.folder_list.map(({ id, folder_name }) => ({ id, folder_name }));
        setFolders(extractedFolders)
      })
      .catch(error => console.error('Error fetching folders:', error));
    // Fetch folder data from FastAPI backend
  }, [conditionFolder]);

  //Folder create
  const handleNewChatClick = () => {
    setIsModalOpen(true);
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
  };

  async function handleSaveFolder() {
    // Here you can send the newChatFolderName to your database or perform any other action
    console.log('Folder name saved:', newChatFolderName);
    try {
      await fetch('http://127.0.0.1:8000/api/folder/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          authorization: `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({
          folder_name: newChatFolderName,
        }),
      });
      setConditionFolder(conditionFolder + 1);
    setIsModalOpen(false);
  }
    catch (error) {
      console.error('Error during API call:', error);
      // Handle error, update state, show an error message, etc.
    }
  };

  //Folder Name Edit Modal
  const handleEditFolderClick = (folderName, folderId) => {
    setEditFolderName(folderName);
    selectedFolderId = folderId;
    setIsModalOpen2(true);
  };

  const handleEditFolderClose = () => {
    setIsModalOpen2(false);
  };

    const handleEditFolder = async () => {
    // Here you can send the newChatFolderName to your database or perform any other action
    console.log('Folder name Edited:', editFolderName, selectedFolderId);
    try {
      await fetch('http://127.0.0.1:8000/api/folder/update', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          authorization: `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({
          folder_name: editFolderName,
          folder_id: selectedFolderId,
        }),
      });
      setConditionFolder(conditionFolder + 1);
    setIsModalOpen2(false);
  }
    catch (error) {
      console.error('Error during API call:', error);
      // Handle error, update state, show an error message, etc.
    }
  };

// auto scroll
  // useEffect(() => {
  // msgEnd.current.scrollIntoView({behavior: 'smooth'});
  // }, [messages])


  // Call Chat GPT 
  const handleChatRoom = async () => {
    console.log('Folder id handle chat room:', selectedFolderId);
    try {
      await fetch('http://127.0.0.1:8000/api/folder_content/list',{
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          authorization: `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({
          folder_id: selectedFolderId,
        }),
      })
      .then(response => response.json())
      .then(data =>  {
        console.log('data:', data)
        if (data.total === 0) {
          setMessages([
            {
              text: 'Hi, I am ChatPub. I am here to help you with your queries.',
              isBot : true,
            }
          ]);
          return;
        }

        const extractedMessages = data.folder_content_list.map(({ question, answer, references }) => ({ question, answer, references }));
        console.log('extractedMessages:', extractedMessages)
          let messagesCluster = [];

        extractedMessages.forEach((message) => {
           messagesCluster = [
            ...messagesCluster, 
            {text: message.question, isBot : false},
            {text: message.answer, isBot : true},
            {text: message.references, isBot : true}
          ]
        })
        setMessages(messagesCluster)
        
      })
    } catch (error) {
        console.error('Error during API call:', error);
    }
    
  }

  

  const handleRoomId = (folderId) => {
    console.log('Folder id room id :', folderId);
    selectedFolderId = folderId;
    handleChatRoom();
    // console.log('Folder id:', selectedFolderId); 
    // handleChatRoom();
  }
  
  // scroll to bottom
  const handleEnter = (e) => {
    if(e.key === 'Enter'){
      handleSend();
    }
  }
  
  // chatgpt message
  const handleSend = async () => {
    const text = input;
    setInput('');
    setMessages([
      ...messages, 
      {text, isBot : false},
      {text: 'Loading...', isBot : true}
    ])
      console.log('Folder id handle send:', selectedFolderId);
      try {
      await fetch('http://127.0.0.1:8000/api/folder_content/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          authorization: `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({
          folder_id: selectedFolderId,
          question: text,
        }),
      })
      .then(response => response.json())
      .then(data =>  {
        setMessages([
          ...messages, 
          {text, isBot : false},
          {text: data.answer, isBot : true},
          {text: data.references, isBot : true}
        ])

      });
      
    } catch (error) {
      console.error('Error during API call:', error);
      // Handle error, update state, show an error message, etc.
    }
  }
  
 

  return (
    <div className="App">
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
      {/* side bar */}
      <div className="Chat Menu" style={{marginLeft : '65px'}}>
        <div className = "upperSide">
          <div className='upperSideTop'><img src = {mainchat} alt ="Logo" className='logo'/><span className='brand'>Chat Pub</span></div>
          <div>
            <button className='midBtn' onClick={handleNewChatClick}><img src ={addBtn} alt ='' className='addBtn'/>
              New Chat
            </button>

            {isModalOpen && (
              <div className="modal">
                <div className="modal-content">
                  <span className="close" onClick={handleModalClose}>
                    &times;
                  </span>
                  <label>
                    Folder Name:
                    <input
                      type="text"
                      value={newChatFolderName}
                      onChange={(e) => setNewChatFolderName(e.target.value)}
                    />
                  </label>
                  <button onClick={handleSaveFolder}>Save Folder</button>
                </div>
              </div>
            )}
          </div>
          <div>
            {folders.map(folder => (
                <div key={folder.id} className='folderlist'>
                  
                  <img src ={editIcon} onClick={() => handleEditFolderClick(folder.folder_name,folder.id)} alt ='' className='editBtn'/>
                  {isModalOpen2 && (
                    <div className="modal">
                      <div className="modal-content">
                        <span className="close" onClick={() => handleEditFolderClose}>
                          &times;
                        </span>
                        <label>
                          Folder Name:
                          <input
                            type="text"
                            value={editFolderName}
                            onChange={(e) => setEditFolderName(e.target.value)}
                          />
                        </label>
                        <button onClick={handleEditFolder}>Edit Folder Name</button>
                      </div>
                    </div>
                  )}
                  <button className="folderBtn" onClick={()=>{handleRoomId(folder.id)}}>
                    <h3>{folder.folder_name}</h3>
                  </button>
                 
                </div> 
              ))}
          </div>
          
          
          
       </div>
        <div className = "lowerSide"></div>
      </div>

      {/* main */}
      <div className="main" style={{marginLeft:'20px'}}>
        <div className='chats'>
          {messages.map((message, i) => 
            <div key ={i} className={message.isBot?'chat bot':"chat"}>
              <img className='chatImg' src = {message.isBot?gptImgLogo:userIcon} alt ="" /> <p className='txt'>{message.text}</p>
            </div>
          )}
          <div ref={msgEnd}/>
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

