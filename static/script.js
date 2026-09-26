let currentChatId = null;

const chatList = document.getElementById("chatList");
const input = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const messages = document.querySelector(".messages");
const suggestionButtons = document.querySelectorAll(".suggestions button");

let isSending = false;


// =====================================================
// SEND MESSAGE
// =====================================================

async function sendMessage(customMessage = null) {

    const message = customMessage || input.value.trim();

    if (message === "" || isSending) {
        return;
    }

    isSending = true;
    sendButton.disabled = true;

    showUserMessage(message);

    input.value = "";

    messages.scrollTop = messages.scrollHeight;


    const typingMessage = document.createElement("div");

    typingMessage.classList.add("message");
    typingMessage.id = "typingMessage";

    typingMessage.innerHTML = `
        <div class="avatar">
            🤖
        </div>

        <div class="message-content">
            <div class="message-name">
                Arnav AI
            </div>

            <div class="bubble">
                <span>Thinking...</span>
            </div>
        </div>
    `;

    messages.appendChild(typingMessage);

    messages.scrollTop = messages.scrollHeight;


    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message,
                chat_id: currentChatId
            })
        });


        if (!response.ok) {

            const errorText = await response.text();

            console.error(
                "Chat API Error:",
                response.status,
                errorText
            );

            removeTypingMessage();

            showBotMessage(
                "Sorry, something went wrong while connecting to the AI server."
            );

            return;
        }


        const data = await response.json();


        if (data.chat_id) {

            currentChatId = data.chat_id;

        }


        removeTypingMessage();


        if (data.reply) {

            showBotMessage(data.reply);

        }
        else {

            showBotMessage(
                "I received your message, but I don't have a response right now."
            );

        }


        loadChats();


    }
    catch (error) {

        console.error(
            "Connection error:",
            error
        );

        removeTypingMessage();

        showBotMessage(
            "Unable to connect to Arnav AI. Please try again."
        );

    }
    finally {

        isSending = false;

        sendButton.disabled = false;

        input.focus();

    }
}


// =====================================================
// SHOW USER MESSAGE
// =====================================================

function showUserMessage(message) {

    const userMessage =
        document.createElement("div");

    userMessage.classList.add("message");

    userMessage.innerHTML = `
        <div class="avatar">
            👤
        </div>

        <div class="message-content">

            <div class="message-name">
                You
            </div>

            <div class="bubble">
                ${escapeHTML(message)}
            </div>

        </div>
    `;

    messages.appendChild(userMessage);
}


// =====================================================
// SHOW BOT MESSAGE
// =====================================================

function showBotMessage(reply) {

    const botMessage =
        document.createElement("div");

    botMessage.classList.add("message");

    botMessage.innerHTML = `
        <div class="avatar">
            🤖
        </div>

        <div class="message-content">

            <div class="message-name">
                Arnav AI
            </div>

            <div class="bubble">
                ${DOMPurify.sanitize(marked.parse(reply))}
            </div>

        </div>
    `;

    messages.appendChild(botMessage);

    if (window.MathJax) {
        MathJax.typesetPromise([botMessage]);
    }

    messages.scrollTop =
        messages.scrollHeight;
}


// =====================================================
// REMOVE TYPING MESSAGE
// =====================================================

function removeTypingMessage() {

    const typingMessage =
        document.getElementById("typingMessage");

    if (typingMessage) {
        typingMessage.remove();
    }
}


// =====================================================
// ESCAPE HTML
// =====================================================

