import { useEffect, useState } from "react";
import "./App.css";

function ChatItem({ message, isUser }) {
    return (
        <div
            className={`${
                isUser ? "justify-end" : "justify-start"
            } w-full flex items-center text-left`}
        >
            <div
                className={`${
                    isUser ? "bg-blue-400 text-white" : "bg-slate-200 text-black"
                } rounded-md p-2 m-2`}
            >
                {message}
            </div>
        </div>
    );
}

function App() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [sender, setSender] = useState("user");

    useEffect(() => {
        // Generate a random 8 character ID for the user
        const id = Math.random().toString(36).substring(2, 10);

        setSender(id);

        console.log("Current user id: " + id);
    }, []);

    // Send message when user presses enter
    const handleKeyPress = (e) => {
        if (e.key === "Enter") {
            sendMessage();
        }
    };

    // When user sends a message, add it to the messages array
    // and then clear the input box
    const sendMessage = async () => {
        const userMessage = { message: input, isUser: true };

        setMessages([...messages, userMessage]);

        setInput("");

        // Query from server
        const response = await fetch(
            "https://hkchat.michaelzhao.xyz/webhooks/rest/webhook",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    sender,
                    message: input,
                }),
            }
        );

        const data = await response.json();

        // Save bot messages
        const botMessages = data.map((message) => ({
            message: message.text,
            isUser: false,
        }));
        setMessages([...messages, userMessage, ...botMessages]);
    };
    return (
        <div className="App">
            {/* Make an interface for a chatbot */}
            <div className="fixed top-0 left-0 h-20 w-full flex items-center justify-center">
                <h1 className="text-4xl font-bold">Hollow Knight Chatbot</h1>
            </div>

            {/* Make a chatbox */}
            <div className="fixed bottom-0 left-0 h-22 p-4 w-full flex items-center">
                <input
                    className="h-full flex-grow border-slate-400 focus:border-blue-400 border-2 rounded-sm outline-none duration-100 p-2"
                    type="text"
                    placeholder="Type a message..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyPress}
                />
                <button
                    className="ml-4 h-10 w-20 bg-blue-400 text-white font-bold rounded-sm"
                    onClick={sendMessage}
                >
                    Send
                </button>
            </div>

            {/* Add dummy items for top */}
            <div className="h-20 w-full flex items-center justify-center"></div>

            {/* Make main chat history area */}
            <div className="overflow-auto flex flex-col-reverse h-[83vh] w-full">
                <div className="flex flex-col">
                    {messages.map((message, i) => (
                        <ChatItem
                            key={i}
                            message={message.message}
                            isUser={message.isUser}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
}

export default App;
