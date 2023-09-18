import tkinter as tk
from sendable_bug_tracker import run_script

app = tk.Tk()
app.title("Bug Tracker (2-week)")
app.geometry("400x300")

product_label = tk.Label(app, text="Enter the product (project):")
product_entry = tk.Entry(app)
component_label = tk.Label(app, text="Enter the component:")
component_entry = tk.Entry(app)
severity_label = tk.Label(app, text="Enter the bug severity:")
severity_entry = tk.Entry(app)

def run_bug_tracker():
    """Run the bug tracker script with user-provided inputs."""
    product = product_entry.get()
    component = component_entry.get()
    severity = severity_entry.get()
    run_script(product, component, severity)

run_button = tk.Button(app, text="Run Bug Tracker", command=run_bug_tracker)

product_label.grid(row=0, column=0, padx=10, pady=10)
product_entry.grid(row=0, column=1, padx=10, pady=10)
component_label.grid(row=1, column=0, padx=10, pady=10)
component_entry.grid(row=1, column=1, padx=10, pady=10)
severity_label.grid(row=2, column=0, padx=10, pady=10)
severity_entry.grid(row=2, column=1, padx=10, pady=10)
run_button.grid(row=3, columnspan=2, padx=10, pady=10)

app.mainloop()