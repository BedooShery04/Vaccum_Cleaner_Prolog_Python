# config.py
import customtkinter as ctk

# Appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Room coordinates (center of each room on the canvas)
room_coords = {
    "hall": (130, 150),
    "bedroom": (425, 150),
    "dock": (670, 150)
}
# Room sizes (width, height)
room_sizes = {
    "hall": (225, 150),
    "bedroom": (225, 120),
    "dock": (125, 180)
}

def adjust_color(color, amount):
    """Lighten or darken a hex color."""
    try:
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        new_rgb = tuple(max(0, min(255, c + amount)) for c in rgb)
        return f'#{new_rgb[0]:02x}{new_rgb[1]:02x}{new_rgb[2]:02x}'
    except Exception:
        return color