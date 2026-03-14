import customtkinter as ctk
import hashlib
import time
import threading
import bcrypt

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class CryptoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("DEMO MÃ HÓA")
        self.geometry("850x600")

        self.header = ctk.CTkLabel(self, text="HỆ THỐNG MÔ PHỎNG HÀM BĂM",
                                   font=("Arial", 24, "bold"))
        self.header.pack(pady=20)

        self.tabview = ctk.CTkTabview(self, width=800, height=450)
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

    def handleClick(self):
        user_input = self.m1_input.get()
        if not user_input:
            return
        user_encoded = user_input.encode("utf-8")

        hash_sha1 = hashlib.sha1(user_encoded).hexdigest()
        hash_sha256 = hashlib.sha256(user_encoded).hexdigest()
        hash_sha3 = hashlib.sha3_256(user_encoded).hexdigest()

        self.m1_sha1.delete(0, "end")
        self.m1_sha1.insert(0, hash_sha1)

        self.m1_sha2.delete(0, "end")
        self.m1_sha2.insert(0, hash_sha256)

        self.m1_sha3.delete(0, "end")
        self.m1_sha3.insert(0, hash_sha3)

    # --- MODULE 1 ---
    def draw_module1(self):
        # Input
        ctk.CTkLabel(self.tab1, text="Nhập mật khẩu:").pack(pady=5)
        self.m1_input = ctk.CTkEntry(self.tab1, width=400)
        self.m1_input.pack(pady=5)

        self.m1_btn = ctk.CTkButton(self.tab1, text="Thực hiện Hash")
        self.m1_btn.pack(pady=15)

        # Output
        self.m1_sha1 = self.create_row(self.tab1, "Mã SHA-1:")
        self.m1_sha2 = self.create_row(self.tab1, "Mã SHA-256:")
        self.m1_sha3 = self.create_row(self.tab1, "Mã SHA-3:")

        self.m1_btn.configure(command=self.handleClick)

    # --- MODULE 2 ---
    def draw_module2(self):
        ctk.CTkLabel(self.tab2, text="Mã Hash cần thám:").pack(pady=5)
        self.m2_hash_input = ctk.CTkEntry(self.tab2, width=450)
        self.m2_hash_input.pack(pady=5)

        # Progress bar
        self.m2_progress = ctk.CTkProgressBar(self.tab2, width=450)
        self.m2_progress.set(0)
        self.m2_progress.pack(pady=20)

        # Time
        self.time_frame = ctk.CTkFrame(self.tab2, fg_color="transparent")
        self.time_frame.pack(pady=5)

        self.lbl_time_title = ctk.CTkLabel(self.time_frame, text="Thời gian thực hiện: ", font=("Arial", 13))
        self.lbl_time_title.pack(side="left")

        self.m2_time_val = ctk.CTkLabel(self.time_frame, text="0.000s", font=("Arial", 13, "bold"),
                                        text_color="#3498DB")
        self.m2_time_val.pack(side="left")

        self.m2_btn = ctk.CTkButton(self.tab2, text="Bắt đầu thám mã", fg_color="#C0392B", hover_color="#922B21")
        self.m2_btn.pack(pady=15)

        self.m2_result_lbl = ctk.CTkLabel(self.tab2, text="Kết quả: ...", font=("Arial", 15, "bold"))
        self.m2_result_lbl.pack(pady=10)

        self.m2_btn.configure(command=self.cryptanalyze)

    def cryptanalyze(self):
        target_hash = self.m2_hash_input.get().strip()
        if not target_hash:
            self.m2_result_lbl.configure(text="Kết quả: Hãy nhập mã hash!", text_color="red")
            return
        # ví dụ từ điển
        dictionary = ["123456", "password", "admin123", "hello", "ptit", "crypto2026"]

        start_time = time.time()
        found = False
        self.m2_progress.set(0)

        for i, word in enumerate(dictionary):
            word_hashed = word.encode("utf-8")

            hash_list = [
                hashlib.sha1(word_hashed).hexdigest(),
                hashlib.sha256(word_hashed).hexdigest(),
                hashlib.sha3_256(word_hashed).hexdigest()
            ]

            if target_hash in hash_list:
                
                algorithm = ""
                if target_hash == hash_list[0]:
                    algorithm = "SHA-1"
                elif target_hash == hash_list[1]:
                    algorithm = "SHA-256"
                else:
                    algorithm = "SHA-3"

                end_time = time.time()
                self.m2_time_val.configure(text=f"{end_time - start_time:.4f}s")
                self.m2_result_lbl.configure(
                    text=f"Khớp {algorithm}: {word}",
                    text_color="#2ECC71"
                )
                # self.m2_progress.set(1.0)
                found = True
                break

            self.m2_progress.set((i + 1) / len(dictionary))
            self.update_idletasks()

        if not found:
            self.m2_time_val.configure(text=f"{time.time() - start_time:.4f}s")
            self.m2_result_lbl.configure(text="Kết quả: Không tìm thấy!", text_color="#E74C3C")

    # --- MODULE 3 ---
    def draw_module3(self):
        ctk.CTkLabel(self.tab3, text="Nhập mật khẩu: ").pack(pady=5)
        self.m3_input = ctk.CTkEntry(self.tab3, width=400)
        self.m3_input.pack(pady=5)

        self.m3_btn = ctk.CTkButton(self.tab3, text="Băm Bcrypt + Salt", fg_color="green",command=self.handle_bcrypt)
        self.m3_btn.pack(pady=15)

        self.m3_bcrypt_res = self.create_row(self.tab3, "Kết quả Bcrypt:")

    def handle_bcrypt(self):
        pwd = self.m3_input.get().encode()
        if not pwd: return

        # Tạo salt và hash
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(pwd, salt)

        self.m3_bcrypt_res.delete(0, 'end')
        self.m3_bcrypt_res.insert(0, hashed.decode())

app = CryptoApp()
app.mainloop()