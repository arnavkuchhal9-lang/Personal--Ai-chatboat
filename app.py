from flask import Flask, render_template, request, jsonify
from google import genai
from datetime import datetime
from zoneinfo import ZoneInfo
import sqlite3
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_connection():
    return sqlite3.connect("database/chatboad.db")


# =====================================================
# PERSONAL INFORMATION
# =====================================================

def get_info(information):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT value FROM personal_info WHERE information = ?",
        (information,)
    )

    results = cursor.fetchall()

    connection.close()

    if results:
        return [row[0] for row in results]

    return []


def find_information(message):

    message = message.lower()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT information, keywords FROM personal_info"
    )

    rows = cursor.fetchall()

    connection.close()

    for information, keywords in rows:

        if keywords:

            keyword_list = keywords.lower().split(",")

            for keyword in keyword_list:

                if keyword.strip() in message:

                    return information

    return None


# =====================================================
# SAVE CHAT MESSAGE
# =====================================================

def save_chat(user_message, ai_reply, chat_id):

    connection = get_connection()
    cursor = connection.cursor()

    current_time = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        INSERT INTO chat_history
        (user_message, ai_reply, created_at, chat_id)
        VALUES (?, ?, ?, ?)
        """,
        (
            user_message,
            ai_reply,
            current_time,
            chat_id
        )
    )

    connection.commit()
    connection.close()


# =====================================================
# GET ONE CHAT HISTORY
# =====================================================

def get_chat_history(chat_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT user_message, ai_reply, created_at
        FROM chat_history
        WHERE chat_id = ?
        ORDER BY id
        """,
        (chat_id,)
    )

    results = cursor.fetchall()

    connection.close()

    return results


# =====================================================
# GET TODAY HISTORY
# =====================================================

def get_today_history():

    connection = get_connection()
    cursor = connection.cursor()

    today = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime("%Y-%m-%d")

    cursor.execute(
        """
        SELECT user_message, ai_reply, created_at
        FROM chat_history
        WHERE DATE(created_at) = ?
        ORDER BY id
        """,
        (today,)
    )

    results = cursor.fetchall()

    connection.close()

    return results


# =====================================================
# HISTORY QUESTION
# =====================================================

def is_history_question(message):

    message = message.lower().strip()

    history_phrases = [

        "aaj humari kya baat hui",
        "aaj hamari kya baat hui",
        "aaj hameri kya baat hui",
        "aaj kya baat hui",
        "aaj kya baatein hui",
        "aaj ki baat",
        "aaj ki baatein",
        "aaj ki chat",
        "aaj ki chats",
        "aaj humne kya baat ki",
        "aaj humne kya baatein ki",
        "aaj hamne kya baat ki",
        "aaj hamne kya baatein ki",

        "what did we talk about today",
        "what did we talk today",
        "what did i ask today",
        "what questions did i ask today",

        "today's chat",
        "todays chat",
        "today chat",
        "show today's chats",
        "show todays chats",
        "show today's conversation",
        "show todays conversation"
    ]

    for phrase in history_phrases:

        if phrase in message:
            return True

    return False


# =====================================================
# HOME
# =====================================================

@app.route("/")
def home():

    return render_template("index.html")


# =====================================================
# CREATE NEW CHAT
# =====================================================

