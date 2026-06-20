# actions.py
import time
import random
import state
import trace
import drawing
from config import room_coords
from prolog_init import prolog

def move_to(room):
    """Move robot to the given room, with animation."""
    if state.current_robot == room:
        trace.trace_call(f"move({state.current_robot}, {room})")
        trace.trace_exit(f"Robot already at {room}")
        trace.trace_outcome("true")
        return True

    trace.trace_call(f"move({state.current_robot}, {room})")

    if room not in room_coords:
        trace.trace_failed(f"Room '{room}' doesn't exist")
        trace.trace_outcome("false")
        return False

    try:
        # Prolog check
        query = f"can_move({state.current_robot}, {room})"
        result = list(prolog.query(query))
        if not result:
            trace.trace_failed(f"Prolog move failed: no path from {state.current_robot} to {room}")
            trace.trace_outcome("false")
            return False

        # Animate movement
        steps = 20
        if state.current_robot in room_coords:
            start_x, start_y = room_coords[state.current_robot]
            end_x, end_y = room_coords[room]
            for i in range(steps + 1):
                progress = i / steps
                x = start_x + (end_x - start_x) * progress
                y = start_y + (end_y - start_y) * progress
                drawing.draw_robot_animation(x, y)
                time.sleep(0.03)

        old = state.current_robot
        state.current_robot = room
        drawing.draw_map()
        trace.trace_exit(f"Robot moved from {old} to {room}")
        trace.trace_outcome("true")
        return True

    except Exception as e:
        trace.trace_failed(f"move failed: {e}")
        trace.trace_outcome("false")
        return False

def clean(room):
    """Clean the specified room (if dirty)."""
    trace.trace_call(f"clean({room})")

    if room in state.cleaned_rooms:
        trace.trace_exit(f"{room.capitalize()} is already clean")
        trace.trace_outcome("true")
        return True

    if room == "dock":
        trace.trace_exit("Dock is always clean")
        trace.trace_outcome("true")
        return True

    if state.current_robot != room:
        trace.trace_info(f"Moving robot to {room} first...")
        if not move_to(room):
            return False

    try:
        query = f"can_clean({room})"
        result = list(prolog.query(query))
        if not result:
            trace.trace_failed(f"Prolog clean failed: cannot clean {room}")
            trace.trace_outcome("false")
            return False

        # Cleaning animation
        x, y = room_coords[room]
        for _ in range(10):
            drawing._canvas().delete("clean_effect")
            for _ in range(5):
                sx = x + random.randint(-40, 40)
                sy = y + random.randint(-30, 30)
                drawing._canvas().create_text(sx, sy, text="✨",
                                              font=("Arial", 16), tags="clean_effect")
            drawing._canvas().update_idletasks()
            time.sleep(0.1)
        drawing._canvas().delete("clean_effect")

        state.cleaned_rooms.add(room)
        state.room_noise[room] = []
        drawing.draw_map()
        trace.trace_exit(f"{room.capitalize()} cleaned successfully")
        trace.trace_outcome("true")
        state.update_cleanliness_indicator()
        return True

    except Exception as e:
        trace.trace_failed(f"clean failed: {e}")
        trace.trace_outcome("false")
        return False

def dock():
    """Move robot to dock and show charging animation."""
    trace.trace_call("dock")

    if state.current_robot == "dock":
        trace.trace_info("Robot already at dock, showing charging animation...")
        x, y = room_coords["dock"]
        drawing._canvas().delete("charging")
        for _ in range(3):
            drawing.draw_charging_animation(x, y)
            time.sleep(0.3)
            drawing._canvas().delete("charging")
            time.sleep(0.2)
        drawing.draw_charging_animation(x, y)
        trace.trace_exit("Robot docked and charging")
        trace.trace_outcome("true")
        return True

    trace.trace_info("Moving robot to dock...")
    if not move_to("dock"):
        return False

    x, y = room_coords["dock"]
    drawing._canvas().delete("charging")
    for i in range(5):
        drawing.draw_charging_animation(x, y)
        if i % 2 == 0:
            for r in [30, 40, 50]:
                drawing._canvas().create_oval(x-r, y-r, x+r, y+r,
                                              outline="#4CC9F0", width=2, dash=(2,2),
                                              tags="charging")
        drawing._canvas().update_idletasks()
        time.sleep(0.2)
        drawing._canvas().delete("charging")
        if i < 4:
            time.sleep(0.1)
    drawing.draw_charging_animation(x, y)
    trace.trace_exit("Successfully docked and charging")
    trace.trace_outcome("true")
    return True

def clear_map():
    """Reset map to default (robot at dock, hall clean, bedroom dirty)."""
    trace.trace_call("clear_map")
    state.current_robot = "dock"
    state.cleaned_rooms = {"hall", "dock"}
    state.room_noise["hall"] = []
    state.room_noise["bedroom"] = state.generate_noise_for_room("bedroom", 30)
    state.room_noise["dock"] = []
    drawing._canvas().delete("charging")
    drawing.draw_map()
    trace.trace_exit("Map and state cleared")
    trace.trace_outcome("true")
    state.update_cleanliness_indicator()

def return_to_default():
    """Return to default clean state (all rooms clean, robot at dock)."""
    trace.trace_call("return_to_default")
    state.current_robot = "dock"
    state.cleaned_rooms = {"hall", "bedroom", "dock"}
    state.room_noise = {"hall": [], "bedroom": [], "dock": []}
    drawing._canvas().delete("charging")
    drawing.draw_map()
    trace.trace_exit("Returned to default state (all rooms clean)")
    trace.trace_outcome("true")
    state.update_cleanliness_indicator()

def add_noise_to_rooms(room=None):
    """Make a room (or all rooms) dirty by adding noise."""
    if room:
        trace.trace_call(f"add_noise_to_rooms({room})")
        if room == "dock":
            trace.trace_info("Dock is always clean, cannot add noise")
            trace.trace_exit("Dock remains clean")
            trace.trace_outcome("true")
            return True
        if room in state.cleaned_rooms:
            state.cleaned_rooms.remove(room)
            trace.trace_info(f"{room.capitalize()} is now dirty")
        state.room_noise[room] = state.generate_noise_for_room(room, random.randint(20, 30))
        drawing.draw_map()
        trace.trace_exit(f"Added noise to {room}")
        trace.trace_outcome("true")
        state.update_cleanliness_indicator()
    else:
        trace.trace_call("add_noise_to_rooms()")
        for room_name in ["hall", "bedroom"]:
            if room_name in state.cleaned_rooms:
                state.cleaned_rooms.remove(room_name)
            state.room_noise[room_name] = state.generate_noise_for_room(room_name, random.randint(15, 25))
        drawing.draw_map()
        trace.trace_exit("Added noise to all rooms (except dock)")
        trace.trace_outcome("true")
        state.update_cleanliness_indicator()