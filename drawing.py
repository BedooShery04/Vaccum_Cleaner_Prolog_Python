# drawing.py
import random
from config import room_coords, room_sizes
import state

# Canvas reference (set by main.py)
_map_canvas = None

def set_canvas(canvas):
    global _map_canvas
    _map_canvas = canvas

def _canvas():
    """Helper to get the canvas, raise if not set."""
    if _map_canvas is None:
        raise RuntimeError("Drawing canvas not initialised. Call set_canvas() first.")
    return _map_canvas

# ------------------------------------------------------------
def draw_robot(room):
    """Draw robot at a named room."""
    c = _canvas()
    c.delete("robot")
    if room in room_coords:
        x, y = room_coords[room]
        c.create_oval(x-15, y-15, x+15, y+15, fill="#FF6B6B", outline="white", width=3, tags="robot")
        c.create_oval(x-6, y-6, x-2, y-2, fill="white", tags="robot")
        c.create_oval(x+2, y-6, x+6, y-2, fill="white", tags="robot")
        c.create_text(x, y+30, text=f"🤖 {room}", fill="white", font=("Arial", 10, "bold"), tags="robot")

def draw_robot_animation(x, y):
    """Draw a temporary robot at an absolute position."""
    c = _canvas()
    c.delete("robot_anim")
    c.create_oval(x-20, y-20, x+20, y+20, fill="#FF6B6B", outline="white", width=3, tags="robot_anim")

def draw_charging_animation(x, y):
    """Draw the charging station effect."""
    c = _canvas()
    c.delete("charging")
    c.create_rectangle(x-40, y+10, x+40, y+50, fill="#4CC9F0", outline="white", width=2, tags="charging")
    c.create_oval(x-15, y-25, x+15, y+5, fill="#FFD166", outline="#FFB347", width=3, tags="charging")
    c.create_text(x, y-40, text="⚡", font=("Arial", 24), tags="charging")

def draw_noise_in_room(room):
    """Draw noise particles in a room (if any)."""
    c = _canvas()
    if room not in state.room_noise or not state.room_noise[room]:
        return
    for (x, y) in state.room_noise[room]:
        c.create_oval(x-3, y-3, x+3, y+3, fill="#F59E0B", outline="#D97706", width=1, tags="noise")

def draw_map():
    """Redraw the entire map (rooms, connections, robot, noise)."""
    c = _canvas()
    c.delete("all")

    # Connections
    connections = [("dock", "bedroom"), ("bedroom", "hall")]
    for r1, r2 in connections:
        x1, y1 = room_coords[r1]
        x2, y2 = room_coords[r2]
        w1 = room_sizes[r1][0]
        w2 = room_sizes[r2][0]
        c.create_line(x1 + w1//2, y1, x2 - w2//2, y2,
                     fill="#7209B7", width=10, dash=(5, 2))

    # Rooms
    for room, (x, y) in room_coords.items():
        width, height = room_sizes.get(room, (100, 60))
        is_clean = (room in state.cleaned_rooms) or (room == "dock")
        color = "#06D6A0" if is_clean else "#118AB2"

        c.create_rectangle(x - width//2, y - height//2,
                           x + width//2, y + height//2,
                           fill=color, outline="white", width=3)

        c.create_rectangle(x-55, y-60, x+55, y-40, fill="#2D3748", outline="white", width=2)
        c.create_text(x, y-50, text=room.upper(), fill="white", font=("Arial", 12, "bold"))

        # Status indicator
        if room == "dock":
            status_color = "#4CC9F0"
            status_text = "CHARGING"
        else:
            status_color = "#4ADE80" if is_clean else "#F87171"
            status_text = "CLEAN" if is_clean else "DIRTY"

        c.create_oval(x-30, y+height//2-30, x+30, y+height//2+10,
                      fill=status_color, outline="white", width=2)
        c.create_text(x, y+height//2-10, text=status_text,
                      fill="white", font=("Arial", 11, "bold"))

        if not is_clean and room != "dock":
            draw_noise_in_room(room)

    draw_robot(state.current_robot)