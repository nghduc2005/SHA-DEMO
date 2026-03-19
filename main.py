import customtkinter as ctk
import threading
import os 

from algorithms import get_sha_hashes, dictionary_attack_file, generate_bcrypt, verify_bcrypt

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CryptoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("DEMO MÃ HÓA")
        self.geometry("850x650")
        
        self.dict_file_path = "demo.txt" 

        self.header = ctk.CTkLabel(self, text="HỆ THỐNG MÔ PHỎNG HÀM BĂM", font=("Arial", 24, "bold"))
        self.header.pack(pady=20)

        self.tabview = ctk.CTkTabview(self, width=800, height=500)
        self.tabview.pack(padx=20, pady=10)

        self.tab1 = self.tabview.add("Hash")
        self.tab2 = self.tabview.add("Thám mã")
        self.tab3 = self.tabview.add("Bcrypt + Salt")

        self.draw_module1()
        self.draw_module2()
        self.draw_module3()

    def create_row(self, master, text):
        row = ctk.CTkFrame(master, fg_color="transparent")
        row.pack(pady=5, fill="x", padx=100)
        ctk.CTkLabel(row, text=text, width=100, anchor="w").pack(side="left")
        entry = ctk.CTkEntry(row, width=350)
        entry.pack(side="right")
        return entry

    #  MODULE 1 
    def draw_module1(self):
        ctk.CTkLabel(self.tab1, text="Nhập mật khẩu:").pack(pady=5)
        self.m1_input = ctk.CTkEntry(self.tab1, width=400)
        self.m1_input.pack(pady=5)
        self.m1_btn = ctk.CTkButton(self.tab1, text="Thực hiện Hash", command=self.handle_hash)
        self.m1_btn.pack(pady=15)
        self.m1_sha1 = self.create_row(self.tab1, "Mã SHA-1:")
        self.m1_sha2 = self.create_row(self.tab1, "Mã SHA-256:")
        self.m1_sha3 = self.create_row(self.tab1, "Mã SHA-3:")

    def handle_hash(self):
        user_input = self.m1_input.get()
        if not user_input: return
        results = get_sha_hashes(user_input)
        self.m1_sha1.delete(0, "end"); self.m1_sha1.insert(0, results["sha1"])
        self.m1_sha2.delete(0, "end"); self.m1_sha2.insert(0, results["sha256"])
        self.m1_sha3.delete(0, "end"); self.m1_sha3.insert(0, results["sha3"])

    # MODULE 2 
    def draw_module2(self):
        ctk.CTkLabel(self.tab2, text="Mã Hash cần thám:").pack(pady=5)
        self.m2_hash_input = ctk.CTkEntry(self.tab2, width=450)
        self.m2_hash_input.pack(pady=5)

  
        self.m2_file_lbl = ctk.CTkLabel(self.tab2, text="Nguồn từ điển: demo.txt", text_color="gray", font=("Arial", 12, "italic"))
        self.m2_file_lbl.pack(pady=(0, 10))

        self.m2_progress = ctk.CTkProgressBar(self.tab2, width=450)
        self.m2_progress.set(0)
        self.m2_progress.pack(pady=10)

        self.time_frame = ctk.CTkFrame(self.tab2, fg_color="transparent")
        self.time_frame.pack(pady=5)
        ctk.CTkLabel(self.time_frame, text="Thời gian thực hiện: ", font=("Arial", 13)).pack(side="left")
        self.m2_time_val = ctk.CTkLabel(self.time_frame, text="0.000s", font=("Arial", 13, "bold"), text_color="#3498DB")
        self.m2_time_val.pack(side="left")

        self.m2_btn = ctk.CTkButton(self.tab2, text="Bắt đầu thám mã", fg_color="#C0392B", hover_color="#922B21", command=self.start_cracking_thread)
        self.m2_btn.pack(pady=15)

        self.m2_result_lbl = ctk.CTkLabel(self.tab2, text="Kết quả: ...", font=("Arial", 15, "bold"))
        self.m2_result_lbl.pack(pady=10)

    def start_cracking_thread(self):
        target_hash = self.m2_hash_input.get().strip()
        if not target_hash:
            self.m2_result_lbl.configure(text="Kết quả: Hãy nhập mã hash!", text_color="red")
            return
            
        if not os.path.exists(self.dict_file_path):
            self.m2_result_lbl.configure(text=f"Lỗi: Không tìm thấy file '{self.dict_file_path}'", text_color="red")
            return
            
        self.m2_btn.configure(state="disabled")
        self.m2_result_lbl.configure(text="Đang quét file, vui lòng đợi...", text_color="#F39C12")
        self.m2_progress.set(0)
        
        thread = threading.Thread(
            target=dictionary_attack_file, 
            args=(target_hash, self.dict_file_path, self.update_progress_safe, self.process_result_safe)
        )
        thread.daemon = True 
        thread.start()

    def update_progress_safe(self, percent):
        self.after(0, lambda: self.m2_progress.set(percent))

    def process_result_safe(self, result):
        self.after(0, lambda: self.show_final_result(result))

    def show_final_result(self, result):
        self.m2_btn.configure(state="normal") 
        
        if "error" in result:
            self.m2_result_lbl.configure(text=result["error"], text_color="red")
            return
            
        self.m2_time_val.configure(text=f"{result['time']:.4f}s")
        
        if result["found"]:
            self.m2_progress.set(1.0)
            self.m2_result_lbl.configure(text=f"Khớp {result['algorithm']}: {result['word']}", text_color="#2ECC71")
        else:
            self.m2_result_lbl.configure(text="Kết quả: Không tìm thấy trong từ điển!", text_color="#E74C3C")

    # MODULE 3 
    def draw_module3(self):
        ctk.CTkLabel(self.tab3, text="Nhập mật khẩu: ").pack(pady=5)
        self.m3_input = ctk.CTkEntry(self.tab3, width=400)
        self.m3_input.pack(pady=5)
        self.m3_btn = ctk.CTkButton(self.tab3, text="Băm Bcrypt + Salt", fg_color="green", command=self.handle_bcrypt_generate)
        self.m3_btn.pack(pady=15)
        self.m3_bcrypt_res = self.create_row(self.tab3, "Kết quả Bcrypt:")

        ctk.CTkLabel(self.tab3, text="--- MÔ PHỎNG ĐĂNG NHẬP ---", text_color="gray").pack(pady=(20, 5))
        self.m3_verify_hash = self.create_row(self.tab3, "Hash trong DB:")
        self.m3_verify_pwd = self.create_row(self.tab3, "Nhập mật khẩu:")
        self.m3_verify_btn = ctk.CTkButton(self.tab3, text="Kiểm tra (Verify)", fg_color="#F39C12", hover_color="#D68910", command=self.handle_bcrypt_verify)
        self.m3_verify_btn.pack(pady=15)
        self.m3_verify_lbl = ctk.CTkLabel(self.tab3, text="Kết quả: ...", font=("Arial", 15, "bold"))
        self.m3_verify_lbl.pack(pady=5)

    def handle_bcrypt_generate(self):
        pwd = self.m3_input.get()
        if not pwd: return
        hashed_str = generate_bcrypt(pwd)
        self.m3_bcrypt_res.delete(0, 'end'); self.m3_bcrypt_res.insert(0, hashed_str)
        # self.m3_verify_hash.delete(0, 'end'); self.m3_verify_hash.insert(0, hashed_str)

    def handle_bcrypt_verify(self):
        saved_hash = self.m3_verify_hash.get()
        input_pwd = self.m3_verify_pwd.get()
        if not saved_hash or not input_pwd: return
        
        if verify_bcrypt(input_pwd, saved_hash):
            self.m3_verify_lbl.configure(text=" Mật khẩu KHỚP! (Đăng nhập thành công)", text_color="#2ECC71")
        else:
            self.m3_verify_lbl.configure(text=" Mật khẩu SAI hoặc Hash không hợp lệ!", text_color="#E74C3C")

if __name__ == "__main__":
    app = CryptoApp()
    app.mainloop()