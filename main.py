import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import random
import os
import sys
import simple_webbrowser
from PIL import ImageTk, Image
from core import level_db, scrapper
import sv_ttk

VERSION = 'v0.0.1 BETA'

LOGO_PATH: str = os.path.join(os.path.dirname(__file__), "assets", "full_logo.png")
ICON_PATH: str = os.path.join(os.path.dirname(__file__), "assets", "full_logo.ico")
GAME_PH = 'Doom (1993) / The Ultimate Doom'
EPISODE_PH = 'E1: Knee-Deep in the Dead'
MAP_PH = 'E1M1: Hangar'
SECRETS_PH = 0

root = tk.Tk()
root.title(f"Doom Map Guesser by MF366 - The GeoGuesser of DOOM ({VERSION})")
root.geometry('800x600')
root.resizable(True, False)

if sys.platform == 'win32':
    root.iconbitmap(ICON_PATH)

f1 = ttk.Frame(root)
f2 = ttk.Frame(f1)
f3 = ttk.Frame(f2)
f4 = ttk.Frame(f2)
f5 = ttk.Frame(f1)

img_label = ttk.Label(f3, text='Image not available.')

database: dict[str, dict[str, dict[str, list[int]]]] = {
    "Doom (1993) / The Ultimate Doom": level_db.ultimate_doom,
    "Doom II": level_db.doom_ii,
    "Doom II: Master Levels": level_db.doom_ii_master_levels,
    "Final Doom: TNT Evilution": level_db.final_doom_tnt_evilution,
    "Final Doom: The Plutonia Experiment": level_db.final_doom_plutonia_experiment,
    "Doom 64": level_db.doom_64,
    "No Rest for the Living": level_db.no_rest_for_the_living
}

screenshot_database: dict[str, list[str]] = scrapper.scrape_json_contents("https://raw.githubusercontent.com/MF366-Coding/DoomMapGuesser/main/.github/ss_db.json")

cur_screenshot = None
cur_settings = ['Norb', 'MF366', 'Zeca70', -1000]
cur_selections = [GAME_PH, EPISODE_PH, MAP_PH, SECRETS_PH]

game_var = tk.Variable(f4, list(database.keys()))
episode_var = tk.Variable(f4, list(database[cur_selections[0]].keys()))
maps_var = tk.Variable(f4, list(database[cur_selections[0]][cur_selections[1]].keys()))
number_of_secrets_var = tk.StringVar(f4, '0')


def choose_game_window(origin: ttk.Button, master: tk.Tk | tk.Toplevel = root):
    def _save_changes():
        try:
            index = game_listbox.curselection()[0]
            selected_text = game_listbox.get(index)
            
            cur_selections[0] = selected_text
            cur_selections[1] = list(database[cur_selections[0]].keys())[0]
            cur_selections[2] = list(database[cur_selections[0]][cur_selections[1]].keys())[0]
            
            origin.configure(text=selected_text)
            
            game_choice_win.destroy()
            
        except tk.TclError as e:
            mb.showerror("Doom Map Guesser - Error #1", f"You must select a game/WAD before hitting 'Comfirm'.\n{e}")
           
    game_choice_win = tk.Toplevel(master)
    game_choice_win.focus_set()
    game_choice_win.geometry('800x600')
    game_choice_win.resizable(False, False)
    game_choice_win.title("Choose the correct game/WAD")
    
    if sys.platform == 'win32':
        game_choice_win.iconbitmap(ICON_PATH)
    
    game_listbox = tk.Listbox(game_choice_win, listvariable=game_var, bg='dark blue', fg='yellow', selectmode=tk.SINGLE, width=100, height=20)
    accept_butt = ttk.Button(game_choice_win, text='Confirm', command=_save_changes)
        
    game_listbox.pack()
    accept_butt.pack()


