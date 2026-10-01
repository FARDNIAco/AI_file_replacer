import os
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime
import xml.etree.ElementTree as ET


# ------------------ Config Management ------------------
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.xml")


def load_config():
    if not os.path.exists(CONFIG_FILE):
        root = ET.Element("configuration")
        ET.SubElement(root, "destination").text = ""
        tree = ET.ElementTree(root)
        tree.write(CONFIG_FILE, encoding="utf-8", xml_declaration=True)
        return ""
    try:
        tree = ET.parse(CONFIG_FILE)
        dest = tree.getroot().findtext("destination") or ""
        return dest.strip()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read config file:\n{e}")
        return ""


def save_config(destination):
    root = ET.Element("configuration")
    ET.SubElement(root, "destination").text = destination
    tree = ET.ElementTree(root)
    tree.write(CONFIG_FILE, encoding="utf-8", xml_declaration=True)


# ------------------ Header Parsing (multi-format) ------------------
# Supports: //, #, ;, /* */, <!-- -->, --, and other comment styles.
# We just look for the Build / Changes / Location trio near the top of the file.
HEADER_PATTERN = re.compile(
    r"(?P<open>[^\n]*)"
    r"[\r\n]+[^\n]*?Build\s*:\s*(?P<build>[^\r\n]+?)\s*[\r\n]+"
    r"[^\n]*?Changes\s*:\s*(?P<idx>\d+)\s+of\s+(?P<total>\d+)\s*[\r\n]+"
    r"[^\n]*?Location\s*:\s*(?P<location>[^\r\n]+?)\s*[\r\n]+",
    re.IGNORECASE,
)

_LOC_CLEAN = re.compile(r"^[\\/]+|[\\/]+$")


def _normalize_location(loc: str) -> str:
    """Strip surrounding slashes/backslashes and unify separators."""
    loc = loc.strip().strip("*/#;<>!-").strip()
    loc = _LOC_CLEAN.sub("", loc)
    return loc.replace("\\", "/")


def parse_header(content: str):
    """
    Extract Build / Changes / Location from the top of a file.
    Works with PHP (//), CSS/JS (/* */), HTML (<!-- -->), Python (#),
    SQL (--), and similar comment styles.
    Returns dict or None.
    """
    # Only inspect the first ~2000 characters to avoid scanning whole file
    head = content[:2000]

    m = HEADER_PATTERN.search(head)
    if not m:
        return None

    try:
        idx = int(m.group("idx"))
        total = int(m.group("total"))
    except ValueError:
        return None

    return {
        "build": m.group("build").strip().strip("*/#;<>!-").strip(),
        "index": idx,
        "total": total,
        "location": _normalize_location(m.group("location")),
    }


