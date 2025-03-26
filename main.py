"""
 Uses the tkinter module to generate a window, accept song input, and return the table of suggested songs.
"""

import tkinter as tk
from tkinter import ttk, Listbox

from RecommendationSystem import RecommendationSystem

recommendation_system = RecommendationSystem()
song_list_names = list(recommendation_system.song_list_names.keys())

root = tk.Tk()
root.title("Music Search ahh app")
root.option_add("*tearOff", False)

# root.columnconfigure(0, weight=1)
# root.columnconfigure(1, weight=3)
# root.rowconfigure(0, weight=1)

# Styling, import theme
style = ttk.Style(root)
root.tk.call("source", "forest-dark.tcl")
style.theme_use("forest-dark")
style.configure("Treeview", font=("Helvetica", 17), rowheight=25)

# Frame for the IO interface
main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True)
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=2)
main_frame.rowconfigure(0, weight=1)

tabs = ttk.Notebook(main_frame)
tabs.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

tab1 = ttk.Frame(tabs)
tabs.add(tab1, text="Search Database")

widgets_frame = ttk.Frame(tab1, padding=(0, 0, 0, 10))
widgets_frame.pack(padx=10, pady=10, fill="both", expand=True)

# Entry field
placeholder_text = "Enter song name here:"
entry = ttk.Entry(widgets_frame, foreground="white")
entry.insert(0, placeholder_text)
entry.grid(row=0, column=0, padx=5, pady=(5, 2), sticky="ew")


def on_click(_) -> None:
    """
        Changes the input text to white so that it is easier for user to see what they are typing.
    """
    if entry.get() == placeholder_text:
        entry.delete(0, tk.END)
        entry.configure(foreground="white")


def on_focus_out(_) -> None:
    """
        Changes the input text to gray again after checking that there is no possible input.
    """
    if entry.get() == "":
        entry.insert(0, placeholder_text)
        entry.configure(foreground="grey")


entry.bind("<FocusIn>", on_click)
entry.bind("<FocusOut>", on_focus_out)

# search bar + search results

listbox_frame = ttk.Frame(widgets_frame)
listbox_frame.grid(row=1, column=0, pady=10, sticky="nsew")

# Create scrollbars
v_scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical")
h_scrollbar = ttk.Scrollbar(listbox_frame, orient="horizontal")

my_list = Listbox(
    listbox_frame,
    width=50,
    background="#383434",
    foreground="white",
    font=("Helvetica", 15),
    yscrollcommand=v_scrollbar.set,
    xscrollcommand=h_scrollbar.set
)

v_scrollbar.config(command=my_list.yview)
h_scrollbar.config(command=my_list.xview)

v_scrollbar.pack(side="right", fill="y")
h_scrollbar.pack(side="bottom", fill="x")
my_list.pack(side="left", fill="both", expand=True)


def update(lst: list) -> None:
    """
        Update my_list for each keystroke

        Instance Attributes:
        - lst: list which will be inserted to my_list
    """
    my_list.delete(0, "end")
    for item in lst:
        my_list.insert("end", item)


def fill_entry(_) -> None:
    """
        fill up the search bar with the selected song from my_list
    """
    selected_index = my_list.curselection()
    if not selected_index:
        return
    song = my_list.get(selected_index)
    entry.delete(0, "end")
    entry.insert(0, song)
    entry.configure(foreground="white")


def check(_) -> None:
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

# Tab 2 - Webscraping
tab2 = ttk.Frame(tabs)
tabs.add(tab2, text="WebSearch")

web_widgets = ttk.Frame(tab2, padding=(0, 0, 0, 10))
web_widgets.pack(padx=10, pady=10, fill="both", expand=True)

# Entry field
placeholder_text = "Enter song name here:"
entry_web = ttk.Entry(web_widgets, foreground="white")
entry_web.insert(0, placeholder_text)
entry_web.grid(row=0, column=0, padx=5, pady=(5, 2), sticky="ew")


def on_click_web(_) -> None:
    """
        Changes the input text to white so that it is easier for user to see what they are typing.
    """
    if entry_web.get() == placeholder_text:
        entry_web.delete(0, tk.END)
        entry_web.configure(foreground="white")


def on_focus_out_web(_) -> None:
    """
        Changes the input text to gray again after checking that there is no possible input.
    """
    if entry_web.get() == "":
        entry_web.insert(0, placeholder_text)
        entry_web.configure(foreground="grey")


entry_web.bind("<FocusIn>", on_click_web)
entry_web.bind("<FocusOut>", on_focus_out_web)

# Tab 3 - Decision Tree
tab3 = ttk.Frame(tabs)
tabs.add(tab3, text="Custom!")

