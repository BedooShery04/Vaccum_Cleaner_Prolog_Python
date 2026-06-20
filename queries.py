# queries.py
import threading
from prolog_init import prolog
import trace
import actions

# Reference to the query entry widget (set by main.py)
_query_entry = None

def set_query_entry(entry):
    global _query_entry
    _query_entry = entry

def clear_trace():
    """Clear the trace output window."""
    # Access the output text widget through trace module's internal variable
    # Since trace._output_text is set, we can use it to delete content.
    # A cleaner approach: add a clear function to trace module.
    # For brevity we'll directly use the known tag.
    if trace._output_text:
        trace._output_text.delete("1.0", "end")
    trace.trace_info("Trace cleared")

def run_query():
    """Execute the Prolog query currently in the entry field."""
    if not _query_entry:
        return
    query = _query_entry.get().strip()
    if not query:
        trace.trace_info("Please enter a query")
        return
    run_plan_query(query)

def run_plan_query(query):
    """Execute a Prolog query in a background thread and log results."""
    def worker():
        trace.trace_call(f"?- {query}")
        try:
            results = list(prolog.query(query))
            if not results:
                trace.trace_outcome("false (no results)")
                return
            for i, res in enumerate(results):
                trace._output_text.insert("end", f"\n--- Result {i+1} ---\n", "info")
                for key, value in res.items():
                    trace.trace_rule(f"{key} = {value}")
            trace.trace_outcome(f"true ({len(results)} results)")
        except Exception as e:
            trace._output_text.insert("end", f"Error: {e}\n", "error")
            trace.trace_outcome("false (error)")

    clear_trace()
    threading.Thread(target=worker, daemon=True).start()

def find_and_execute_plan():
    """Automatically generate and execute a plan to clean the bedroom and dock."""
    trace.trace_call("Finding plan to clean bedroom and return to dock...")

    if "bedroom" not in state.cleaned_rooms:
        # Hardcoded plan based on known connections: dock<->bedroom<->hall
        plan = ["move(dock, bedroom)", "clean(bedroom)", "dock"]
        trace.trace_rule(f"Plan: {plan}")
        trace.trace_info("Executing plan...")

        if not actions.move_to("bedroom"):
            trace.trace_failed("Failed to move to bedroom")
            return
        if not actions.clean("bedroom"):
            trace.trace_failed("Failed to clean bedroom")
            return
        if not actions.dock():
            trace.trace_failed("Failed to dock")
            return

        trace.trace_info("Plan execution completed!")
        trace.trace_outcome("true (plan executed)")
    else:
        trace.trace_info("All rooms are already clean! Showing charging animation...")
        actions.dock()
        trace.trace_outcome("true (goal already achieved)")