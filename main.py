import tkinter as tk
from tkinter import scrolledtext
from ask_ai import ask_ai
from summarizer import summarize_text
from quiz_generator import generate_quiz
from speech_to_text import listen_to_voice
from text_to_speech import speak_text
from database import save_history, get_history


window = tk.Tk()

window.title("AI Study Assistant")
window.geometry("1000x1000")
window.config(bg="#f0f4f7")

quiz_answers = ""

def get_answer():

    question = question_entry.get()

    if question.strip() == "":
        return

    output_area.delete(1.0, tk.END)

    output_area.insert(
        tk.END,
        "🤖 Thinking...\n\n"
    )

    window.update()

    try:

        answer = ask_ai(question)
        save_history(question, answer)

        output_area.delete(1.0, tk.END)

        output_area.insert(tk.END, answer)

        start = output_area.index(tk.INSERT)

        output_area.insert(
            tk.END,
            "\n\n🔊 Speak Answer"
        )

        end = output_area.index(tk.INSERT)

        output_area.tag_add(
            "speak",
            start,
            end
        )

        output_area.tag_config(
            "speak",
            foreground="blue",
            underline=True,
            font=("Arial", 11, "bold")
        )
        output_area.tag_bind(
            "speak",
            "<Enter>",
            lambda e: output_area.config(cursor="hand2")
        )

        output_area.tag_bind(
            "speak",
            "<Leave>",
            lambda e: output_area.config(cursor="")
        )

        def speak_click(event):

            speak_text(answer)

        output_area.tag_bind(
            "speak",
            "<Button-1>",
            speak_click
        )

    except Exception as e:

        output_area.delete(1.0, tk.END)

        output_area.insert(
            tk.END,
            f"Error:\n{e}"
        )

def summarize_notes():

    text = question_entry.get()

    if text.strip() == "":
        return

    output_area.delete(1.0, tk.END)

    output_area.insert(tk.END, "Summarizing...\n\n")

    try:

        summary = summarize_text(text)

        output_area.delete(1.0, tk.END)

        output_area.insert(tk.END, summary)

    except Exception as e:

        output_area.delete(1.0, tk.END)

        output_area.insert(tk.END, f"Error:\n{e}")


def create_quiz():

    global quiz_answers

    topic = question_entry.get()

    if topic.strip() == "":
        return

    output_area.delete(1.0, tk.END)

    output_area.insert(tk.END, "Generating Quiz...\n\n")

    try:

        quiz, answers = generate_quiz(topic)

        quiz_answers = answers

        output_area.delete(1.0, tk.END)

        output_area.insert(tk.END, quiz)

        
        output_area.insert(
            tk.END,
            "\n\nClick here to Show Answers"
        )

        start_index = "end-1c linestart"
        end_index = "end-1c"
        
        output_area.tag_add(
            "show_answers",
            start_index,
            end_index
        )

      
        output_area.tag_config(
            "show_answers",
            foreground="blue",
            underline=True,
            font=("Arial", 11, "bold")
        )

        
        output_area.tag_bind(
            "show_answers",
            "<Button-1>",
            lambda e: show_answers()
        )

    except Exception as e:

        output_area.delete(1.0, tk.END)

        output_area.insert(
            tk.END,
            f"Error:\n{e}"
        )

def show_answers():

    global quiz_answers

    if quiz_answers.strip() == "":
        return

    output_area.insert(
        tk.END,
        "\n\n========== ANSWERS ==========\n\n"
    )

    output_area.insert(
        tk.END,
        quiz_answers
    )



def reset_all():

    question_entry.delete(0, tk.END)

    output_area.delete(1.0, tk.END)


def close_app():

    window.destroy()


