import React from 'react'; 
import ReactDOM from 'react-dom/client';   
import { BrowserRouter, Routes, Route } from 'react-router-dom';



import Home from './Home'; 
import Login from './Login';
import CreateAccount from './Signup';
import App from './App';
import Search from './Search';
import Detail from './Detail';
import DetailEdit from './DetailEdit';


const root = ReactDOM.createRoot(document.getElementById('root'));
// root.render(<App/>);
root.render(
    <BrowserRouter>
        <Routes>
            <Route path="/" element={<Home/>} />
            <Route path="login" element={<Login/>} />
            <Route path="signup" element={<CreateAccount/>} />
            <Route path="App" element={<App/>} />
            <Route path="HomePage" element={<Home/>} />
            <Route path="Search" element={<Search/>}/>
            <Route path="Detail" element={<Detail/>}/>
            <Route path="DetailEdit" element={<DetailEdit/>}/>
        </Routes>
    </BrowserRouter>
    // <Home/>
);