# ------------------ Main Application ------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Deployment Manager")
        self.geometry("950x650")
        self.configure(bg="#f0f0f0")

        self.font_normal = ("Segoe UI", 10)
        self.font_bold = ("Segoe UI", 10, "bold")
        self.font_mono = ("Consolas", 10)

        try:
            self.option_add("*Font", self.font_normal)
        except Exception:
            pass

        self.source_dir = tk.StringVar()
        self.dest_dir = tk.StringVar(value=load_config())

        self._build_ui()

    def _build_ui(self):
        # ----- Settings Frame -----
        top = ttk.LabelFrame(self, text="Settings")
        top.pack(fill="x", padx=10, pady=5)

        ttk.Label(top, text="Destination Folder:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(top, textvariable=self.dest_dir, width=60).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(top, text="Browse...", command=self.choose_dest).grid(row=0, column=2, padx=5)
        ttk.Button(top, text="Save to XML", command=self.save_dest).grid(row=0, column=3, padx=5)

        # ----- Buttons Frame -----
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Select Source Folder",
                   command=self.choose_source).pack(side="left", padx=5)
        self.btn_action = ttk.Button(btn_frame, text="Run Action", command=self.run_action)
        self.btn_action.pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear Report",
                   command=self.clear_report).pack(side="left", padx=5)

        # ----- Source Label -----
        self.source_label = ttk.Label(self, text="Source folder: not selected", foreground="blue")
        self.source_label.pack(fill="x", padx=10)

        # ----- Report Frame -----
        report_frame = ttk.LabelFrame(self, text="Operation Report")
        report_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.report = scrolledtext.ScrolledText(
            report_frame, wrap="word", font=self.font_mono,
            bg="#ffffff", fg="#000000"
        )
        self.report.pack(fill="both", expand=True, padx=5, pady=5)

        self.report.tag_config("new", foreground="green")
        self.report.tag_config("modified", foreground="orange")
        self.report.tag_config("error", foreground="red")
        self.report.tag_config("info", foreground="blue")

    # ------------------ Actions ------------------
    def choose_dest(self):
        d = filedialog.askdirectory(title="Select Destination Folder")
        if d:
            self.dest_dir.set(d)

    def save_dest(self):
        save_config(self.dest_dir.get())
        messagebox.showinfo("Saved", "Settings saved to config.xml")

    def choose_source(self):
        d = filedialog.askdirectory(title="Select Source Folder")
        if d:
            self.source_dir.set(d)
            self.source_label.config(text=f"Source folder: {d}")

    def clear_report(self):
        self.report.delete("1.0", "end")

    def log(self, text, tag=None):
        self.report.insert("end", text + "\n", tag)
        self.report.see("end")
        self.update_idletasks()

    # ------------------ Main Operation ------------------
    def run_action(self):
        src = self.source_dir.get().strip()
        dst = self.dest_dir.get().strip()

        if not src or not os.path.isdir(src):
            messagebox.showerror("Error", "Source folder is not valid.")
            return
        if not dst:
            messagebox.showerror("Error", "Destination folder is not configured.")
            return

        self.clear_report()
        self.log(f"=== Operation started - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===", "info")
        self.log(f"Source: {src}")
        self.log(f"Destination: {dst}\n")

        # 1. Collect files and parse headers
        files_info = []
        errors = []
        for name in sorted(os.listdir(src)):
            full = os.path.join(src, name)
            if not os.path.isfile(full):
                continue
            try:
                with open(full, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
            except Exception as e:
                errors.append(f"Failed to read '{name}': {e}")
                continue

            info = parse_header(content)
            if not info:
                errors.append(f"Invalid header in file '{name}'.")
                continue

            info["filename"] = name
            info["content"] = content
            files_info.append(info)

        if errors:
            for e in errors:
                self.log("[X] " + e, "error")
            self.log("\nOperation aborted due to errors above.", "error")
            return

        if not files_info:
            self.log("No valid files found in source folder.", "error")
            return

        # 2. Check Build consistency
        builds = {fi["build"] for fi in files_info}
        if len(builds) > 1:
            self.log("[X] Build numbers are not identical:", "error")
            for fi in files_info:
                self.log(f"   - {fi['filename']}: Build = {fi['build']}", "error")
            return
        build = builds.pop()
        self.log(f"[OK] Build number is consistent: {build}", "info")

        # 3. Check total count
        declared_totals = {fi["total"] for fi in files_info}
        if len(declared_totals) > 1:
            self.log("[X] 'Changes: x of N' values are not identical:", "error")
            for fi in files_info:
                self.log(f"   - {fi['filename']}: {fi['index']} of {fi['total']}", "error")
            return
        declared_total = declared_totals.pop()
        actual_total = len(files_info)

        if declared_total != actual_total:
            self.log(
                f"[X] File count mismatch! Header says {declared_total} files, but {actual_total} found.",
                "error"
            )
            return
        self.log(f"[OK] File count matches header: {actual_total}", "info")

        # 4. Check index sequence 1..N
        indices = sorted(fi["index"] for fi in files_info)
        expected = list(range(1, declared_total + 1))
        if indices != expected:
            self.log(f"[X] Changes indices are not complete/unique. Expected: {expected}", "error")
            self.log(f"   Got: {indices}", "error")
            return
        self.log("[OK] Changes index sequence is valid.\n", "info")

        # 5. Deploy files
        self.log("--- Starting file deployment ---", "info")
        new_files = []
        modified_files = []
        failed = []

        for fi in sorted(files_info, key=lambda x: x["index"]):
            rel = fi["location"].lstrip("/").replace("/", os.sep)
            target = os.path.join(dst, rel)
            target_dir = os.path.dirname(target)

            try:
                os.makedirs(target_dir, exist_ok=True)
            except Exception as e:
                failed.append(f"{fi['filename']}: failed to create dir - {e}")
                continue

            existed = os.path.exists(target)
            try:
                with open(target, "w", encoding="utf-8") as f:
                    f.write(fi["content"])
            except Exception as e:
                failed.append(f"{fi['filename']}: failed to write - {e}")
                continue

            if existed:
                modified_files.append((fi, target))
            else:
                new_files.append((fi, target))

        # 6. Final report
        self.log("\n--- NEW FILES (created) ---", "info")
        if new_files:
            for fi, t in new_files:
                self.log(f"  + [{fi['index']}/{fi['total']}] {fi['location']}", "new")
        else:
            self.log("  (no new files created)")

        self.log("\n--- MODIFIED FILES (updated) ---", "info")
        if modified_files:
            for fi, t in modified_files:
                self.log(f"  ~ [{fi['index']}/{fi['total']}] {fi['location']}", "modified")
        else:
            self.log("  (no files were modified)")

        if failed:
            self.log("\n--- ERRORS ---", "info")
            for e in failed:
                self.log("  [X] " + e, "error")

        self.log(
            f"\n=== Operation finished - New: {len(new_files)} | Modified: {len(modified_files)} | Failed: {len(failed)} ===",
            "info"
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()
