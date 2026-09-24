import os
import tkinter as tk
from PIL import Image, ImageTk  # Requires pillow: pip install pillow
import pyttsx3

# Initialize Text-To-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Main window setup
window = tk.Tk()
window.title("JesWay Hospital Navigator")
window.geometry("520x720")
window.resizable(False, False)

# Global variables for tracking user selections & images
bg_image = None
landmark_photo = None

selected_start = None
selected_dest = None

# Comprehensive list of hospital locations
LOCATIONS = [
    "Main OPD", "Maternity", "Accident",
    "Main Gate", "Administration", "Emergency", "Family Health",
    "Cardio", "X-Ray", "Mortuary", "Laboratory",
    "Blood Bank", "Main Pharmacy", "ENT",
    "Eye Clinic", "Pharmacy Annex", "MRI", "Physiotherapy"
]


def speak_directions(text):
    """Speaks the provided direction text aloud."""
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Audio Error: {e}")


def get_route_data(start, destination):
    """Returns directions and image file name for given start and destination."""
    routes = {
        ("Main Gate", "Maternity"): (
            "From the main gate, look to your right and take the first path headed toward the white and red building. Take the pathway to your left and walk straight down the cemented walkway. Pass the second building on your left and keep walking toward the third building on your left. Watch for signs—there is a pathway leading to your right that leads straight to Maternity.",
            "maternity.png"),
        ("Main Gate", "Administration"): (
            "From the main gate, walk straight and pass the first pathway on your right. Continue to the second pathway and head toward the story building directly on your left. That is the Administration block.",
            "administration.png"),
        ("Main OPD", "Laboratory"): (
           "From Main OPD, walk forward a short distance and turn right. Walk straight ahead toward the Main Pharmacy—the Laboratory will be directly in front of you.",
            "laboratory.png"),
        ("Main Gate", "Main OPD"): (
           "From the main gate, walk straight ahead while watching for signs directing to the OPD. Bypass the initial signs and keep heading straight until you reach the open building area with benches, a front desk, and a large hospital layout map displayed above. That is the Main OPD.",
            "Main OPD.png"),
        ("Main OPD", "X-Ray"): (
            "From Main OPD, turn directly to your left and take the first pathway. Walk straight to the end, then turn right. Look up for the signs indicating Accident and X-Ray.",
            "accidentXray.png"),
        ("Main OPD", "Main Pharmacy"): (
            "From Main OPD, walk forward a short distance to the first pathway on your right. Walk straight along the path—you will see Main Pharmacy directly opposite the Laboratory. Watch for signs along the way.",
            "pharmlab.png"),
        ("Main OPD", "Eye Clinic"): (
            "From Main OPD, walk forward and pass the first entrance. Walk toward the building directly in front of you, then move to your right. Watch on your left for signs indicating the Eye Department. Look for the blue and white door marked Eye Department.",
            "eyeclinic.png"),
        ("Main OPD", "Physiotherapy"): (
           "From Main OPD, walk straight ahead, passing the first pathways on both your left and right. Walk toward the two buildings directly in front of you and move to your left. Look for the large door with Physiotherapy written on it.",
            "physioeyeear.png"),
        ("Main Gate", "Emergency"): (
            "From the main gate, walk straight ahead, passing the OPD and the car park. Continue walking straight down the tarred road. Walk toward the ambulance or the first building directly in front of you after passing the OPD. That building is Emergency.",
              "emergency.png"),
        ("Main OPD", "Main Pharmacy"): (
           "From Main OPD, walk forward a short distance to the first pathway on your right. Walk straight along the path—you will see Main Pharmacy directly opposite the Laboratory. Watch for signs along the way.",
                "main pharmacy admin.png"),
        ("Main OPD", "Family Health"): (
            "From Main OPD, walk straight ahead, passing all pathways on your left and right. Bypass the building directly in front of you and continue until you reach a long pathway on your left. Walk to the very end of this pathway toward the building directly facing you. Watch for signs indicating Family Health.",
               "familyhealth.png"),
        ("Main OPD","X-Ray"): (
            "From Main OPD, turn directly to your left and take the first pathway. Walk straight to the end, then turn right. Look up for the signs indicating Accident and X-Ray.",
                "accidentXray.png"),
        ("Emergency", "Blood Bank"): (
            "From Emergency, walk straight along the path, passing the OPD. Turn left onto the pathway and follow it until you reach the first building. Always look up at the ceiling for signboards marked Blood Bank.",
                 "bloodbank.png"),
        ("Main OPD", "Eye Clinic"): (
               "Head out from the OPD entrance, turn right down the central corridor, and follow the blue wall markings to the Eye Clinic reception.",
                    "eyeclinic.png"),
        ("Main OPD", "ENT"): (
               "From the main waiting hall, take the left hallway leading toward the specialty clinics. ENT is the second door on your right.",
                   "entphysioeye.png"),
        ("Main OPD", "Physiotherapy"): (
                "Exit the rear OPD door, cross the covered walkway towards the rehab wing, and Physiotherapy is at the end of the hall.",
                    "physioeyeear.png"),
        ("Laboratory", "Pharmacy Annex"): (
                 "Leave the lab, head straight past the courtyard benches, and the Pharmacy Annex pickup window is on your right.",
                     "pharmannex.png"),
        ("Main Gate", "Mortuary"): (
                 "From the main gate, follow the outer service road to the far left boundary of the hospital grounds.",
                      "mortuary.png"),
    }

    if (start, destination) in routes:
        return routes[(start, destination)]
    else:
        return (f"From {start}, follow the directional wall signs following the primary corridor toward {destination}.",
                f"{destination.lower().replace(' ', '_')}.png")