def choose_episode_window(origin: ttk.Button, master: tk.Tk | tk.Toplevel = root):
    episode_var.set(list(database[cur_selections[0]].keys()))
    
    def _save_changes():
        try:
            index = episode_listbox.curselection()[0]
            selected_text = episode_listbox.get(index)
            
            cur_selections[1] = selected_text
            cur_selections[2] = list(database[cur_selections[0]][cur_selections[1]].keys())[0]
            
            origin.configure(text=selected_text)
            
            episode_choice_win.destroy()
            
        except tk.TclError as e:
            mb.showerror("Doom Map Guesser - Error #1", f"You must select a game/WAD before hitting 'Comfirm'.\n{e}")
           
    episode_choice_win = tk.Toplevel(master)
    episode_choice_win.focus_set()
    episode_choice_win.geometry('800x600')
    episode_choice_win.resizable(False, False)
    episode_choice_win.title(f"Choose the correct episode for {cur_selections[0]}")
    
    if sys.platform == 'win32':
        episode_choice_win.iconbitmap(ICON_PATH)
    
    episode_listbox = tk.Listbox(episode_choice_win, listvariable=episode_var, bg='dark blue', fg='yellow', selectmode=tk.SINGLE, width=100, height=20)
    accept_butt = ttk.Button(episode_choice_win, text='Confirm', command=_save_changes)
        
    episode_listbox.pack()
    accept_butt.pack()
    

def choose_map_window(origin: ttk.Button, master: tk.Tk | tk.Toplevel = root):
    maps_var.set(list(database[cur_selections[0]][cur_selections[1]].keys()))
    
    def _save_changes():
        try:
            index = maps_listbox.curselection()[0]
            selected_text = maps_listbox.get(index)
            
            cur_selections[2] = selected_text
            
            origin.configure(text=selected_text)
            
            map_choice_win.destroy()
            
        except tk.TclError as e:
            mb.showerror("Doom Map Guesser - Error #1", f"You must select a game/WAD before hitting 'Comfirm'.\n{e}")
           
    map_choice_win = tk.Toplevel(master)
    map_choice_win.focus_set()
    map_choice_win.geometry('800x600')
    map_choice_win.resizable(False, False)
    map_choice_win.title(f"Choose the correct map for {cur_selections[1]}")
    
    if sys.platform == 'win32':
        map_choice_win.iconbitmap(ICON_PATH)
    
    maps_listbox = tk.Listbox(map_choice_win, listvariable=maps_var, bg='dark blue', fg='yellow', selectmode=tk.SINGLE, width=100, height=20)
    accept_butt = ttk.Button(map_choice_win, text='Confirm', command=_save_changes)
        
    maps_listbox.pack()
    accept_butt.pack()


choose_game_butt = ttk.Button(f4, text=cur_selections[0], command=lambda:
    choose_game_window(choose_game_butt))
choose_episode_butt = ttk.Button(f4, text=cur_selections[1], command=lambda:
    choose_episode_window(choose_episode_butt))
choose_map_butt = ttk.Button(f4, text=cur_selections[2], command=lambda:
    choose_map_window(choose_map_butt))


def pick_new_game_wad():
    new_game_wad: str = random.choice(list(database.keys()))
    return new_game_wad


def pick_new_episode(game: str):
    new_episode = random.choice(list(database[game].keys()))
    return new_episode


def pick_new_map(game: str, episode: str) -> tuple[str, int, int]:
    new_map = random.choice(list(database[game][episode].keys()))
    return new_map, database[game][episode][new_map][0], database[game][episode][new_map][1]


def pick_new_screenshot(map_id: int, current_screenshot_link: str, attempts: int = 10) -> str | bool:
    new_screenshot = current_screenshot_link
    map_id = str(map_id)
    
    for _ in range(attempts):
        if map_id not in screenshot_database.keys():
            return False # [i] no screenshots for given map
        
        new_screenshot: str = random.choice(screenshot_database[map_id])
        
        if new_screenshot == current_screenshot_link:
            continue # [i] same screenshot, so let's move on
        
        return new_screenshot # [i] the screenshot exists and is new
    
    return False # [i] limit of attempts was reached


