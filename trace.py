# trace.py
import time

# The text widget where traces are displayed (set by main.py)
_output_text = None

def set_output_text(widget):
    global _output_text
    _output_text = widget
    # Configure tags once
    widget.tag_config("call", foreground="yellow")
    widget.tag_config("exit", foreground="green")
    widget.tag_config("outcome", foreground="cyan")
    widget.tag_config("rule", foreground="#FF69B4")
    widget.tag_config("failed", foreground="#FF6B6B")
    widget.tag_config("info", foreground="#4CC9F0")
    widget.tag_config("error", foreground="#EF476F")

def _write(tag, msg):
    if _output_text:
        _output_text.insert("end", msg + "\n", tag)
        _output_text.see("end")
        _output_text.update_idletasks()
        time.sleep(0.02)

def trace_call(call):
    timestamp = time.strftime("%H:%M:%S")
    _write("call", f"[{timestamp}] Call: {call}")

def trace_exit(exit_str):
    _write("exit", f"      Exit: {exit_str}")

def trace_outcome(outcome):
    _write("outcome", f"   Outcome: {outcome}\n")

def trace_rule(rule_str):
    _write("rule", f"     Rule: {rule_str}")

def trace_failed(fail_str):
    _write("failed", f"   Failed: {fail_str}")

def trace_info(info_str):
    _write("info", f"     Info: {info_str}")