def select_location(loc_name):
    """Handles 2-step selection: 1st click = Start, 2nd click = Destination."""
    global selected_start, selected_dest, landmark_photo

    if selected_start is None:
        selected_start = loc_name
        status_label.config(text=f"Location set: {selected_start}\nNow tap your DESTINATION", fg="#38bdf8")
        btn_dict[loc_name].config(bg="#0ea5e9", fg="#ffffff")

    elif selected_dest is None and loc_name != selected_start:
        selected_dest = loc_name
        btn_dict[loc_name].config(bg="#10b981", fg="#ffffff")

        direction, photo_name = get_route_data(selected_start, selected_dest)

        status_label.config(text=f"Route: {selected_start} ➔ {selected_dest}", fg="#10b981")
        text_label.config(text=direction)

        # Show Action Buttons
        canvas.itemconfig(reset_window, state="normal")
        canvas.itemconfig(audio_window, state="normal")

        # Load & Resize Landmark Image safely
        if photo_name != "" and os.path.exists(photo_name):
            try:
                img = Image.open(photo_name)
                img = img.resize((360, 200), Image.Resampling.LANCZOS)
                landmark_photo = ImageTk.PhotoImage(img)
                image_label.config(image=landmark_photo, text="", bg="#0f172a")
            except Exception:
                image_label.config(image="", text=f"[ Image Error: Re-save '{photo_name}' ]", fg="#f87171", bg="#0f172a")
        else:
            image_label.config(image="", text=f"[ Landmark Photo '{photo_name}' ]", fg="#cbd5e1", bg="#0f172a")

        speech_text = f"Route set from {selected_start} to {selected_dest}. {direction}"
        window.after(100, lambda: speak_directions(speech_text))


def play_audio():
    """Replays the direction text for the currently active route."""
    if selected_start and selected_dest:
        direction = text_label.cget("text")
        speak_directions(direction)


def reset_selection():
    """Resets all button colors and clears current route."""
    global selected_start, selected_dest, landmark_photo

    selected_start = None
    selected_dest = None
    landmark_photo = None

    for loc, btn in btn_dict.items():
        btn.config(bg="#1e293b", fg="#ffffff")

    status_label.config(text="Please tap on your Location & Destination", fg="#ffffff")
    text_label.config(text="")
    image_label.config(image="", text="")

    # Hide Action Buttons
    canvas.itemconfig(reset_window, state="hidden")
    canvas.itemconfig(audio_window, state="hidden")


# --- Canvas Setup ---
canvas = tk.Canvas(window, width=520, height=720, highlightthickness=0, bg="#0f172a")
canvas.pack(fill="both", expand=True)

if os.path.exists("bg.png"):
    try:
        bg_img_raw = Image.open("bg.png").resize((520, 720), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(bg_img_raw)
        canvas.create_image(0, 0, image=bg_image, anchor="nw")
    except Exception:
        pass

# Header Title
title_label = tk.Label(canvas, text="JesWay Hospital Navigator", font=("Segoe UI", 14, "bold"), fg="#ffffff",
                       bg="#0ea5e9", padx=16, pady=4)
canvas.create_window(260, 30, window=title_label)

# Instruction Status Bar
status_label = tk.Label(canvas, text="Please tap on your Location & Destination", font=("Segoe UI", 10, "bold"),
                        fg="#ffffff", bg="#0f172a", padx=10, pady=2)
canvas.create_window(260, 68, window=status_label)

# --- Button Grid Frame ---
grid_frame = tk.Frame(canvas, bg="#0f172a", bd=2, relief="solid")
canvas.create_window(260, 205, window=grid_frame)

btn_dict = {}

for index, loc in enumerate(LOCATIONS):
    row = index // 4
    col = index % 4

    btn = tk.Button(
        grid_frame,
        text=loc,
        font=("Segoe UI", 8, "bold"),
        bg="#1e293b",
        fg="#ffffff",
        activebackground="#0ea5e9",
        activeforeground="#ffffff",
        width=12,
        height=2,
        wraplength=80,
        relief="flat",
        cursor="hand2",
        command=lambda l=loc: select_location(l)
    )
    btn.grid(row=row, column=col, padx=3, pady=3)
    btn_dict[loc] = btn

# Action Buttons
reset_btn = tk.Button(canvas, text="🔄 Reset Selection", command=reset_selection, bg="#ef4444", fg="#ffffff",
                      font=("Segoe UI", 9, "bold"), relief="flat", padx=8, pady=3, cursor="hand2")
reset_window = canvas.create_window(170, 340, window=reset_btn, state="hidden")

audio_btn = tk.Button(canvas, text="🔊 Read Directions Aloud", command=play_audio, bg="#0ea5e9", fg="#ffffff",
                      font=("Segoe UI", 9, "bold"), relief="flat", padx=8, pady=3, cursor="hand2")
audio_window = canvas.create_window(330, 340, window=audio_btn, state="hidden")

# Navigation Directions Output Box
text_label = tk.Label(canvas, text="", font=("Segoe UI", 9, "bold"), bg="#0f172a", fg="#f8fafc", wraplength=420,
                      relief="flat", bd=2, width=48, height=3)
canvas.create_window(260, 410, window=text_label)

# Landmark Display Area Frame (Pixel sizing handled via container)
image_frame = tk.Frame(canvas, width=360, height=200, bg="#0f172a", bd=2, relief="solid")
image_frame.pack_propagate(False)
canvas.create_window(260, 560, window=image_frame)

image_label = tk.Label(image_frame, bg="#0f172a")
image_label.pack(fill="both", expand=True)

window.mainloop()
