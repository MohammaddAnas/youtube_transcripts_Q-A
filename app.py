import re
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from youtube_transcript_api import YouTubeTranscriptApi

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)

from langchain_community.vectorstores import FAISS

from langchain_core.prompts import PromptTemplate

from langchain_core.runnables import (
    RunnableParallel,
    RunnableLambda,
    RunnablePassthrough
)

from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()


# FLASK APP
app = Flask(
    __name__,
    static_folder="frontend",
    static_url_path=""
)

CORS(app)

@app.route("/")
def home():
    return send_from_directory(
        "frontend",
        "index.html"
    )

# GLOBAL RAG CHAIN
main_chain = None

# GEMINI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2
)


# GET YOUTUBE VIDEO ID
def get_video_id(url):

    match = re.search(r"v=([^&]+)", url)

    if match:
        return match.group(1)

    match = re.search(r"youtu\.be/([^?]+)", url)

    if match:
        return match.group(1)

    match = re.search(
        r"youtube\.com/shorts/([^?]+)",
        url
    )

    if match:
        return match.group(1)

    return None

# CREATE RAG

def create_rag(video_link):

    # 1. Get video ID
    video_id = get_video_id(video_link)

    if video_id is None:
        raise ValueError("Invalid YouTube URL")


    # 2. Get transcript
    transcript_list = (
        YouTubeTranscriptApi()
        .list(video_id)
    )

    transcript = next(
        iter(transcript_list)
    )

    transcript_data = transcript.fetch()

    transcript_text = " ".join(
        chunk.text
        for chunk in transcript_data
    )


    # 3. Split transcript
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.create_documents(
        [transcript_text]
    )


    # 4. Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001"
    )


    # 5. FAISS
    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )


    # 6. Retriever
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 4
        }
    )


    # 7. Format documents
    def format_docs(docs):

        return "\n\n".join(
            doc.page_content
            for doc in docs
        )


    # 8. Prompt
    prompt = PromptTemplate(
        template="""
You are a helpful assistant.

Answer ONLY from the provided transcript context.

If the context is insufficient, say:

"I don't know based on the provided transcript."

Context:
{context}

Question:
{question}

Answer:
""",
        input_variables=[
            "context",
            "question"
        ]
    )


    # 9. RunnableParallel
    parallel_chain = RunnableParallel({

        "context":
            retriever
            | RunnableLambda(format_docs),

        "question":
            RunnablePassthrough()
    })


    # 10. Parser
    parser = StrOutputParser()


    # 11. Main chain
    main_chain = (
        parallel_chain
        | prompt
        | llm
        | parser
    )


    return main_chain



# LOAD VIDEO
@app.route("/load-video", methods=["POST"])
def load_video():

    global main_chain

    data = request.get_json()

    video_link = data.get("video_link")


    if not video_link:

        return jsonify({
            "success": False,
            "message": "YouTube link is required"
        }), 400


    try:

        main_chain = create_rag(
            video_link
        )

        return jsonify({

            "success": True,

            "message":
                "Video loaded successfully"

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 400

# ASK QUESTION
@app.route("/ask", methods=["POST"])
def ask_question():

    global main_chain

    if main_chain is None:

        return jsonify({

            "success": False,

            "message":
                "Please load a video first."

        }), 400


    data = request.get_json()

    question = data.get("question")


    if not question:

        return jsonify({

            "success": False,

            "message":
                "Question is required."

        }), 400


    try:

        answer = main_chain.invoke(
            question
        )

        return jsonify({

            "success": True,

            "answer": answer

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500


# RUN SERVER
if __name__ == "__main__":

    app.run(
        debug=False,
        port=5000
    )