function escapeHTML(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


// =====================================================
// CLEAR MESSAGES
// =====================================================

function clearMessages() {

    messages.innerHTML = "";

    messages.scrollTop = 0;
}


// =====================================================
// GET DATE GROUP
// =====================================================

function getDateGroup(dateString) {

    const chatDate =
        new Date(dateString.replace(" ", "T"));

    const now =
        new Date();

    const today =
        new Date(
            now.getFullYear(),
            now.getMonth(),
            now.getDate()
        );

    const yesterday =
        new Date(today);

    yesterday.setDate(
        yesterday.getDate() - 1
    );


    const previousSevenDays =
        new Date(today);

    previousSevenDays.setDate(
        previousSevenDays.getDate() - 7
    );


    const date =
        new Date(
            chatDate.getFullYear(),
            chatDate.getMonth(),
            chatDate.getDate()
        );


    if (date.getTime() === today.getTime()) {
        return "Today";
    }


    if (date.getTime() === yesterday.getTime()) {
        return "Yesterday";
    }


    if (date >= previousSevenDays) {
        return "Previous 7 Days";
    }


    return "Older";
}


// =====================================================
// CREATE DATE GROUP
// =====================================================

function createDateGroup(title) {

    const group =
        document.createElement("div");

    group.classList.add("chat-date-group");

    group.textContent = title;

    return group;
}


// =====================================================
// LOAD ALL CHATS
// =====================================================

async function loadChats() {

    try {

        const response =
            await fetch("/chats");

        const data =
            await response.json();

        chatList.innerHTML = "";


        let currentGroup = null;


        data.chats.forEach(function(chat) {

            const groupName =
                chat.date_group ||
                getDateGroup(chat.created_at);


            if (groupName !== currentGroup) {

                currentGroup = groupName;

                chatList.appendChild(
                    createDateGroup(groupName)
                );

            }


            const chatItem =
                document.createElement("div");

            chatItem.classList.add("chat-item");

            chatItem.dataset.chatId =
                chat.id;


            const title =
                document.createElement("span");

            title.classList.add("chat-title");

            title.textContent =
                chat.title;


            const actions =
                document.createElement("div");

            actions.classList.add("chat-actions");


            const renameButton =
                document.createElement("button");

            renameButton.classList.add(
                "rename-chat"
            );

            renameButton.textContent = "✏️";

            renameButton.title =
                "Rename chat";


            const deleteButton =
                document.createElement("button");

            deleteButton.classList.add(
                "delete-chat"
            );

            deleteButton.textContent = "🗑️";

            deleteButton.title =
                "Delete chat";


            actions.appendChild(renameButton);

            actions.appendChild(deleteButton);


            chatItem.appendChild(title);

            chatItem.appendChild(actions);


            if (
                currentChatId &&
                Number(currentChatId) ===
                Number(chat.id)
            ) {

                chatItem.classList.add(
                    "selected"
                );

            }


            chatItem.addEventListener(
                "click",
                function(event) {

                    if (
                        event.target.closest(
                            ".chat-actions"
                        )
                    ) {
                        return;
                    }

                    openChat(chat.id);

                }
            );


            renameButton.addEventListener(
                "click",
                function(event) {

                    event.stopPropagation();

                    renameChat(chat.id);

                }
            );


            deleteButton.addEventListener(
                "click",
                function(event) {

                    event.stopPropagation();

                    deleteChat(chat.id);

                }
            );


            chatList.appendChild(
                chatItem
            );

        });


    }
    catch (error) {

        console.error(
            "Loading chats error:",
            error
        );

    }
}


// =====================================================
// OPEN OLD CHAT
// =====================================================

async function openChat(chatId) {

    try {

        const response =
            await fetch(
                `/chat/${chatId}`
            );


        if (!response.ok) {
            return;
        }


        const data =
            await response.json();


        currentChatId =
            chatId;


        clearMessages();


        data.messages.forEach(
            function(chat) {

                showUserMessage(
                    chat.user_message
                );

                showBotMessage(
                    chat.ai_reply
                );

            }
        );


        loadChats();


        messages.scrollTop =
            messages.scrollHeight;

        input.focus();


    }
    catch (error) {

        console.error(
            "Opening chat error:",
            error
        );

    }
}


// =====================================================
// RENAME CHAT
// =====================================================

async function renameChat(chatId) {

    const newTitle =
        prompt(
            "Enter new chat name:"
        );


    if (
        newTitle === null ||
        newTitle.trim() === ""
    ) {
        return;
    }


    try {

        const response =
            await fetch(
                `/chat/${chatId}/rename`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        title:
                            newTitle.trim()
                    })
                }
            );


        if (!response.ok) {

            alert(
                "Unable to rename chat."
            );

            return;

        }


        loadChats();


    }
    catch (error) {

        console.error(
            "Rename error:",
            error
        );

    }
}


// =====================================================
// DELETE CHAT
// =====================================================

async function deleteChat(chatId) {

    const confirmed =
        confirm(
            "Are you sure you want to delete this chat?"
        );


    if (!confirmed) {
        return;
    }


    try {

        const response =
            await fetch(
                `/chat/${chatId}`,
                {
                    method: "DELETE"
                }
            );


        if (!response.ok) {

            alert(
                "Unable to delete chat."
            );

            return;

        }


        if (
            currentChatId &&
            Number(currentChatId) ===
            Number(chatId)
        ) {

            currentChatId = null;

            clearMessages();

        }


        loadChats();


    }
    catch (error) {

        console.error(
            "Delete error:",
            error
        );

    }
}


// =====================================================
// SEND BUTTON
// =====================================================

sendButton.addEventListener(
    "click",
    function() {

        sendMessage();

    }
);


// =====================================================
// ENTER KEY
// =====================================================

input.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            event.preventDefault();

            sendMessage();

        }

    }
);


// =====================================================
// SUGGESTION BUTTONS
// =====================================================

suggestionButtons.forEach(
    function(button) {

        button.addEventListener(
            "click",
            function() {

                let question =
                    button.textContent.trim();


                question =
                    question.replace(
                        /^[^\w]+/u,
                        ""
                    ).trim();


                if (
                    question.includes(
                        "Favourite sport"
                    )
                ) {

                    question =
                        "What is Arnav's favourite sport?";

                }

                else if (
                    question.includes(
                        "What does Arnav study"
                    )
                ) {

                    question =
                        "What does Arnav study?";

                }

                else if (
                    question.includes(
                        "What are his hobbies"
                    )
                ) {

                    question =
                        "What are Arnav's hobbies?";

                }

                else if (
                    question.includes(
                        "What is his goal"
                    )
                ) {

                    question =
                        "What is Arnav's goal?";

                }


                sendMessage(question);

            }
        );

    }
);


// =====================================================
// NEW CHAT
// =====================================================

const newChatButton =
    document.querySelector(".new-chat");


if (newChatButton) {

    newChatButton.addEventListener(
        "click",
        function() {

            currentChatId = null;

            clearMessages();

            input.value = "";

            input.focus();

            loadChats();

        }
    );

}


// =====================================================
// INITIAL LOAD
// =====================================================

loadChats();

currentChatId = null;

clearMessages();

input.focus();