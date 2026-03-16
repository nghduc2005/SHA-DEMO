import hashlib
import time
import bcrypt

#  MODULE 1: HASH 
def get_sha_hashes(text):
    encoded = text.encode("utf-8")
    return {
        "sha1": hashlib.sha1(encoded).hexdigest(),
        "sha256": hashlib.sha256(encoded).hexdigest(),
        "sha3": hashlib.sha3_256(encoded).hexdigest()
    }

#  MODULE 2: THÁM MÃ
def dictionary_attack_file(target_hash, file_path, progress_callback, result_callback):
    start_time = time.time()
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            total_lines = sum(1 for _ in f)
    except Exception as e:
        result_callback({"error": f"Lỗi đọc file: {str(e)}"})
        return


    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f):
                word = line.strip()
                if not word: continue
                
                word_hashed = word.encode("utf-8")
                
                if target_hash == hashlib.sha1(word_hashed).hexdigest():
                    result_callback({"found": True, "word": word, "algorithm": "SHA-1", "time": time.time() - start_time})
                    return
                if target_hash == hashlib.sha256(word_hashed).hexdigest():
                    result_callback({"found": True, "word": word, "algorithm": "SHA-256", "time": time.time() - start_time})
                    return
                if target_hash == hashlib.sha3_256(word_hashed).hexdigest():
                    result_callback({"found": True, "word": word, "algorithm": "SHA-3", "time": time.time() - start_time})
                    return
                
                
                if i % 5000 == 0:
                    progress_callback(i / total_lines)
                    
    except Exception as e:
         result_callback({"error": f"Lỗi quét file: {str(e)}"})
         return
         
    progress_callback(1.0)
    result_callback({"found": False, "time": time.time() - start_time})

#  MODULE 3: BCRYPT + SALT 
def generate_bcrypt(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_bcrypt(password, saved_hash):
    try:
        return bcrypt.checkpw(password.encode('utf-8'), saved_hash.encode('utf-8'))
    except ValueError:
        return False