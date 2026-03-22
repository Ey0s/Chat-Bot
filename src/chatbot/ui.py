from __future__ import annotations

from typing import List

import customtkinter as ctk

from .bot import ChatBot
from .storage import JSONStorage


class ChatApp:
    def __init__(self, root: ctk.CTk, chatbot: ChatBot, storage: JSONStorage):
        self.chatbot = chatbot
        self.storage = storage
        self.history: List[str] = self.storage.load_history()

        self.root = root
        self.root.title(f"Chat-Ey Bot v2 by {self.chatbot.creator}")
        self.root.geometry("760x680")
        self.root.minsize(560, 520)

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(padx=14, pady=14, fill="both", expand=True)

        self.chat_display = ctk.CTkTextbox(
            main_frame,
            wrap="word",
            state="disabled",
            font=("Segoe UI", 14),
            corner_radius=10,
        )
        self.chat_display.pack(pady=(0, 10), fill="both", expand=True)

        self.chat_display.tag_config("user", foreground="#2B7DE9")
        self.chat_display.tag_config("bot", foreground="#2FA36B")
        self.chat_display.tag_config("system", foreground="#D96F2A")

        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(fill="x")

        self.user_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="Ask me anything...",
            font=("Segoe UI", 14),
            height=42,
        )
        self.user_input.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.user_input.bind("<Return>", lambda event: self.send_message())

        send_button = ctk.CTkButton(input_frame, text="Send", width=88, command=self.send_message)
        send_button.pack(side="right")

        btn_frame = ctk.CTkFrame(main_frame)
        btn_frame.pack(pady=8, fill="x")

        button_specs = [
            ("Show History", self.show_history),
            ("Clear Chat", self.clear_chat),
            ("Clear History", self.clear_history),
            ("Exit", self.exit_app),
        ]

        for text, command in button_specs:
            ctk.CTkButton(btn_frame, text=text, command=command).pack(
                side="left", padx=4, fill="x", expand=True
            )

        self.add_to_chat("system", f"Hello. I am Chat-Ey v2.0.0 by {self.chatbot.creator}.")
        self.add_to_chat("bot", "Try greeting me, asking for the date/time, or asking for help.")
        self.user_input.focus_set()

    def send_message(self) -> None:
        user_message = self.user_input.get().strip()
        if not user_message:
            return

        self.add_to_chat("user", f"You: {user_message}")
        self.user_input.delete(0, "end")

        bot_response = self.chatbot.get_response(user_message)
        self.add_to_chat("bot", f"Bot: {bot_response}")

        self.history.append(f"You: {user_message}")
        self.history.append(f"Bot: {bot_response}")
        self.storage.save_history(self.history)

    def add_to_chat(self, sender: str, message: str) -> None:
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", message + "\n", sender)
        self.chat_display.configure(state="disabled")
        self.chat_display.yview("end")

    def show_history(self) -> None:
        if not self.history:
            self.add_to_chat("system", "History is empty.")
            return
        self.add_to_chat("system", "Chat History:\n" + "\n".join(self.history))

    def clear_chat(self) -> None:
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")

    def clear_history(self) -> None:
        self.history.clear()
        self.storage.save_history(self.history)
        self.add_to_chat("system", "Chat history cleared.")

    def exit_app(self) -> None:
        self.root.quit()
