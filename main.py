# main.py
import customtkinter as ctk
import state
import drawing
import trace
import actions
import queries
from config import adjust_color, room_coords  # if needed elsewhere

# ---------------------- GUI Setup ----------------------
root = ctk.CTk()
root.title("🤖 Smart Vacuum Prolog Planner")
root.geometry("1200x850")
root.configure(fg_color="#1e1e2f")

# Title
title_label = ctk.CTkLabel(root, text="🤖 Smart Vacuum Prolog Planner",
                           font=("Arial", 28, "bold"), text_color="#4CC9F0")
title_label.pack(pady=15)

# Main container
main_frame = ctk.CTkFrame(root, fg_color="transparent")
main_frame.pack(fill="both", expand=True, padx=25, pady=10)

# Left panel (map + controls)
left_frame = ctk.CTkFrame(main_frame, width=500)
left_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))

map_frame = ctk.CTkFrame(left_frame, corner_radius=15)
map_frame.pack(fill="both", expand=True, pady=(0, 15))
map_label = ctk.CTkLabel(map_frame, text="🏠 Robot Map", font=("Arial", 18, "bold"))
map_label.pack(pady=8)

# Canvas
map_canvas = ctk.CTkCanvas(map_frame, width=750, height=350, bg="#111", highlightthickness=0)
map_canvas.pack(pady=10, padx=15)

# Inject canvas into drawing module
drawing.set_canvas(map_canvas)

# Controls frame
controls_frame = ctk.CTkFrame(left_frame, corner_radius=15)
controls_frame.pack(fill="x", pady=10)

controls_label = ctk.CTkLabel(controls_frame, text="🎮 Manual Controls",
                              font=("Arial", 16, "bold"))
controls_label.pack(pady=8)

# Button definitions (text, command, color)
button_grid = [
    ("🧹 Clean Hall",       lambda: actions.clean("hall"),                  "#04982E"),
    ("🛏️ Clean Bedroom",   lambda: actions.clean("bedroom"),               "#04982E"),
    ("⚡ Dock (Charge)",    actions.dock,                                  "#FFD166"),
    ("➡️ Hall",            lambda: actions.move_to("hall"),                "#FFA726"),
    ("➡️ Bedroom",         lambda: actions.move_to("bedroom"),             "#FFA726"),
    ("🏠 Go to Dock",      lambda: actions.move_to("dock"),                "#0609D6"),
    ("🌊 Hall Noise",      lambda: actions.add_noise_to_rooms("hall"),     "#FF6B6B"),
    ("🌊 Bedroom Noise",   lambda: actions.add_noise_to_rooms("bedroom"),  "#FF6B6B"),
    ("🔄 Default State",   actions.return_to_default,                     "#6B7280"),
]

for i, (text, cmd, color) in enumerate(button_grid):
    row = i // 3
    # Create row frame if needed
    if i % 3 == 0:
        row_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        row_frame.pack(fill="x", padx=12, pady=3)
    btn = ctk.CTkButton(row_frame, text=text, command=cmd,
                        fg_color=color, hover_color=adjust_color(color, -20),
                        font=("Arial", 13), height=40, corner_radius=8)
    btn.pack(side="left", fill="both", expand=True, padx=3)

# Right panel (query + trace)
right_frame = ctk.CTkFrame(main_frame)
right_frame.pack(side="right", fill="both", expand=True)

# Query frame
query_frame = ctk.CTkFrame(right_frame, corner_radius=15)
query_frame.pack(fill="x", pady=(0, 12))

query_label = ctk.CTkLabel(query_frame, text="🔍 Prolog Query", font=("Arial", 16, "bold"))
query_label.pack(pady=8)

query_input_frame = ctk.CTkFrame(query_frame, fg_color="transparent")
query_input_frame.pack(fill="x", padx=12, pady=6)

query_entry = ctk.CTkEntry(query_input_frame, placeholder_text="Enter Prolog query...",
                           font=("Courier", 13), height=40)
query_entry.pack(side="left", fill="x", expand=True, padx=(0, 12))

btn_query = ctk.CTkButton(query_input_frame, text="Run", command=queries.run_query,
                          fg_color="#7209B7", hover_color="#560BAD",
                          font=("Arial", 13, "bold"), width=80, height=40)