def use_voice_input():

    output_area.delete(1.0, tk.END)

    output_area.insert(
        tk.END,
        "🎤 Listening...\nPlease speak now..."
    )

    window.update()

    text = listen_to_voice()

    question_entry.delete(0, tk.END)

    question_entry.insert(0, text)

    output_area.delete(1.0, tk.END)

    output_area.insert(
        tk.END,
        f"You Said:\n\n{text}\n\n"
    )

    if text.startswith("Error"):
        return

    try:

        output_area.insert(
            tk.END,
            "🤖 Thinking...\n\n"
        )

        window.update()

     
        answer = ask_ai(text)

        output_area.insert(
            tk.END,
            answer
        )

    except Exception as e:

        output_area.insert(
            tk.END,
            f"\nError:\n{e}"
        )


def speak_answer():

    answer = output_area.get(1.0, tk.END)

    if answer.strip() == "":
        return

    speak_text(answer)

def view_history():

    output_area.delete(1.0, tk.END)

    history = get_history()

    if not history:

        output_area.insert(
            tk.END,
            "No study history found."
        )

        return

    for item in history:

        history_text = f"""

ID: {item[0]}

Question:
{item[1]}

Answer:
{item[2]}

Date:
{item[3]}

==================================================

"""

        output_area.insert(
            tk.END,
            history_text
        )


heading = tk.Label(
    window,
    text="AI STUDY ASSISTANT",
    font=("Arial", 24, "bold"),
    bg="#f0f4f7",
    fg="darkblue"
)

heading.pack(pady=20)

question_label = tk.Label(
    window,
    text="Ask Your Question",
    font=("Arial", 14, "bold"),
    bg="#f0f4f7",
    fg="black"
)

question_label.pack()


question_entry = tk.Entry(
    window,
    width=70,
    font=("Arial", 13),
    bd=3
)

question_entry.pack(pady=10)


button_frame = tk.Frame(
    window,
    bg="#f0f4f7"
)

button_frame.pack(pady=10)


ask_button = tk.Button(
    button_frame,
    text="Ask AI",
    font=("Arial", 12, "bold"),
    bg="blue",
    fg="white",
    width=12,
    command=get_answer
)

ask_button.grid(row=0, column=0, padx=10)


summarize_button = tk.Button(
    button_frame,
    text="Summarize",
    font=("Arial", 12, "bold"),
    bg="green",
    fg="white",
    width=12,
    command=summarize_notes
)

summarize_button.grid(row=0, column=1, padx=10)

quiz_button = tk.Button(
    button_frame,
    text="Generate Quiz",
    font=("Arial", 12, "bold"),
    bg="purple",
    fg="white",
    width=15,
    command=create_quiz
)

quiz_button.grid(row=0, column=2, padx=10)

voice_button = tk.Button(
    button_frame,
    text="Voice Input",
    font=("Arial", 12, "bold"),
    bg="#795548",
    fg="white",
    width=15,
    command=use_voice_input
)

voice_button.grid(row=0, column=4, padx=10)


answer_label = tk.Label(
    window,
    text="Answer",
    font=("Arial", 14, "bold"),
    bg="#f0f4f7",
    fg="black"
)

answer_label.pack(pady=10)


output_area = scrolledtext.ScrolledText(
    window,
    wrap=tk.WORD,
    width=85,
    height=18,
    font=("Arial", 11),
    bd=3
)

output_area.pack(pady=10)

bottom_button_frame = tk.Frame(
    window,
    bg="#f0f4f7"
)

bottom_button_frame.pack(pady=10)

history_button = tk.Button(
    bottom_button_frame,
    text="View History",
    font=("Arial", 12, "bold"),
    bg="#607D8B",
    fg="white",
    width=15,
    command=view_history
)

history_button.grid(row=0, column=0, padx=10)

reset_button = tk.Button(
    bottom_button_frame,
    text="Reset",
    font=("Arial", 12, "bold"),
    bg="orange",
    fg="white",
    width=12,
    command=reset_all
)

reset_button.grid(row=0, column=1, padx=10)


close_button = tk.Button(
    bottom_button_frame,
    text="Close",
    font=("Arial", 12, "bold"),
    bg="red",
    fg="white",
    width=12,
    command=close_app
)

close_button.grid(row=0, column=2, padx=10)


window.mainloop()