@app.route("/new-chat", methods=["POST"])
def new_chat():

    connection = get_connection()
    cursor = connection.cursor()

    current_time = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        INSERT INTO chat_sessions
        (title, created_at)
        VALUES (?, ?)
        """,
        (
            "New Chat",
            current_time
        )
    )

    chat_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return jsonify({
        "chat_id": chat_id,
        "title": "New Chat"
    })


# =====================================================
# GET ALL CHAT SESSIONS
# =====================================================

@app.route("/chats", methods=["GET"])
def chats():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT cs.id, cs.title, cs.created_at
        FROM chat_sessions cs
        WHERE EXISTS (
            SELECT 1
            FROM chat_history ch
            WHERE ch.chat_id = cs.id
        )
        ORDER BY cs.id DESC
        """
    )

    results = cursor.fetchall()

    connection.close()

    chats = []

    today = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime("%Y-%m-%d")

    for chat_id, title, created_at in results:

        if created_at:

            chat_date = created_at[:10]

            if chat_date == today:

                date_group = "Today"

            else:

                try:

                    chat_datetime = datetime.strptime(
                        chat_date,
                        "%Y-%m-%d"
                    )

                    today_datetime = datetime.now(
                        ZoneInfo("Asia/Kolkata")
                    ).replace(
                        hour=0,
                        minute=0,
                        second=0,
                        microsecond=0
                    ).replace(
                        tzinfo=None
                    )

                    difference = (
                        today_datetime - chat_datetime
                    ).days

                    if difference == 1:

                        date_group = "Yesterday"

                    elif 1 < difference <= 7:

                        date_group = "Previous 7 Days"

                    else:

                        date_group = "Older"

                except:

                    date_group = "Older"

        else:

            date_group = "Older"

        chats.append({
            "id": chat_id,
            "title": title,
            "created_at": created_at,
            "date_group": date_group
        })

    return jsonify({
        "chats": chats
    })


# =====================================================
# GET ONE CHAT
# =====================================================

@app.route("/chat/<int:chat_id>", methods=["GET"])
def load_chat(chat_id):

    history = get_chat_history(chat_id)

    messages = []

    for user_message, ai_reply, created_at in history:

        messages.append({
            "user_message": user_message,
            "ai_reply": ai_reply,
            "created_at": created_at
        })

    return jsonify({
        "messages": messages
    })


# =====================================================
# RENAME CHAT
# =====================================================

@app.route("/chat/<int:chat_id>/rename", methods=["POST"])
def rename_chat(chat_id):

    data = request.get_json()

    title = data.get("title", "").strip()

    if title == "":

        return jsonify({
            "error": "Title cannot be empty"
        }), 400

    if len(title) > 50:

        title = title[:50]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE chat_sessions
        SET title = ?
        WHERE id = ?
        """,
        (
            title,
            chat_id
        )
    )

    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "title": title
    })


# =====================================================
# DELETE CHAT
# =====================================================

@app.route("/chat/<int:chat_id>", methods=["DELETE"])
def delete_chat(chat_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM chat_history
        WHERE chat_id = ?
        """,
        (chat_id,)
    )

    cursor.execute(
        """
        DELETE FROM chat_sessions
        WHERE id = ?
        """,
        (chat_id,)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "success": True
    })