btn_query.pack(side="right")

# Pass query entry to queries module
queries.set_query_entry(query_entry)

# Plan button
plan_frame = ctk.CTkFrame(query_frame, fg_color="transparent")
plan_frame.pack(fill="x", padx=12, pady=6)

btn_find_plan = ctk.CTkButton(plan_frame, text="🔍 Find and Execute Plan",
                              command=queries.find_and_execute_plan,
                              fg_color="#4361EE", hover_color="#3A56D4",
                              font=("Arial", 13, "bold"), height=40)
btn_find_plan.pack(fill="x")

# Preset queries
preset_frame = ctk.CTkFrame(query_frame, fg_color="transparent")
preset_frame.pack(fill="x", padx=12, pady=6)

preset_label = ctk.CTkLabel(preset_frame, text="Presets:", font=("Arial", 11))
preset_label.pack(side="left", padx=(0, 10))

presets = [("Check Rooms", "room(X)"),
           ("Check Path", "can_move(dock, bedroom)"),
           ("All Connections", "connected(X, Y)")]

for text, q in presets:
    btn = ctk.CTkButton(preset_frame, text=text,
                        command=lambda q=q: query_entry.insert(0, q),
                        fg_color="#3A56D4", hover_color="#2D46B3",
                        font=("Arial", 10), height=30, width=80)
    btn.pack(side="left", padx=2)

# Trace output
trace_frame = ctk.CTkFrame(right_frame, corner_radius=15)
trace_frame.pack(fill="both", expand=True)

trace_label = ctk.CTkLabel(trace_frame, text="📜 Execution Trace",
                           font=("Arial", 16, "bold"))
trace_label.pack(pady=8)

trace_container = ctk.CTkFrame(trace_frame, fg_color="transparent")
trace_container.pack(fill="both", expand=True, padx=12, pady=8)

output_text = ctk.CTkTextbox(trace_container, font=("Consolas", 12),
                             fg_color="#222222", text_color="white", wrap="word")
output_text.pack(fill="both", expand=True)

# Inject output text into trace module
trace.set_output_text(output_text)

# Status bar
status_frame = ctk.CTkFrame(root, height=35, corner_radius=0)
status_frame.pack(side="bottom", fill="x")

cleanliness_label = ctk.CTkLabel(status_frame,
                                 text="🧹 Clean: 1/2 rooms (dock always clean)",
                                 font=("Arial", 11), text_color="#06D6A0")
cleanliness_label.pack(side="right", padx=20)

# Inject cleanliness label into state
state.set_cleanliness_label(cleanliness_label)

# Bottom control buttons
bottom_frame = ctk.CTkFrame(root, fg_color="transparent")
bottom_frame.pack(pady=12)

btn_clear_trace = ctk.CTkButton(bottom_frame, text="🗑️ Clear Trace",
                                command=queries.clear_trace,
                                fg_color="#4361EE", hover_color="#3A56D4",
                                font=("Arial", 13), width=130, height=40)
btn_clear_trace.pack(side="left", padx=8)

btn_clear_map = ctk.CTkButton(bottom_frame, text="🗑️ Clear Map",
                              command=actions.clear_map,
                              fg_color="#EF476F", hover_color="#D43D63",
                              font=("Arial", 13), width=130, height=40)
btn_clear_map.pack(side="left", padx=8)

btn_exit = ctk.CTkButton(bottom_frame, text="🚪 Exit",
                         command=root.destroy,
                         fg_color="#6B7280", hover_color="#4B5563",
                         font=("Arial", 13, "bold"), width=130, height=40)
btn_exit.pack(side="right", padx=8)

# ------------------ Initialise and Run ------------------
drawing.draw_map()
trace.trace_info("🚀 Smart Vacuum System Initialized")
trace.trace_info("📍 Robot is at dock")
trace.trace_info("🧹 Hall is clean, Bedroom is dirty, Dock is always clean")
trace.trace_info("🔍 Try 'Find and Execute Plan' button or enter a Prolog query")
trace.trace_info("⚡ Click 'Dock (Charge)' button for charging animation!")
state.update_cleanliness_indicator()

root.mainloop()