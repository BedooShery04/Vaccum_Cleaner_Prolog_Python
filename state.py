# state.py
import random
from config import room_coords, room_sizes

# Global robot state
current_robot = "dock"
# Rooms that are currently clean (dock is always clean)
cleaned_rooms = {"hall", "dock"}
# Noise particles per room (list of (x,y) tuples)
room_noise = {
    "hall": [],
    "bedroom": [],
    "dock": []          # Dock never has noise
}

# GUI widget references (set by main.py after creation)
cleanliness_label = None

def set_cleanliness_label(label):
    global cleanliness_label
    cleanliness_label = label

def update_cleanliness_indicator():
    """Update the cleanliness label in the status bar."""
    if cleanliness_label:
        # Only hall and bedroom count; dock is always clean
        clean_count = sum(1 for r in ['hall', 'bedroom'] if r in cleaned_rooms)
        cleanliness_label.configure(text=f"🧹 Clean: {clean_count}/2 rooms (dock always clean)")

def generate_noise_for_room(room, num_particles=30):
    """Generate random noise positions inside a room."""
    if room == "dock":
        return []
    x, y = room_coords[room]
    width, height = room_sizes[room]
    positions = []
    for _ in range(num_particles):
        noise_x = random.randint(x - width//2 + 20, x + width//2 - 20)
        noise_y = random.randint(y - height//2 + 20, y + height//2 - 20)
        positions.append((noise_x, noise_y))
    return positions