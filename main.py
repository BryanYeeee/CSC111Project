"""
 Uses the tkinter module to generate a window, accept song input, and return the table of suggested songs.
"""

import tkinter as tk
from tkinter import ttk, Listbox
from typing import Optional

import song_finder
from RecommendationSystem import RecommendationSystem
from SongDecisionTree import organize_levels

recommendation_system = RecommendationSystem()
song_list_names = list(recommendation_system.song_list_names.keys())

root = tk.Tk()
root.title("🎶")
root.option_add("*tearOff", False)

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

# tabs

tabs = ttk.Notebook(main_frame)
tabs.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


def prevent_auto_focus(_):
    """
        Forces focus away from the first widget in the tab
    """
    root.focus_set()


tabs.bind("<<NotebookTabChanged>>", prevent_auto_focus)

tab1 = ttk.Frame(tabs)
tabs.add(tab1, text="Search Database")

widgets_frame = ttk.Frame(tab1, padding=(0, 0, 0, 10))
widgets_frame.columnconfigure(0, weight=1)
widgets_frame.columnconfigure(1, weight=1)
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

# selected song listbox

selected_frame = ttk.Frame(widgets_frame)
selected_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="nsew")

vs_scrollbar = ttk.Scrollbar(selected_frame, orient="vertical")
hs_scrollbar = ttk.Scrollbar(selected_frame, orient="horizontal")

my_selected = Listbox(
    selected_frame,
    background="#383434",
    width=50,
    foreground="white",
    font=("Helvetica", 15),
    yscrollcommand=vs_scrollbar.set,
    xscrollcommand=hs_scrollbar.set,
    height=7
)

vs_scrollbar.config(command=my_selected.yview)
hs_scrollbar.config(command=my_selected.xview)

vs_scrollbar.pack(side="right", fill="y")
hs_scrollbar.pack(side="bottom", fill="x")
my_selected.pack(side="left", fill="both", expand=True)

# search bar + search results

listbox_frame = ttk.Frame(widgets_frame)
listbox_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")

# Create scrollbars
v_scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical")
h_scrollbar = ttk.Scrollbar(listbox_frame, orient="horizontal")

my_list = Listbox(
    listbox_frame,
    background="#383434",
    width=50,
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


def add_song():
    """ Show selected songs"""
    if not my_list.curselection():
        return
    current_song = my_list.get(my_list.curselection())
    my_selected.insert("end", current_song)
    song_list_names.remove(current_song)
    update(song_list_names)
    if current_song != placeholder_text:
        entry.delete(0, tk.END)
        entry.insert(0, placeholder_text)
        entry.configure(foreground="grey")
    print(current_song)


def remove_song():
    """
        Remove the selected song from the listbox
    """
    selected_song = my_selected.get(my_selected.curselection())
    if not selected_song:
        return
    song_list_names.append(selected_song)
    update(song_list_names)
    my_selected.delete(my_selected.curselection())


add_button = ttk.Button(widgets_frame, text="Add Song", style="Accent.TButton", command=add_song)
add_button.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

# "Remove Song" button
remove_button = ttk.Button(widgets_frame, text="Remove Song", style="Accent.TButton", command=remove_song)
remove_button.grid(row=2, column=1, padx=5, pady=10, sticky="nsew")

entry.bind("<KeyRelease>", check)

my_list.bind("<<ListboxSelect>>", fill_entry)

# Tab 2 - Webscraping
tab2 = ttk.Frame(tabs)
tabs.add(tab2, text="WebSearch")

web_widgets = ttk.Frame(tab2, padding=(0, 0, 0, 10))
web_widgets.pack(padx=10, pady=10, fill="both", expand=True)

# Entry field
placeholder_text = "Enter song name here:"
entry_web = ttk.Entry(web_widgets, foreground="white", width=50)
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

web_frame = ttk.Frame(web_widgets)
web_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="nsew")

# Create scrollbars
vw_scrollbar = ttk.Scrollbar(web_frame, orient="vertical")
hw_scrollbar = ttk.Scrollbar(web_frame, orient="horizontal")

