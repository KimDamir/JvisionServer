import datetime
import io
from flask import Flask, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, JWTManager
import PIL.Image as Image
from dtrocr.model import DTrOCRLMHeadModel
from dtrocr.processor import DTrOCRProcessor
from api.load_model import load_model
from api.load_processor import load_processor
from api.create_dict import create_dict
from dict.dictionary import Dictionary
from schema.schema import WordSchema
from schema.models import Query, db, User

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
    translations = DTrOCR.dictionary.search(predicted_text)
    words_schema = WordSchema(many=True)
    print(jsonify(words_schema.dump(translations)))
    return jsonify(words_schema.dump(translations))

@app.route("/user", methods=['POST'])
def create_user():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    user = User(username, email)
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'Successfully registered!'})

@app.route("/user", methods=['GET'])
def login():
    data = request.get_json()
    user = User.objects.get(email=data.get('email'))
    authorized = user.check_password(data.get('password'))
    if not authorized:
        return {'error': 'Email or password invalid'}, 401
    
    expires = datetime.timedelta(days=7)
    access_token = create_access_token(identity=str(user.id), expires_delta=expires)
    return {'token': access_token}, 200

@app.route("/history", methods=['GET'])
@jwt_required
def get_history():
    user_id = get_jwt_identity
    history = Query.query.filter_by(user_id = user_id).all()
    return jsonify(history)


if __name__ == '__main__':
    startup()
    app.run(debug=False, port=9000)

