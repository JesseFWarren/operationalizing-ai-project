import React, { useState, useEffect } from "react";
import axios from "axios";
import "./styles.css";

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [image, setImage] = useState(null);
  const [isTyping, setIsTyping] = useState(false);

  const BACKEND_URL = "https://healthlivechatbackend.onrender.com";
  const API_KEY = "secretkey123"; 

  useEffect(() => {
    setMessages([
      { text: "Welcome to Health Live Chat! How can I assist you today?", sender: "bot" }
    ]);
  }, []);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) setImage(file);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim() && !image) return;

    const userMessage = {
      text: question || "[Image submitted]",
      sender: "user",
      image: image ? URL.createObjectURL(image) : null
    };
    setMessages((prev) => [...prev, userMessage]);
    setQuestion("");
    setImage(null);
    setIsTyping(true);

    try {
      let res;
      if (image) {
        const formData = new FormData();
        formData.append("query", question);
        formData.append("image", image);

        res = await axios.post(`${BACKEND_URL}/ask_image`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            "x-api-key": API_KEY
          }
        });
      } else {
        res = await axios.post(`${BACKEND_URL}/ask`, { query: question }, {
          headers: {
            "Content-Type": "application/json",
            "x-api-key": API_KEY
          }
        });
      }

      const botMessage = { text: res.data.response, sender: "bot" };
      setTimeout(() => {
        setMessages((prev) => [...prev, botMessage]);
        setIsTyping(false);
      }, 1500);
    } catch (error) {
      console.error("Error:", error);
      setIsTyping(false);
      setMessages((prev) => [
        ...prev,
        { text: "Error fetching response. Try again later.", sender: "bot" }
      ]);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.image && <img src={msg.image} alt="Uploaded" className="uploaded-img" />}
            {msg.text}
          </div>
        ))}
        {isTyping && <div className="message bot typing">...</div>}
      </div>

      <form className="chat-form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Describe your symptoms..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <input type="file" accept="image/*" onChange={handleImageChange} />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default Chatbot;
