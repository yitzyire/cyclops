import tkinter as tk
from tkinter import ttk, filedialog
import subprocess
import time
import sys
from collections import Counter
import re

def select_pcap_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Please select PCAP or PCAPNG file",
        filetypes=[("PCAP files", "*.pcap *.pcapng"), ("All files", "*.*")]
    )
    return file_path if file_path else None

def extract_diagnostics(pcap_path):
    diagnostics = []
    raw_log = ""

    try:
        retrans = subprocess.run(
            ["tshark", "-r", pcap_path, "-Y", "tcp.analysis.retransmission", "-T", "fields", "-e", "ip.src"],
            capture_output=True, text=True, check=True
        )
        ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', retrans.stdout)
        for ip, c in Counter(ips).items():
            diagnostics.append(("TCP Retransmission", ip, f"{c} packets"))
        raw_log += f"[TCP Retransmission]\n{retrans.stdout.strip()}\n"
    except subprocess.CalledProcessError:
        diagnostics.append(("TCP Retransmission", "Error", "Failed to parse."))

    try:
        resets = subprocess.run(
            ["tshark", "-r", pcap_path, "-Y", "tcp.flags.reset==1", "-T", "fields", "-e", "ip.src"],
            capture_output=True, text=True, check=True
        )
        ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', resets.stdout)
        for ip, c in Counter(ips).items():
            diagnostics.append(("TCP Reset", ip, f"{c} resets"))
        raw_log += f"[TCP Reset]\n{resets.stdout.strip()}\n"
    except subprocess.CalledProcessError:
        diagnostics.append(("TCP Reset", "Error", "Failed to parse."))

    try:
        icmp = subprocess.run(
            ["tshark", "-r", pcap_path, "-Y", "icmp.type==3 || icmp.type==11", "-T", "fields", "-e", "ip.src"],
            capture_output=True, text=True, check=True
        )
        ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', icmp.stdout)
        for ip, c in Counter(ips).items():
            diagnostics.append(("ICMP Error", ip, f"{c} packets"))
        raw_log += f"[ICMP Errors]\n{icmp.stdout.strip()}\n"
    except subprocess.CalledProcessError:
        diagnostics.append(("ICMP Error", "Error", "Failed to parse."))

    return diagnostics, raw_log.strip()

def launch_viewer_window(pcap_path):
    root = tk.Tk()
    root.title("PCAP Diagnostics Viewer")
    root.configure(bg="black", highlightthickness=0, bd=0)
    root.state("zoomed")
    root.overrideredirect(False)

    def on_close():
        root.destroy()
        sys.exit()

    root.protocol("WM_DELETE_WINDOW", on_close)

    main_frame = tk.Frame(root, bg="black", highlightthickness=0, bd=0)
    main_frame.pack(fill=tk.BOTH, expand=True)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(main_frame, variable=progress_var, maximum=100, length=600)
    progress_bar.pack(pady=20)

    percent_label = tk.Label(main_frame, text="Loading... 0%", font=("Segoe UI", 10), fg="white", bg="black")
    percent_label.pack()

    def show_diagnostics():
        for widget in main_frame.winfo_children():
            widget.destroy()

        toggle_frame = tk.Frame(main_frame, bg="black", highlightthickness=0, bd=0)
        toggle_frame.pack(fill=tk.X)

        toggle_button = tk.Button(toggle_frame, text="Show Raw Logs", font=("Segoe UI", 10),
                                  bg="#2e2e2e", fg="white", bd=0, highlightthickness=0)
        toggle_button.pack(pady=5)

        table_container = tk.Frame(main_frame, bg="black", highlightthickness=0, bd=0)
        table_container.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(table_container, columns=("Issue", "IP", "Details"), show="headings", height=15)
        tree.heading("Issue", text="Issue")
        tree.heading("IP", text="IP Address")
        tree.heading("Details", text="Details")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#1e1e1e",
                        foreground="white",
                        fieldbackground="#1e1e1e",
                        rowheight=28,
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="black", foreground="white", font=("Segoe UI", 10, "bold"))
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        style.configure("Vertical.TScrollbar", background="#2e2e2e", troughcolor="#1a1a1a", arrowcolor="white")
        style.map("Treeview", background=[("selected", "#333333")])

        vsb = ttk.Scrollbar(table_container, orient="vertical", command=tree.yview, style="Vertical.TScrollbar")
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=lambda *args: None)
        vsb.pack(side="right", fill="y")
        tree.pack(fill=tk.BOTH, expand=True)

        console_frame = tk.Frame(main_frame, bg="black", highlightthickness=0, bd=0)
        console_text = tk.Text(console_frame, wrap=tk.WORD, bg="black", fg="lightgray",
                               font=("Courier New", 10), bd=0, highlightthickness=0)
        console_scroll = ttk.Scrollbar(console_frame, orient="vertical", command=console_text.yview)
        console_text.configure(yscrollcommand=console_scroll.set)
        console_scroll.pack(side="right", fill="y")
        console_text.pack(side="left", fill=tk.BOTH, expand=True)
        console_frame.pack_forget()

        diagnostics, raw_log = extract_diagnostics(pcap_path)
        for index, (issue, ip, detail) in enumerate(diagnostics):
            color = "#90ee90" if "TCP" in issue else "orange"
            tag = f"row{index}"
            tree.insert("", "end", values=(issue, ip, detail), tags=(tag,))
            tree.tag_configure(tag,
                               background="#1e1e1e" if index % 2 == 0 else "#2a2a2a",
                               foreground=color)

        def toggle_view():
            if table_container.winfo_ismapped():
                table_container.pack_forget()
                console_text.delete(1.0, tk.END)
                console_text.insert(tk.END, raw_log)
                console_frame.pack(fill=tk.BOTH, expand=True)
                toggle_button.config(text="Show Summary Table")
            else:
                console_frame.pack_forget()
                table_container.pack(fill=tk.BOTH, expand=True)
                toggle_button.config(text="Show Raw Logs")

        toggle_button.config(command=toggle_view)

    def animate_progress():
        steps = 100
        interval = 1000 // steps
        for i in range(steps + 1):
            progress_var.set(i)
            percent_label.config(text=f"Loading... {i}%")
            root.update_idletasks()
            time.sleep(interval / 1000)
        percent_label.config(text="Ready.")
        root.after(500, show_diagnostics)

    root.after(500, animate_progress)
    root.mainloop()

# --- Run ---
if __name__ == "__main__":
    file_path = select_pcap_file()
    if file_path:
        launch_viewer_window(file_path)