web_list = Listbox(
    web_frame,
    background="#383434",
    width=50,
    foreground="white",
    font=("Helvetica", 15),
    yscrollcommand=vw_scrollbar.set,
    xscrollcommand=hw_scrollbar.set,
    height=5
)

vw_scrollbar.config(command=my_list.yview)
hw_scrollbar.config(command=my_list.xview)

vw_scrollbar.pack(side="right", fill="y")
hw_scrollbar.pack(side="bottom", fill="x")
web_list.pack(side="left", fill="both", expand=True)

web_links = {}

link_select = True
error_msg = "No songs found with the given name!"


def disable_selection(_):
    """
        Prevents you from selecting the error message when no songs are found
    """
    if not link_select:
        web_list.selection_clear(0, tk.END)


web_list.bind("<<ListboxSelect>>", disable_selection)


def search_web():
    """
        Gets the name of the song the user inputs, and then webscrapes and lists the "song name | artist" for the top
        five urls found based on the song input.
    """
    global link_select
    link_select = True
    global web_links
    web_list.delete(0, web_list.size())
    song_name = entry_web.get()
    if song_name != placeholder_text:
        entry_web.delete(0, tk.END)
        entry_web.insert(0, placeholder_text)
        entry_web.configure(foreground="grey")
    song_links = song_finder.get_song_links(song_name)

    if not song_links:
        web_list.insert("end", error_msg)
        link_select = False

    for link in song_links:
        element = song_finder.get_title_artist(link)
        item = element[0] + " | " + element[1]
        if item not in web_links:
            web_list.insert("end", item)
            web_links[item] = link


search_web_button = ttk.Button(web_widgets, text="Search Web", style="Accent.TButton",
                               command=search_web)
