import './App.css';


import mainchat from './assets/mainchat.png';

 import addBtn from './assets/add-30.png';
 import homeIcon from './assets/home.svg';
 import chatimg from './assets/chat.svg';
 import searchimg from './assets/search.svg';
 import sendBtn from './assets/send.svg';
 import userIcon from './assets/user.svg';
 import gptImgLogo from './assets/chatgptLogo.svg';
 import editIcon from './assets/edit.svg';
 import {useEffect, useRef,useState} from 'react';

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
      {/* side bar */}
      <div className="sidebar">
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
        <div className = "lowerSide">
          {/* menu - onClick send to each pages */}
          <div className='listItems'><img src= {homeIcon} alt ="" className='listItemsImg'/>Home</div>
          <div className='listItems'><img src= {chatimg} alt ="" className='listItemsImg'/>Chat</div>
          <div className='listItems'><img src= {searchimg} alt ="" className='listItemsImg'/>Search</div>
        </div>
      </div>

      {/* main */}
      <div className="main">
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