def display_intro(master: tk.Tk | tk.Toplevel = root):
    intro_win = tk.Toplevel(master)
    intro_win.focus_set()
    intro_win.resizable(False, False)
    intro_win.title(f"Meet Doom Map Guesser ({VERSION})")
    
    if sys.platform == 'win32':
        intro_win.iconbitmap(ICON_PATH)
    
    logo = Image.open(LOGO_PATH)
    intro_win.tk_logo = ImageTk.PhotoImage(logo, (100, 100))
    logo_label = ttk.Label(intro_win, image=intro_win.tk_logo)
    
    about_1 = ttk.Label(intro_win, text=f"Doom Map Guesser {VERSION} is the GeoGuesser of the DOOM series.")
    about_2 = ttk.Label(intro_win, text="Enjoy this little game made by MF366! :D")
    about_3 = ttk.Label(intro_win, text="Small note about what is considered a secret:")
    about_4 = ttk.Label(intro_win, text="The number of secrets are the number of sectors with Effect 9, whether they're acessible or not.")
    
    butt_github = ttk.Button(intro_win, text='GitHub', command=lambda:
        simple_webbrowser.website("https://github.com/MF366-Coding/DoomMapGuesser"))
    butt_discord = ttk.Button(intro_win, text='Discord Server', command=lambda:
        simple_webbrowser.website("https://discord.gg/HZnBRYTqvC"))
    butt_buy_coffee = ttk.Button(intro_win, text="Donate <3", command=lambda:
        simple_webbrowser.website("https://buymeacoffee.com/mf366/"))
        
    logo_label.pack()
    about_1.pack()
    about_2.pack()
    about_3.pack()
    about_4.pack()
    butt_github.pack()
    butt_discord.pack()
    butt_buy_coffee.pack()
    
    # sv_ttk.set_theme


def display_screenshot(screenshot_link: str):
    img = Image.frombytes("RGBA", (350, 250), scrapper.scrape_byte_contents(screenshot_link))
    f3.tk_img = ImageTk.PhotoImage(img)
    img_label.configure(text='', image=f3.tk_img)


def change_secret_amount_by_1(positive: bool):   
    # [!] i need to implement limits for this feature
    
    if positive:
        a = 1
        
    else:
        a = -1
    
    number_of_secrets_var.set(str(int(number_of_secrets_var.get()) + a))


secrets_label = ttk.Label(f4, textvariable=number_of_secrets_var)
secrets_plus_butt = ttk.Button(f4, text='+', command=lambda:
    change_secret_amount_by_1(True))
secrets_minus_butt = ttk.Button(f4, text='-', command=lambda:
    change_secret_amount_by_1(False))


def generate_new_game():
    global cur_screenshot, cur_selections, cur_settings
    
    game = pick_new_game_wad()
    episode = pick_new_episode(game)
    map_details = pick_new_map(game, episode)
    
    map_name = map_details[0]
    map_id = map_details[1]
    number_of_secrets = map_details[2]
    
    cur_screenshot = False
    
    while cur_screenshot is False:
        cur_screenshot = pick_new_screenshot(map_id, cur_screenshot)
    
    cur_settings = [game, episode, map_name, number_of_secrets]
    cur_selections = [GAME_PH, EPISODE_PH, MAP_PH, SECRETS_PH]
    number_of_secrets_var.set('0')
    
    choose_game_butt.configure(text=cur_selections[0])
    choose_episode_butt.configure(text=cur_selections[1])
    choose_map_butt.configure(text=cur_selections[2])

    display_screenshot(cur_screenshot)
    

def guess_screenshot():
    correct_guesses = 0
    
    cur_selections[3] = int(number_of_secrets_var.get())
    
    for index, setting in enumerate(cur_settings, 0):
        if cur_selections[index] == setting:
            correct_guesses += 1
    
    mb.showwarning("Final Results", f"Correct guesses: {correct_guesses}/4")


def prevent_from_leaving(master: tk.Tk | tk.Toplevel = root):
    leave_confirmation = mb.askyesno("Doom Map Guesser by MF366", "Leaving already :(... Please stay a little longer... Will you?")

    if not leave_confirmation:
        master.destroy()


generate_butt = ttk.Button(f5, text="Generate new screenshot (WON'T ASK FOR CONFIRMATION!)", command=generate_new_game)
guess_butt = ttk.Button(f5, text="Confirm guess (WON'T ASK FOR CONFIRMATION!)", command=guess_screenshot)
leave_butt = ttk.Button(f5, text='Exit', command=prevent_from_leaving)

# [*] packing the rest of the elements
img_label.pack()

choose_game_butt.pack()
choose_episode_butt.pack()
choose_map_butt.pack()

secrets_plus_butt.pack()
secrets_label.pack()
secrets_minus_butt.pack()

generate_butt.pack()
guess_butt.pack()
leave_butt.pack()

f3.grid(column=0, row=0)
f4.grid(column=1, row=0)

f2.pack()
f5.pack()

f1.pack()

display_intro()

sv_ttk.set_theme('dark', root)

root.protocol("WM_DELETE_WINDOW", prevent_from_leaving)

root.mainloop()
