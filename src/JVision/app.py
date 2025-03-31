from datetime import datetime, timezone, timedelta
import io
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, JWTManager
import PIL.Image as Image
from dtrocr.model import DTrOCRLMHeadModel
from dtrocr.processor import DTrOCRProcessor
from api.load_model import load_model
from api.load_processor import load_processor
from api.create_dict import create_dict
from dict.dictionary import Dictionary
from schema.schema import WordSchema
from schema.models import OcrQuery, db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b4d0ada2eadcabc83ac56aae7fb58b87f0874b9112e76a36a5ca38ea9f487775'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Jvision.db'
jwt = JWTManager(app)

db.init_app(app)
with app.app_context():
    db.create_all()

class DTrOCR:
    model: DTrOCRLMHeadModel
    processor: DTrOCRProcessor
    dictionary: Dictionary
    
def startup():
    print("\nStarting up JVision\n")
    DTrOCR.model = load_model()
    print("\nSuccessfully loaded the model\n")
    DTrOCR.processor = load_processor()
    print("\nSuccessfully loaded the processor\n")
    DTrOCR.dictionary = create_dict()
    print("\nSuccessfully initialized the dictionary\n")
    

@app.route("/ocr", methods=['POST'])
@jwt_required()
def predict() -> str:
    body = request.data
    image = Image.open(io.BytesIO(body)).convert('RGB')
    image.save('api/images/res.png', "PNG")
    inputs = DTrOCR.processor(
        images=image,
        texts='',
        return_tensors='pt'
    )
    model_output = DTrOCR.model.generate(
        inputs,
        DTrOCR.processor,
        num_beams=1
    )

    predicted_text = DTrOCR.processor.tokeniser.decode(model_output[0], skip_special_tokens=True)
    wordList = DTrOCR.dictionary.search(predicted_text)
    if (len(wordList) >= 1):
        word = wordList[0]
        user_id = get_jwt_identity()
        time = datetime.now(timezone.utc).astimezone().isoformat(sep='/', timespec='minutes')
        query = OcrQuery(word.writings[0].writing, word.translations[0].translation, predicted_text, time, user_id)
        db.session.add(query)
        db.session.commit()
        print("Commited query")
    serializedWords = [translation.serialize() for translation in wordList]
    print(serializedWords)
    return jsonify(serializedWords)

@app.route("/user", methods=['POST'])
def create_user():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    user = User(username, email)
    user.set_password(password)
    try:    
        db.session.add(user)
        db.session.commit()
        response = jsonify({'message': 'Successfully registered!'})
    except:
        response = jsonify({'error': 'User already exists'})
    
    return response

@app.route("/user/<string:email>", methods=['GET'])
def login(email):
    password = request.headers.get('password')
    user = User.query.filter_by(email=email).first()
    authorized = user.check_password(password)
    if not authorized:
        return {'error': 'Email or password invalid'}, 401
    
    expires = timedelta(days=7)
    access_token = create_access_token(identity=str(user.id), expires_delta=expires)
    return {'token': access_token}, 200

@app.route("/history", methods=['GET'])
@jwt_required()
def get_history():
    user_id = get_jwt_identity()
    history = OcrQuery.query.filter_by(user_id = user_id).all()
    result = json_list = [i.serialize for i in history]
    print(result)
    return jsonify(result)

@app.route("/query/<string:query_text>", methods=['GET'])
@jwt_required()
def get_query(query_text):
    wordList = DTrOCR.dictionary.search(query_text)
    serializedWords = [translation.serialize() for translation in wordList]
    print(serializedWords)
    return jsonify(serializedWords)
    

if __name__ == '__main__':
    startup()
    app.run(debug=False, port=9000)

