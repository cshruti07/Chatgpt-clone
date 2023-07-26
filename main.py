from flask import Flask,render_template,jsonify,request
from flask_pymongo import PyMongo
 
import openai

openai.api_key ="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"
 
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://shruti:N1eayKzgjmzrLzFE@cluster0.jrpdlzh.mongodb.net/chatgpt"
mongo = PyMongo(app)

@app.route('/')
def home():
    chats = mongo.db.chats.find({})
    mychats=[chat for chat in chats]
    print(mychats)
    return render_template("index.html",mychats=mychats)

@app.route('/api',methods=["GET","POST"])
def qa():
    if request.method=="POST":
        print(request.json)
        question=request.json.get("question")
        chat=mongo.db.chats.find_one({"question":question})
        print(chat)
        if chat:
            data={"question":question,"answer":f"{chat ['answer']}"}
            return jsonify(data)
        else:
            
           
           
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=question,
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
                )
            print(response)
            data={"question":question,"answer":response["choices"][0]["text"]}
            mongo.db.chats.insert_one({"question":question,"answer":response["choices"][0]["text"]})
            return jsonify(data)
    data={"result":"thank you! my name is chatgpt im here to help u "}
    return jsonify(data)
app.run(debug=True)