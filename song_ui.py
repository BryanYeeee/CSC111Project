"""
 Uses the tkinter module to generate a window, accept song input, and return the table of suggested songs.
"""

import tkinter as tk
from tkinter import ttk, BooleanVar, Listbox

# TODO: NEED A LIST OF  ALL SONGS- ARTISTS PRESENT IN THE DATABASE for the autocomplete thing
song_list_names = []

root = tk.Tk()
root.title("Music Search ahh app")
root.option_add("*tearOff", False)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)
root.rowconfigure(0, weight=1)

style = ttk.Style(root)
# TODO: import forest style
style.configure("Treeview", font=("Helvetica", 17), rowheight=25)

# Frame for the IO interface
widgets_frame = ttk.Frame(root, padding=(0, 0, 0, 10))
widgets_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
widgets_frame.columnconfigure(0, weight=1)

# checkbox for popular songs
pop = BooleanVar()
p = ttk.Checkbutton(widgets_frame, text="Popular songs only", variable=pop)
p.grid(row=2, column=0, pady=(5, 2), sticky="w")  # Less vertical spacing

# Entry field
placeholder_text = "Enter song name here:"
entry = ttk.Entry(widgets_frame, foreground="white")
entry.insert(0, placeholder_text)
entry.grid(row=0, column=0, padx=5, pady=(5, 2), sticky="ew")


def on_click(_):
    """
        Changes the input text to white so that it is easier for user to see what they are typing.
    """
    if entry.get() == placeholder_text:
        entry.delete(0, tk.END)
        entry.configure(foreground="white")


def on_focus_out(_):
    """
        Changes the input text to gray again after checking that there is no possible input.
    """
    if entry.get() == "":
        entry.insert(0, placeholder_text)
        entry.configure(foreground="grey")


entry.bind("<FocusIn>", on_click)
entry.bind("<FocusOut>", on_focus_out)

# search bar

my_list = Listbox(widgets_frame, width=50, background="#383434", foreground="white", font=("Helvetia", 15))
my_list.grid(row=1, column=0, pady=40, sticky="ew")


def update(lst):
    """
        Update my_list for each keystroke
    """
    my_list.delete(0, "end")
    for item in lst:
        my_list.insert("end", item)


def fill_entry(_):
    """
        fill up the search bar with the selected song from my_list
    """
    selected_index = my_list.curselection()
    song = my_list.get(selected_index)
    entry.delete(0, "end")
    entry.insert(0, song)


def check(_):
    """
        check if the typed song is in the database, and if it is, display it in my_list
    """
    typed = entry.get()
    if not typed:
        data = song_list_names
    else:
        data = []
        for item in song_list_names:
            if typed.lower() in item.lower():
                data.append(item)
    update(data)


update(song_list_names)

entry.bind("<KeyRelease>", check)

my_list.bind("<<ListboxSelect>>", fill_entry)

# Output table
tree_frame = ttk.Frame(root)
tree_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")  # Expands fully

tree = ttk.Treeview(tree_frame, columns=("Title", "Artist", "Score"), show="headings")
tree.heading("Title", text="Title")
tree.heading("Artist", text="Artist")
tree.heading("Score", text="Score")

tree.column("Title", width=300, anchor="w")
tree.column("Artist", width=150, anchor="center")
tree.column("Score", width=100, anchor="center")

tree.pack(expand=True, fill="both")
tree.tag_configure('even', background='#191c1a')
tree.tag_configure('odd', background='#2d302d')


def get_input() -> tuple[str, bool]:
    """
        Gets the text input from the user, after they click the recommend button.
    """
    song_name = entry.get()
    if song_name != placeholder_text:
        entry.delete(0, tk.END)
        entry.insert(0, placeholder_text)
        entry.configure(foreground="grey")
        return song_name, pop.get()


def suggest_song() -> None:
    """
        takes the input, generates a list of simillar songs, and updates the treeview
    """
    song_input = get_input()
    # TODO: remove ts later
    print(song_input)
    # firstly, clear the previous values
    for item in tree.get_children():
        tree.delete(item)

    # TODO: NEED HELP GETTING THE LIST OF SUGGESTIONS - idk which function does that
    song_list = []

    # Now, we need to update the treeview.
    i = 1
    for item in song_list:
        tag = 'even' if i % 2 == 0 else 'odd'
        tree.insert("", "end", values=(item[0], item[1], item[2]), tags=(tag,))
        i += 1


# Recommend button
accent_button = ttk.Button(widgets_frame, text="Recommend New Songs!", style="Accent.TButton",
                           command=suggest_song)
accent_button.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")

# Center the window, and set minsize
root.update()
root.minsize(root.winfo_width(), root.winfo_height())
x_cordinate = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
y_cordinate = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
root.geometry("+{}+{}".format(x_cordinate, y_cordinate))

# initialize the window
root.mainloop()
