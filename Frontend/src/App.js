import React, { useState, useEffect } from 'react';
import axios from 'axios';

import './App.css';

const App = () => {
    const [file, setFile] = useState(null);
    const [userList, setUserList] = useState([]);
    const [comment, setComment] = useState('');
    const [expandedId, setExpandedId] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = async () => {
        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await axios.post('http://89.232.170.158:8000', formData, {
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            const newUsers = response.data;
            setUserList(newUsers);
        } catch (error) {
            console.error('Ошибка при загрузке файла:', error);
        }
    };

    const handleButtonClick = async (userId, value) => {
        try {
            const response = await axios.post('http://89.232.170.158:8000', {
                id: userId,
                answer: value,
                comment: comment,
            });

            const updatedUsers = response.data;
            setUserList(updatedUsers);
        } catch (error) {
            console.error('Ошибка при отправке данных:', error);
        }
    };

    const handleExport = async () => {
        try {
            const response = await axios.get('http://89.232.170.158:8000', {
                responseType: 'blob',
            });

            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'user_data.json');
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } catch (error) {
            console.error('Ошибка при экспорте данных:', error);
        }
    };

    const handleExpand = (userId) => {
        setExpandedId(expandedId === userId ? null : userId);
    };

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get('http://89.232.170.158:8000');
                setUserList(response.data);
            } catch (error) {
                console.error('Ошибка при получении данных:', error);
            }
        };

        fetchData();
    }, []);

    useEffect(() => {
        // Пример начальных данных:
        const initialUsers = [
            {
                id: 1,
                answer: "Проверка данных",
                comment: '',
            },
            {
                id: 2,
                answer: "Проверка БД",
                comment: '',
            },
        ];
        setUserList(initialUsers);
    }, []);


    return (
        <div className="app-container">
            <header className="Header-bar">
                <div className="Header-text">
                    Веб - сервис по генерации маркетинговых предложений
                </div>
            </header>
            <div className="file-upload-container">
                <input type="file" onChange={handleFileChange}/>
                <button onClick={handleUpload}>Загрузить файл</button>
            </div>

            <div className="user-list-container">
                {userList.map((user) => (
                    <div key={user.id} className="user-item">
                        <p>ID пользователя: {user.id}</p>
                        <div className="answer-container">
                            <p className="answer-label">Ответ:</p>
                            <div
                                className={`answer-content ${expandedId === user.id ? 'expanded' : ''}`}
                                onClick={() => handleExpand(user.id)}
                            >
                                <p>{user.answer}</p>
                            </div>
                        </div>
                        <p className="comment">Комментарий: {user.comment}</p>
                        <div className="button-container">
                            <button onClick={() => handleButtonClick(user.id, 0)}>Неправильно</button>
                            <button onClick={() => handleButtonClick(user.id, 1)}>Правильно</button>
                            <input
                                type="text"
                                placeholder="Введите комментарий"
                                value={comment}
                                onChange={(e) => setComment(e.target.value)}
                            />
                        </div>
                    </div>
                ))}
            </div>
            <button className="export-button" onClick={handleExport}>
                Экспорт
            </button>
        </div>
    );
};

export default App;