search_web_button.grid(row=1, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")


def get_web():
    """
        Gets the selected song's properties and uses it to suggest and show songs
    """
    song_name = web_list.get(web_list.curselection())  # this returns the song which u clicked on
    song_link = web_links[song_name]
    properties = song_finder.get_song_properties(song_link)
    properties_to_list = [properties[feature] for feature in properties]
    suggest_and_show_songs(organize_levels(*properties_to_list[3:]), 10)


accent_button_web = ttk.Button(web_widgets, text="Recommend New Songs!", style="Accent.TButton",
                               command=get_web)
accent_button_web.grid(row=5, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

# Tab 3 - Decision Tree

tab3 = ttk.Frame(tabs)
tabs.add(tab3, text="Custom!")

dt_widget = ttk.Frame(tab3, padding=(0, 0, 0, 10))
dt_widget.columnconfigure(0, weight=1)
dt_widget.columnconfigure(1, weight=1)

dt_widget.pack(padx=10, pady=10, fill="both", expand=True)


def get_val(val: float) -> int:
    """
        Gets the integer value for a slider, that is consistent with what is displayed in the labels
    """

    if 0 < val < 1:
        return 1
    else:
        return int(val)


# Danceability slider
slider_danceability_label = ttk.Label(dt_widget, text="Danceability: 2")
slider_danceability_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

slider_danceability = ttk.Scale(dt_widget, from_=0, to=5, orient="horizontal", length=200)
slider_danceability.set(2.5)
slider_danceability.grid(row=1, column=0, padx=5, pady=5, sticky="ew")


def update_danceability_label(val) -> None:
    """
    Updates the label for danceability to reflect the current slider value.
    Instance Attributes:
    - val: value from the slider
    """
    if 0 < float(val) < 1:
        slider_danceability_label.config(text=f"Danceability: 1")
    else:
        slider_danceability_label.config(text=f"Danceability: {int(float(val))}")


slider_danceability.config(command=update_danceability_label)

# Energy slider
slider_energy_label = ttk.Label(dt_widget, text="Energy: 2")
slider_energy_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

slider_energy = ttk.Scale(dt_widget, from_=0, to=5, orient="horizontal", length=200)
slider_energy.set(2.5)
slider_energy.grid(row=3, column=0, padx=5, pady=5, sticky="ew")


def update_energy_label(val) -> None:
    """
    Updates the label for energy to reflect the current slider value.
    Instance Attributes:
    - val: value from the slider
    """
    if 0 < float(val) < 1:
        slider_energy_label.config(text=f"Energy: 1")
    else:
        slider_energy_label.config(text=f"Energy: {int(float(val))}")


slider_energy.config(command=update_energy_label)

# Key slider
slider_key_label = ttk.Label(dt_widget, text="Key: 2")
slider_key_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")

slider_key = ttk.Scale(dt_widget, from_=0, to=5, orient="horizontal", length=200)
slider_key.set(2.5)
slider_key.grid(row=5, column=0, padx=5, pady=5, sticky="ew")


def update_key_label(val) -> None:
    """
    Updates the label for key to reflect the current slider value.
    Instance Attributes:
    - val: value from the slider
    """
    if 0 < float(val) < 1:
        slider_key_label.config(text=f"Key: 1")
    else:
        slider_key_label.config(text=f"Key: {int(float(val))}")


slider_key.config(command=update_key_label)

# Loudness slider
slider_loudness_label = ttk.Label(dt_widget, text="Loudness: 2")
slider_loudness_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

slider_loudness = ttk.Scale(dt_widget, from_=0, to=5, orient="horizontal", length=200)
slider_loudness.set(2.5)
slider_loudness.grid(row=1, column=1, padx=5, pady=5, sticky="ew")


def update_loudness_label(val) -> None:
    """
    Updates the label for loudness to reflect the current slider value.
    Instance Attributes:
    - val: value from the slider
    """
    if 0 < float(val) < 1:
        slider_loudness_label.config(text=f"Loudness: 1")
    else:
        slider_loudness_label.config(text=f"Loudness: {int(float(val))}")


slider_loudness.config(command=update_loudness_label)

# Mode slider
slider_mode_label = ttk.Label(dt_widget, text="Mode: 2")
slider_mode_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")

slider_mode = ttk.Scale(dt_widget, from_=0, to=5, orient="horizontal", length=200)
slider_mode.set(2.5)
slider_mode.grid(row=3, column=1, padx=5, pady=5, sticky="ew")


def update_mode_label(val) -> None:
    """
    Updates the label for mode to reflect the current slider value.
    Instance Attributes:
    - val: value from the slider
    """
    if 0 < float(val) < 1:
        slider_mode_label.config(text=f"Mode: 1")
    else:
        slider_mode_label.config(text=f"Mode: {int(float(val))}")


slider_mode.config(command=update_mode_label)

# Speechiness slider
slider_speechiness_label = ttk.Label(dt_widget, text="Speechiness: 2")
slider_speechiness_label.grid(row=4, column=1, padx=5, pady=5, sticky="w")

slider_speechiness = ttk.Scale(dt_widget, from_=0, to=5, orient="horizontal", length=200)
slider_speechiness.set(2.5)
slider_speechiness.grid(row=5, column=1, padx=5, pady=5, sticky="ew")


def update_speechiness_label(val) -> None:
    """
    Updates the label for speechiness to reflect the current slider value.
    Instance Attributes:
    - val: value from the slider
    """
    if 0 < float(val) < 1:
        slider_speechiness_label.config(text=f"Speechiness: 1")
    else:
        slider_speechiness_label.config(text=f"Speechiness: {int(float(val))}")


slider_speechiness.config(command=update_speechiness_label)

# Acousticness slider
slider_acousticness_label = ttk.Label(dt_widget, text="Acousticness: 2")
slider_acousticness_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")

slider_acousticness = ttk.Scale(dt_widget, from_=0, to=5, orient="horizontal", length=200)
slider_acousticness.set(2.5)
slider_acousticness.grid(row=7, column=0, padx=5, pady=5, sticky="ew")


def update_acousticness_label(val) -> None:
    """
    Updates the label for acousticness to reflect the current slider value.
    Instance Attributes:
    - val: value from the slider
    """
    if 0 < float(val) < 1:
        slider_acousticness_label.config(text=f"Acousticness: 1")
    else:
        slider_acousticness_label.config(text=f"Acousticness: {int(float(val))}")


slider_acousticness.config(command=update_acousticness_label)

# Instrumentalness slider
slider_instrumentalness_label = ttk.Label(dt_widget, text="Instrumentalness: 2")
slider_instrumentalness_label.grid(row=6, column=1, padx=5, pady=5, sticky="w")

slider_instrumentalness = ttk.Scale(dt_widget, from_=0, to=5, orient="horizontal", length=200)
slider_instrumentalness.set(2.5)
slider_instrumentalness.grid(row=7, column=1, padx=5, pady=5, sticky="ew")


def update_instrumentalness_label(val) -> None:
    """
    Updates the label for instrumentalness to reflect the current slider value.
    Instance Attributes:
    - val: value from the slider
    """
    if 0 < float(val) < 1:
        slider_instrumentalness_label.config(text=f"Instrumentalness: 1")
    else:
        slider_instrumentalness_label.config(text=f"Instrumentalness: {int(float(val))}")


slider_instrumentalness.config(command=update_instrumentalness_label)

# Liveness slider
slider_liveness_label = ttk.Label(dt_widget, text="Liveness: 2")
slider_liveness_label.grid(row=8, column=0, padx=5, pady=5, sticky="w")

slider_liveness = ttk.Scale(dt_widget, from_=0, to=5, orient="horizontal", length=200)
slider_liveness.set(2.5)
slider_liveness.grid(row=9, column=0, padx=5, pady=5, sticky="ew")


def update_liveness_label(val) -> None:
    """
    Updates the label for liveness to reflect the current slider value.
    Instance Attributes:
    - val: value from the slider
    """
    if 0 < float(val) < 1:
        slider_liveness_label.config(text=f"Liveness: 1")
    else:
        slider_liveness_label.config(text=f"Liveness: {int(float(val))}")


slider_liveness.config(command=update_liveness_label)

# Valence slider
slider_valence_label = ttk.Label(dt_widget, text="Valence: 2")
slider_valence_label.grid(row=8, column=1, padx=5, pady=5, sticky="w")

slider_valence = ttk.Scale(dt_widget, from_=0, to=5, orient="horizontal", length=200)
slider_valence.set(2.5)
slider_valence.grid(row=9, column=1, padx=5, pady=5, sticky="ew")


def update_valence_label(val) -> None:
    """
    Updates the label for valence to reflect the current slider value.
    Instance Attributes:
    - val: value from the slider
    """
    if 0 < float(val) < 1:
        slider_valence_label.config(text=f"Valence: 1")
    else:
        slider_valence_label.config(text=f"Valence: {int(float(val))}")


slider_valence.config(command=update_valence_label)

# Tempo slider
slider_tempo_label = ttk.Label(dt_widget, text="Tempo: 2")
slider_tempo_label.grid(row=10, column=0, padx=5, pady=5, sticky="w")

slider_tempo = ttk.Scale(dt_widget, from_=0, to=5, orient="horizontal", length=200)
slider_tempo.set(2.5)
slider_tempo.grid(row=11, column=0, padx=5, pady=5, sticky="ew")


def update_tempo_label(val) -> None:
    """
    Updates the label for tempo to reflect the current slider value.
    Instance Attributes:
    - val: value from the slider
    """
    if 0 < float(val) < 1:
        slider_tempo_label.config(text=f"Tempo: 1")
    else:
        slider_tempo_label.config(text=f"Tempo: {int(float(val))}")


slider_tempo.config(command=update_tempo_label)

# genre

genre_label = ttk.Label(dt_widget, text="Genre")
genre_label.grid(row=10, column=1, padx=5, pady=5, sticky="w")

genres = ["-"] + list(recommendation_system.genres)

genre_name = ttk.Combobox(dt_widget, values=genres, state="readonly", width=30)
genre_name.grid(row=11, column=1, padx=5, pady=5, sticky="w")


def get_slider():
    """
        Gets the value from all the attribute sliders + genre name
        All the values range from 0 to 5
        Multiplies the value with the range of the attribute given in SongGraph.py
        Cretes a list for these values
    """

    slider_value = [
        get_val(slider_danceability.get()),
        get_val(slider_energy.get()),
        get_val(slider_key.get()),
        get_val(slider_loudness.get()),
        get_val(slider_mode.get()),
        get_val(slider_speechiness.get()),
        get_val(slider_acousticness.get()),
        get_val(slider_instrumentalness.get()),
        get_val(slider_liveness.get()),
        get_val(slider_valence.get()),
        get_val(slider_tempo.get()),
    ]

    # u can modify this as needed to get the values
    attribute_range = [1, 1, 11, -10, 1, 1, 1, 1, 1, 1, 250]

    final_value = []

    for i in range(len(slider_value)):
        assert len(slider_value) == len(attribute_range)
        attribute = (slider_value[i] / 5) * attribute_range[i]
        final_value.append(attribute)

    # change this to whatever the decision tree needs
    suggest_and_show_songs(organize_levels(*final_value, genre_name.get().lower()), 10)


accent_button_slider = ttk.Button(dt_widget, text="Recommend New Songs!", style="Accent.TButton",
                                  command=get_slider)
accent_button_slider.grid(row=12, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

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
tree.tag_configure('header', background="#1DB954", foreground="#ffffff")


def get_input() -> list:
    """
        Gets the text input from the user, after they click the recommend button.
    """
    song_list = list(my_selected.get(0, "end"))
    print(song_list)
    return song_list


slider_label = ttk.Label(widgets_frame, text="Max number of Recommendations: 10")
slider_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="w")

slider = ttk.Scale(widgets_frame, from_=1, to=10, orient="horizontal", length=200)
slider.set(10)  # Default value (number of recommendations)
slider.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew")


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

    update(song_list_names)
    suggest_and_show_songs(song_input, n_recom)


def suggest_and_show_songs(given_input: Optional[str | list], recommended_count: int):
    """
    Given the user input, generate the song recommendations.
    """
    print(given_input)
    # firstly, clear the previous values
    for item in tree.get_children():
        tree.delete(item)

    # case: when u mistakenly click the recommend button twice or don't select a song
    if not given_input:
        tree.insert("", "end", values=("You must select a song from the list!", "-", "-"))
        return

    song_list = recommendation_system.generate_recommendations(given_input, recommended_count)
    print(song_list)
    # case: no recommendations
    if all({lst == [] for lst in song_list}):
        tree.insert("", "end", values=("No similar songs found :(", "", ""))
        return

    # Now, we need to update the treeview.
    # best_score = first score, which is the best recommendation

    def star(value: float, current_list: list) -> str:
        """
            converts the score to a star based rating
            within 50% greater than the best score: 3 stars
            between 50 to 75%: 2 stars
            more than 75%: 1 star
        """
        best_score = current_list[0][2]
        threshold_excellent = best_score * 1.5
        threshold_good = best_score * 1.75

        if value <= threshold_excellent:
            return "⭐⭐⭐️"
        elif value <= threshold_good:
            return "⭐⭐"
        else:
            return "⭐"

    n = len(song_list)
    for i in range(n):
        lst = song_list[i]
        if n > 1 and lst != []:
            tree.insert("", "end", values=(f'NUMBER OF SONGS IN COMMON: {n - i}', "", ""), tags='header')
        m = 0
        for item in lst:
            tag = 'even' if m % 2 == 0 else 'odd'
            tree.insert("", "end", values=(item[0], item[1], star(float(item[2]), lst)), tags=(tag,))
            m += 1


# Recommend button for Database search
accent_button = ttk.Button(widgets_frame, text="Recommend New Songs!", style="Accent.TButton",
                           command=suggest_song)
accent_button.grid(row=6, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

# Center the window, and set minsize
root.update()
root.minsize(root.winfo_width(), root.winfo_height())
x_cordinate = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
y_cordinate = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
root.geometry("+{}+{}".format(x_cordinate, y_cordinate))

# initialize the window
root.mainloop()