dt_widget = ttk.Frame(tab3, padding=(0, 0, 0, 10))
dt_widget.columnconfigure(0, weight=1)
dt_widget.columnconfigure(1, weight=1)

dt_widget.pack(padx=10, pady=10, fill="both", expand=True)

# dance slider
slider_dance_label = ttk.Label(dt_widget, text="Dancebility: 5")
slider_dance_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

slider_dance = ttk.Scale(dt_widget, from_=0, to=5, orient="horizontal", length=200)
slider_dance.set(2.5)  # Default value (number of recommendations)
slider_dance.grid(row=1, column=0, padx=5, pady=5, sticky="ew")


def update_dance_label(val) -> None:
    """
        updates the number beside the slider_label to represent the value of dance
        Instance Attributes:
        - val: value from the slider
    """
    slider_dance_label.config(text=f"Dancebility: {int(float(val))}")


slider_dance.config(command=update_dance_label)

# energy slider
slider_energy_label = ttk.Label(dt_widget, text="Energy:5")
slider_energy_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

slider_energy = ttk.Scale(dt_widget, from_=0, to=5, orient="horizontal", length=200)
slider_energy.set(2.5)  # Default value (number of recommendations)
slider_energy.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# Output table
output_frame = ttk.Frame(main_frame)
output_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")  # Expands fully

tree = ttk.Treeview(output_frame, columns=("Title", "Artist", "Score"), show="headings")
tree.heading("Title", text="Title")
tree.heading("Artist", text="Artist")
tree.heading("Score", text="Score")

tree.column("Title", width=350, anchor="w")
tree.column("Artist", width=150, anchor="center")
tree.column("Score", width=100, anchor="e")

tree.pack(expand=True, fill="both")
tree.tag_configure('even', background='#191c1a')
tree.tag_configure('odd', background='#2d302d')


def get_input() -> str:
    """
        Gets the text input from the user, after they click the recommend button.
    """
    song_name = entry.get()
    if song_name != placeholder_text:
        entry.delete(0, tk.END)
        entry.insert(0, placeholder_text)
        entry.configure(foreground="grey")
        return song_name


slider_label = ttk.Label(widgets_frame, text="Max number of Recommendations: 10")
slider_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

slider = ttk.Scale(widgets_frame, from_=1, to=10, orient="horizontal", length=200)
slider.set(10)  # Default value (number of recommendations)
slider.grid(row=4, column=0, padx=5, pady=5, sticky="ew")


def update_slider_label(val) -> None:
    """
        updates the number beside the slider_label to represent the value of n_recom
        Instance Attributes:
        - val: value from the slider
    """
    slider_label.config(text=f"Max number of Recommendations: {int(float(val))}")


# update slider_label with the current n_recom value
slider.config(command=update_slider_label)


def suggest_song() -> None:
    """
        takes the input, generates a list of simillar songs, and updates the treeview
    """
    song_input = get_input()
    n_recom = int(slider.get())

    my_list.selection_clear(0, tk.END)

    # firstly, clear the previous values
    for item in tree.get_children():
        tree.delete(item)

    # case: when u mistakenly click the recommend button twice or dont select a song
    if not song_input:
        tree.insert("", "end", values=("You must select a song from the list!", "-", "-"))
        return

    song_list = recommendation_system.generate_recommendations(song_input, 10)
    song_list = song_list[:n_recom]

    # case: no recommendations
    if not song_list:
        tree.insert("", "end", values=("No similar songs found :(", "", ""))
        return

    # Now, we need to update the treeview.
    # best_score = first score, which is the best recommendation
    best_score = float(song_list[00][2])

    def star(value: float) -> str:
        """
            converts the score to a star based rating
            within 50% greater than the best score: 3 stars
            between 50 to 75%: 2 stars
            more than 75%: 1 star
        """
        threshold_excellent = best_score * 1.5
        threshold_good = best_score * 1.75

        if value <= threshold_excellent:
            return "⭐⭐⭐️"
        elif value <= threshold_good:
            return "⭐⭐"
        else:
            return "⭐"

    i = 1
    for item in song_list:
        tag = 'even' if i % 2 == 0 else 'odd'
        tree.insert("", "end", values=(item[0], item[1], star(float(item[2]))), tags=(tag,))
        i += 1


# Recommend button for Database search
accent_button = ttk.Button(widgets_frame, text="Recommend New Songs!", style="Accent.TButton",
                           command=suggest_song)
accent_button.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")

# Center the window, and set minsize
root.update()
root.minsize(root.winfo_width(), root.winfo_height())
x_cordinate = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
y_cordinate = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
root.geometry("+{}+{}".format(x_cordinate, y_cordinate))

# initialize the window
root.mainloop()

# tabs feature check