# =====================================================
# SEND MESSAGE
# =====================================================

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    message = data["message"]

    chat_id = data.get("chat_id")


    # =================================================
    # CREATE CHAT ONLY WHEN FIRST MESSAGE IS SENT
    # =================================================

    if not chat_id:

        connection = get_connection()
        cursor = connection.cursor()

        current_time = datetime.now(
            ZoneInfo("Asia/Kolkata")
        ).strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            """
            INSERT INTO chat_sessions
            (title, created_at)
            VALUES (?, ?)
            """,
            (
                "New Chat",
                current_time
            )
        )

        chat_id = cursor.lastrowid

        connection.commit()
        connection.close()


    # =================================================
    # TODAY HISTORY QUESTION
    # =================================================

    if is_history_question(message):

        today_history = get_today_history()

        if today_history:

            reply = "Lo bhai, aaj humari baatein 📜😂\n\n"

            count = 1

            for user_message, ai_reply, created_at in today_history:

                time_only = created_at[11:19]

                reply += (
                    f"{count}. {time_only} - "
                    f"{user_message}\n"
                )

                count += 1

        else:

            reply = (
                "Aaj abhi tak humari koi "
                "previous chat nahi hui. 😄"
            )

        return jsonify({
            "reply": reply,
            "chat_id": chat_id
        })


    # =================================================
    # CURRENT CHAT HISTORY
    # =================================================

    chat_history = get_chat_history(chat_id)

    history_text = ""

    for user_message, ai_reply, created_at in chat_history:

        history_text += f"""
Date and Time: {created_at}

User: {user_message}

AI: {ai_reply}
"""


    # =================================================
    # PERSONAL INFORMATION
    # =================================================

    information = find_information(message)


    if information:

        info = get_info(information)

        if info:

            database_info = ", ".join(info)

            prompt = f"""
You are Arnav's personal AI chatbot.

Your job is to answer questions about Arnav using the
information provided in the database and the previous
conversation.

Previous conversation:

{history_text}

The user asked:

{message}

Information from Arnav's database:

{information}: {database_info}


IMPORTANT RULES:

1. Do not invent, guess, or assume personal information
   about Arnav.

2. Use the database information when answering questions
   about Arnav.

3. If multiple database values are provided, include them
   naturally when relevant.

4. Use the previous conversation when it helps understand
   the user's question.

5. Answer naturally, like a helpful personal AI assistant.

6. Do not unnecessarily repeat the question.

7. Keep simple factual answers concise.

8. If the question requires explanation, give enough detail
   for the user to understand it.


FORMATTING RULES:

Use Markdown formatting when useful.

Use headings for longer explanations.

Use bullet points or numbered lists when appropriate.

For mathematical formulas, use LaTeX.

Use:
$$
formula
$$

for larger equations.

Use:
$formula$

for inline equations.

For programming questions, use proper Markdown code blocks.

Make the response clean, readable, and easy for a human
to understand.
"""


        else:

            reply = "I don't know that yet."

            save_chat(
                message,
                reply,
                chat_id
            )

            return jsonify({
                "reply": reply,
                "chat_id": chat_id
            })


    else:

        prompt = f"""
You are Arnav's personal AI chatbot.

Previous conversation:

{history_text}

User message:

{message}


Your goal is to have a natural and helpful conversation.

Use the previous conversation when it is relevant.

If the user is greeting you, greet them naturally.

If the user asks a simple factual question, answer directly.

If the user asks a technical, programming, mathematical,
DSA, DBMS, computer science, or educational question,
give a clear explanation instead of only giving the final
answer.


FOR EDUCATIONAL QUESTIONS:

1. Explain the concept clearly.

2. Break the solution into logical steps.

3. Show the important formulas when needed.

4. If there is a calculation, calculate it carefully.

5. If useful, provide a small example.

6. For programming questions, explain the logic and then
   provide clean code.

7. If the user asks why something happens, explain the
   reason rather than simply repeating the answer.

8. Do not skip important steps just to make the answer
   shorter.

9. Do not add unnecessary information.


ACCURACY:

Do not knowingly provide incorrect information.

For mathematical problems, carefully check calculations.

If the question is ambiguous or information is missing,
clearly say what is missing instead of inventing an answer.

For personal information about Arnav, only use information
available in the database or conversation.


FORMATTING:

Use Markdown formatting for readability.

Use headings when appropriate.

Use numbered steps for procedures.

Use bullet points for lists.

For mathematical formulas, use LaTeX.

Use:
$$
formula
$$

for display equations.

Use:
$formula$

for inline equations.

For programming questions, use Markdown code blocks.

Make every answer clean, readable, and understandable to
a human.


RESPONSE LENGTH:

Do not force every answer to be short.

Match the length to the question.

Simple questions can have short answers.

Complex questions should have enough explanation,
steps, examples, and reasoning to properly understand
the topic.
"""


    # =================================================
    # GEMINI
    # =================================================

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    reply = response.text


    # =================================================
    # SAVE CHAT
    # =================================================

    save_chat(
        message,
        reply,
        chat_id
    )


    # =================================================
    # FIRST MESSAGE BECOMES CHAT TITLE
    # =================================================

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM chat_history
        WHERE chat_id = ?
        """,
        (chat_id,)
    )

    count = cursor.fetchone()[0]


    if count == 1:

        title = message.strip()

        if len(title) > 35:

            title = title[:35] + "..."

        cursor.execute(
            """
            UPDATE chat_sessions
            SET title = ?
            WHERE id = ?
            """,
            (
                title,
                chat_id
            )
        )

        connection.commit()


    connection.close()


    return jsonify({
        "reply": reply,
        "chat_id": chat_id
    })


# =====================================================
# RUN
# =====================================================

app.run(debug=True)