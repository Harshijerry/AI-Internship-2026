"""
AI Chatbot - Module 5 Project
FREE Version using Google Gemini API
Model: gemini-3.6-flash
Author: Harshini
Date: 2026
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()


class AIChatbot:
    """AI Chatbot using Google Gemini API (gemini-3.6-flash)"""

    def __init__(self):
        """Initialize the chatbot"""
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key or api_key == "your_api_key_here":
            print("\n" + "="*60)
            print("⚠️  API KEY NOT FOUND!")
            print("="*60)
            print("💡 Get your FREE key: https://aistudio.google.com/app/apikey")
            print("📝 Add it to .env file: GEMINI_API_KEY=your_key")
            print("="*60 + "\n")
            sys.exit(1)

        try:
            self.client = genai.Client(api_key=api_key)
            self.conversation_history = []
            self.start_time = datetime.now()
            print("✅ Chatbot initialized successfully!")
            print("🎯 Model: gemini-3.6-flash")
        except Exception as e:
            print(f"❌ Error initializing: {e}")
            sys.exit(1)

    def get_response(self, user_message):
        """Send message to AI using gemini-3.6-flash"""
        try:
            response = self.client.models.generate_content(
                model="gemini-3.6-flash",
                contents=user_message
            )
            ai_response = response.text

            # Save to history
            self.conversation_history.append({
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'user': user_message,
                'ai': ai_response
            })

            return ai_response

        except Exception as e:
            return f"❌ Error: {str(e)}\n💡 Check your API key and internet connection."

    def clear_history(self):
        """Clear conversation history"""
        if not self.conversation_history:
            print("\n📭 No conversation to clear!")
            return
        confirm = input("\n⚠️  Clear all history? (yes/no): ").strip().lower()
        if confirm == 'yes':
            self.conversation_history = []
            print("✅ Conversation history cleared!")
        else:
            print("❌ Cancelled.")

    def save_conversation(self):
        """Save conversation to text file"""
        if not self.conversation_history:
            print("\n📭 No conversation to save!")
            return
        filename = f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                f.write("AI CHATBOT CONVERSATION HISTORY\n")
                f.write("Model: gemini-3.6-flash\n")
                f.write("="*60 + "\n\n")
                for i, msg in enumerate(self.conversation_history, 1):
                    f.write(f"[{i}] {msg['timestamp']}\n")
                    f.write(f"👤 You: {msg['user']}\n\n")
                    f.write(f"🤖 AI: {msg['ai']}\n\n")
                    f.write("-"*60 + "\n\n")
            print(f"\n✅ Conversation saved to: {filename}")
        except Exception as e:
            print(f"\n❌ Error saving: {e}")

    def show_statistics(self):
        """Show conversation statistics"""
        if not self.conversation_history:
            print("\n📭 No conversation yet!")
            return
        total_msgs = len(self.conversation_history)
        total_user_chars = sum(len(m['user']) for m in self.conversation_history)
        total_ai_chars = sum(len(m['ai']) for m in self.conversation_history)
        duration = datetime.now() - self.start_time
        print("\n" + "="*50)
        print("📊 CONVERSATION STATISTICS")
        print("="*50)
        print(f"💬 Total exchanges: {total_msgs}")
        print(f"👤 Your characters: {total_user_chars}")
        print(f"🤖 AI characters: {total_ai_chars}")
        print(f"⏱️  Duration: {str(duration).split('.')[0]}")
        print("="*50)

    def quick_prompts(self):
        """Show quick prompt examples"""
        prompts = [
            "Explain Python decorators with examples",
            "Write a Python function to reverse a string",
            "What is the difference between list and tuple?",
            "Explain machine learning in simple terms",
            "Write a program to find factorial of a number",
            "How to debug a Python error?",
            "What is the difference between AI and ML?",
            "Explain OOP concepts with examples",
        ]
        print("\n" + "="*60)
        print("💡 QUICK PROMPT EXAMPLES")
        print("="*60)
        for i, prompt in enumerate(prompts, 1):
            print(f"  {i}. {prompt}")
        print("\n💡 Copy any prompt and paste it in the chat!")
        print("="*60)

    def chat(self):
        """Interactive chat mode"""
        print("\n" + "="*60)
        print("💬 CHAT MODE")
        print("="*60)
        print("Type 'back' to return to menu")
        print("Type 'save' to save conversation")
        print("="*60 + "\n")

        while True:
            try:
                user_input = input("👤 You: ").strip()
                if not user_input:
                    continue
                if user_input.lower() == 'back':
                    break
                if user_input.lower() == 'save':
                    self.save_conversation()
                    continue
                print("\n🤖 AI: ", end="", flush=True)
                response = self.get_response(user_input)
                print(response)
            except KeyboardInterrupt:
                print("\n\n👋 Returning to menu...")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

    def show_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("🤖 AI CHATBOT (FREE - Google Gemini)")
        print("🎯 Model: gemini-3.6-flash")
        print("="*50)
        print("1. 💬 Start Chatting")
        print("2. 📊 Show Statistics")
        print("3. 💾 Save Conversation")
        print("4. 🗑️  Clear History")
        print("5. 💡 Quick Prompt Examples")
        print("6. ❌ Exit")
        print("="*50)

    def run(self):
        """Main program loop"""
        print("\n" + "="*60)
        print("🎉 WELCOME TO AI CHATBOT!")
        print("="*60)
        print("💡 Powered by Google Gemini API (100% FREE)")
        print("🎯 Using Model: gemini-3.6-flash")
        print("="*60)

        while True:
            self.show_menu()
            try:
                choice = input("\nEnter your choice (1-6): ").strip()
                if choice == '1':
                    self.chat()
                elif choice == '2':
                    self.show_statistics()
                elif choice == '3':
                    self.save_conversation()
                elif choice == '4':
                    self.clear_history()
                elif choice == '5':
                    self.quick_prompts()
                elif choice == '6':
                    print("\n👋 Thank you for using AI Chatbot!\n")
                    break
                else:
                    print("❌ Invalid choice! Enter 1-6.")
            except KeyboardInterrupt:
                print("\n\n👋 Exiting...")
                break


if __name__ == "__main__":
    try:
        chatbot = AIChatbot()
        chatbot.run()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")