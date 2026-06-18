from flask import Flask, request, jsonify
from cipher.playfair_cipher import PlayFairCipher

app = Flask(__name__)

playfair_cipher = PlayFairCipher()

# 1. API Tạo Ma Trận Playfair
@app.route('/api/playfair/creatematrix', methods=['POST'])
def playfair_creatematrix():
    data = request.get_json()
    if not data or 'key' not in data:
        return jsonify({"error": "Thiếu tham số 'key'"}), 400
        
    key = data['key']
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    return jsonify({"playfair_matrix": playfair_matrix})

# 2. API Mã Hóa
@app.route('/api/playfair/encrypt', methods=['POST'])
def playfair_encrypt():
    data = request.get_json()
    if not data or 'text' not in data or 'key' not in data:
        return jsonify({"error": "Thiếu tham số 'text' hoặc 'key'"}), 400
        
    text = data['text']
    key = data['key']
    
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    encrypted_text = playfair_cipher.playfair_encrypt(text, playfair_matrix)
    return jsonify({'encrypted_text': encrypted_text})

# 3. API Giải Mã
@app.route('/api/playfair/decrypt', methods=['POST'])
def playfair_decrypt():
    data = request.get_json()
    if not data or 'text' not in data or 'key' not in data:
        return jsonify({"error": "Thiếu tham số 'text' hoặc 'key'"}), 400
        
    text = data['text']
    key = data['key']
    
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    decrypted_text = playfair_cipher.playfair_decrypt(text, playfair_matrix)
    return jsonify({'decrypted_text': decrypted_text})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)