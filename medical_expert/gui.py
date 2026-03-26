import tkinter as tk
from tkinter import ttk
from typing import Dict, List

from medical_expert.inference_engine import ForwardChainingEngine
from medical_expert.knowledge_base import DISEASE_RULES, SYMPTOM_QUESTIONS
from medical_expert.models import DiagnosisResult


SYMPTOM_GROUPS = {
    "General": ["fever", "fatigue", "headache", "body_ache"],
    "Respiratory": ["cough", "dry_cough", "runny_nose", "nasal_congestion", "sneezing"],
    "Throat": ["sore_throat", "painful_swallowing", "swollen_lymph_nodes"],
    "Allergy": ["itchy_eyes"],
    "Digestive": ["nausea", "vomiting", "diarrhea", "abdominal_cramps"],
    "Special": ["loss_of_taste_smell"],
}

# Modern color scheme
PRIMARY_COLOR = "#0D7377"
SECONDARY_COLOR = "#14919B"
ACCENT_COLOR = "#FF6B6B"
LIGHT_BG = "#F0F9FA"
CARD_BG = "#FFFFFF"
TEXT_DARK = "#1A3A3F"
TEXT_LIGHT = "#4A6F76"
BUTTON_HOVER = "#0A5A62"
SUCCESS_COLOR = "#22AB94"


class DiagnosisApp:
    """Modern Tkinter GUI for the medical diagnosis expert system."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Medical Diagnosis Expert System")
        self.root.geometry("900x700")
        self.root.minsize(750, 600)
        self.root.configure(bg=LIGHT_BG)

        self.engine = ForwardChainingEngine(DISEASE_RULES)
        self.symptom_vars: Dict[str, tk.BooleanVar] = {}
        self.selection_summary_var = tk.StringVar(value="Selected: 0 symptoms")

        self._configure_styles()
        self._build_layout()

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")

        # Main frame styles
        style.configure("App.TFrame", background=LIGHT_BG)
        style.configure("Card.TFrame", background=CARD_BG, relief="flat")
        
        # Title styles
        style.configure(
            "CardTitle.TLabel",
            background=CARD_BG,
            foreground=PRIMARY_COLOR,
            font=("Segoe UI", 14, "bold"),
        )
        style.configure(
            "CardSubTitle.TLabel",
            background=CARD_BG,
            foreground=TEXT_LIGHT,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Status.TLabel",
            background=CARD_BG,
            foreground=SUCCESS_COLOR,
            font=("Segoe UI", 10, "bold"),
        )
        
        # Button styles - Primary
        style.configure(
            "Accent.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=12,
            background=PRIMARY_COLOR,
            foreground="white",
        )
        style.map(
            "Accent.TButton",
            background=[("active", BUTTON_HOVER)],
        )
        
        # Button styles - Secondary
        style.configure(
            "Muted.TButton",
            font=("Segoe UI", 10),
            padding=10,
            background=LIGHT_BG,
            foreground=PRIMARY_COLOR,
            borderwidth=1,
        )
        style.map(
            "Muted.TButton",
            background=[("active", PRIMARY_COLOR)],
            foreground=[("active", "white")],
        )
        
        # Group styles
        style.configure(
            "Group.TLabelframe",
            background=CARD_BG,
            borderwidth=2,
            lightcolor=LIGHT_BG,
            darkcolor=LIGHT_BG,
        )
        style.configure(
            "Group.TLabelframe.Label",
            background=CARD_BG,
            foreground=PRIMARY_COLOR,
            font=("Segoe UI", 10, "bold"),
        )
        
        # Checkbutton style
        style.configure(
            "TCheckbutton",
            background=CARD_BG,
            foreground=TEXT_DARK,
            font=("Segoe UI", 10),
            focuscolor="none",
        )
        style.map(
            "TCheckbutton",
            background=[("active", LIGHT_BG)],
        )

    def _build_layout(self) -> None:
        # Main container
        main_container = ttk.Frame(self.root, style="App.TFrame", padding=0)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Header with gradient effect
        header = tk.Frame(main_container, bg=PRIMARY_COLOR, height=120)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        # Header content
        header_content = tk.Frame(header, bg=PRIMARY_COLOR)
        header_content.pack(fill=tk.BOTH, expand=True, padx=24, pady=16)

        title = tk.Label(
            header_content,
            text="Medical Diagnosis Expert System",
            bg=PRIMARY_COLOR,
            fg="white",
            font=("Segoe UI", 26, "bold"),
            anchor=tk.W,
        )
        title.pack(anchor=tk.W, pady=(0, 4))

        subtitle = tk.Label(
            header_content,
            text="AI-Powered Clinical Decision Support | Educational Purpose",
            bg=PRIMARY_COLOR,
            fg="#E0F2F1",
            font=("Segoe UI", 11),
            anchor=tk.W,
        )
        subtitle.pack(anchor=tk.W, pady=(0, 0))

        # Body with two columns
        body = ttk.Frame(main_container, style="App.TFrame", padding=20)
        body.pack(fill=tk.BOTH, expand=True)

        # Left column - Symptoms
        left_column = ttk.Frame(body, style="App.TFrame")
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        symptom_card = self._create_card(left_column)
        symptom_card.pack(fill=tk.BOTH, expand=True)

        symptom_title = tk.Label(
            symptom_card,
            text="Symptom Selection",
            bg=CARD_BG,
            fg=PRIMARY_COLOR,
            font=("Segoe UI", 13, "bold"),
            anchor=tk.W,
            padx=16,
        )
        symptom_title.pack(fill=tk.X, pady=(12, 4))

        symptom_subtitle = tk.Label(
            symptom_card,
            text="Select all symptoms observed",
            bg=CARD_BG,
            fg=TEXT_LIGHT,
            font=("Segoe UI", 9),
            anchor=tk.W,
            padx=16,
        )
        symptom_subtitle.pack(fill=tk.X, pady=(0, 12))

        self._build_scrollable_symptom_groups(symptom_card)

        # Action buttons
        action_frame = tk.Frame(symptom_card, bg=CARD_BG)
        action_frame.pack(fill=tk.X, padx=16, pady=(12, 0))

        diagnose_btn = ttk.Button(
            action_frame,
            text="Diagnose",
            style="Accent.TButton",
            command=self._run_diagnosis,
        )
        diagnose_btn.pack(side=tk.LEFT, padx=(0, 8))

        clear_btn = ttk.Button(
            action_frame,
            text="Clear",
            style="Muted.TButton",
            command=self._clear_selection,
        )
        clear_btn.pack(side=tk.LEFT, padx=4)

        profile_btn = ttk.Button(
            action_frame,
            text="Respiratory Set",
            style="Muted.TButton",
            command=self._apply_respiratory_profile,
        )
        profile_btn.pack(side=tk.LEFT, padx=4)

        # Status label
        status_frame = tk.Frame(symptom_card, bg=LIGHT_BG)
        status_frame.pack(fill=tk.X, padx=12, pady=(12, 12))

        status_label = tk.Label(
            status_frame,
            textvariable=self.selection_summary_var,
            bg=LIGHT_BG,
            fg=SUCCESS_COLOR,
            font=("Segoe UI", 10, "bold"),
            anchor=tk.W,
            padx=4,
            pady=6,
        )
        status_label.pack(fill=tk.X)

        # Right column - Results
        right_column = ttk.Frame(body, style="App.TFrame")
        right_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        result_card = self._create_card(right_column)
        result_card.pack(fill=tk.BOTH, expand=True)

        result_title = tk.Label(
            result_card,
            text="Diagnosis Results",
            bg=CARD_BG,
            fg=PRIMARY_COLOR,
            font=("Segoe UI", 13, "bold"),
            anchor=tk.W,
            padx=16,
        )
        result_title.pack(fill=tk.X, pady=(12, 4))

        result_subtitle = tk.Label(
            result_card,
            text="Ranked diagnoses with confidence scores",
            bg=CARD_BG,
            fg=TEXT_LIGHT,
            font=("Segoe UI", 9),
            anchor=tk.W,
            padx=16,
        )
        result_subtitle.pack(fill=tk.X, pady=(0, 12))

        # Output text area with better styling
        output_wrap = tk.Frame(result_card, bg=CARD_BG)
        output_wrap.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        scrollbar = ttk.Scrollbar(output_wrap, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_text = tk.Text(
            output_wrap,
            wrap=tk.WORD,
            height=25,
            font=("Consolas", 10),
            bg="#F8FBFC",
            fg=TEXT_DARK,
            relief=tk.FLAT,
            padx=12,
            pady=12,
            yscrollcommand=scrollbar.set,
            insertbackground=PRIMARY_COLOR,
            selectbackground=SECONDARY_COLOR,
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.configure(command=self.output_text.yview)

        # Text tags for rich formatting
        self.output_text.tag_configure("heading", font=("Segoe UI", 12, "bold"), foreground=PRIMARY_COLOR)
        self.output_text.tag_configure("disease", font=("Segoe UI", 11, "bold"), foreground=ACCENT_COLOR)
        self.output_text.tag_configure("meta", foreground=TEXT_LIGHT, font=("Segoe UI", 10))
        self.output_text.tag_configure("warn", foreground=ACCENT_COLOR, font=("Segoe UI", 10, "bold"))
        self.output_text.tag_configure("ok", foreground=SUCCESS_COLOR, font=("Segoe UI", 10, "bold"))

        self._render_welcome_message()

    def _create_card(self, parent: tk.Widget) -> tk.Frame:
        """Create a card with shadow effect."""
        card = tk.Frame(parent, bg=CARD_BG, relief=tk.RAISED, borderwidth=1)
        card.configure(highlightbackground=LIGHT_BG, highlightthickness=1)
        return card

    def _build_scrollable_symptom_groups(self, parent: tk.Frame) -> None:
        canvas_wrap = tk.Frame(parent, bg=CARD_BG)
        canvas_wrap.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        canvas = tk.Canvas(
            canvas_wrap,
            bg=CARD_BG,
            highlightthickness=0,
            relief=tk.FLAT,
        )
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(canvas_wrap, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        body = tk.Frame(canvas, bg=CARD_BG)
        window_id = canvas.create_window((0, 0), window=body, anchor="nw")

        def _resize_canvas(_: tk.Event) -> None:
            canvas.configure(scrollregion=canvas.bbox("all"))

        def _resize_window(event: tk.Event) -> None:
            canvas.itemconfig(window_id, width=event.width)

        body.bind("<Configure>", _resize_canvas)
        canvas.bind("<Configure>", _resize_window)

        # Add symptom groups
        for idx, (group_name, symptom_names) in enumerate(SYMPTOM_GROUPS.items()):
            section = tk.LabelFrame(
                body,
                text=f"  {group_name}  ",
                bg=LIGHT_BG,
                fg=PRIMARY_COLOR,
                font=("Segoe UI", 10, "bold"),
                padx=12,
                pady=8,
                relief=tk.FLAT,
                borderwidth=1,
                highlightthickness=0,
            )
            section.pack(fill=tk.X, pady=8, padx=0)

            for symptom_key in symptom_names:
                prompt = SYMPTOM_QUESTIONS[symptom_key]
                label_text = self._friendly_symptom_label(prompt)

                var = tk.BooleanVar(value=False)
                self.symptom_vars[symptom_key] = var

                check = tk.Checkbutton(
                    section,
                    text=label_text,
                    variable=var,
                    command=self._update_selection_summary,
                    bg=LIGHT_BG,
                    fg=TEXT_DARK,
                    font=("Segoe UI", 10),
                    activebackground=LIGHT_BG,
                    activeforeground=PRIMARY_COLOR,
                    selectcolor=LIGHT_BG,
                    highlightthickness=0,
                    anchor=tk.W,
                )
                check.pack(anchor=tk.W, pady=2, padx=0)

    @staticmethod
    def _friendly_symptom_label(question: str) -> str:
        cleaned = question.strip().rstrip("?")
        for prefix in ("Do you have ", "Did you ", "Is ", "Do you feel "):
            if cleaned.startswith(prefix):
                cleaned = cleaned.replace(prefix, "", 1)
                break
        return cleaned[:1].upper() + cleaned[1:]

    def _update_selection_summary(self) -> None:
        selected_count = sum(1 for var in self.symptom_vars.values() if var.get())
        if selected_count == 1:
            self.selection_summary_var.set(f"✓ Selected: {selected_count} symptom")
        else:
            self.selection_summary_var.set(f"✓ Selected: {selected_count} symptoms")

    def _render_welcome_message(self) -> None:
        self._reset_output()
        self.output_text.insert(tk.END, "Welcome to TechSquad MediDiagnosis\n", "heading")
        self.output_text.insert(tk.END, "\n")
        self.output_text.insert(
            tk.END,
            "Select symptoms from the left panel and click the Diagnose button to receive AI-powered diagnostic suggestions.\n\n",
            "meta",
        )
        self.output_text.insert(tk.END, "Quick Start:\n", "heading")
        self.output_text.insert(
            tk.END,
            "1. Check symptoms from the categories\n"
            "2. Click 'Diagnose' to analyze\n"
            "3. Review ranked diagnoses with confidence scores\n\n",
            "meta",
        )
        self.output_text.insert(
            tk.END,
            "Disclaimer: This system is for educational purposes only and should never replace professional medical consultation.\n",
            "warn",
        )
        self.output_text.configure(state=tk.DISABLED)

    def _run_diagnosis(self) -> None:
        facts = {symptom: var.get() for symptom, var in self.symptom_vars.items()}
        self._update_selection_summary()

        if not any(facts.values()):
            self._reset_output()
            self.output_text.insert(tk.END, "No symptoms selected\n", "heading")
            self.output_text.insert(
                tk.END,
                "Please select at least one symptom from the left panel before running diagnosis.\n",
                "warn",
            )
            self.output_text.configure(state=tk.DISABLED)
            return

        results = self.engine.diagnose(facts)
        self._render_results(results)

    def _clear_selection(self) -> None:
        for var in self.symptom_vars.values():
            var.set(False)
        self._update_selection_summary()
        self._render_welcome_message()

    def _apply_respiratory_profile(self) -> None:
        respiratory = set(SYMPTOM_GROUPS["Respiratory"]) | {"sore_throat", "fever", "fatigue"}

        for symptom_name, var in self.symptom_vars.items():
            var.set(symptom_name in respiratory)

        self._update_selection_summary()
        self._reset_output()
        self.output_text.insert(tk.END, "✓ Respiratory Profile Applied\n", "heading")
        self.output_text.insert(
            tk.END,
            "A pre-configured respiratory symptom set has been selected for demonstration. You can modify it before diagnosis.\n\n",
            "meta",
        )
        self.output_text.insert(
            tk.END,
            "Selected symptoms: Cough, nasal congestion, sore throat, fever, fatigue, and related respiratory symptoms.\n",
            "ok",
        )
        self.output_text.configure(state=tk.DISABLED)

    def _render_results(self, diagnoses: List[DiagnosisResult]) -> None:
        self._reset_output()

        if not diagnoses:
            self.output_text.insert(tk.END, "No Strong Diagnosis Inferred\n", "heading")
            self.output_text.insert(
                tk.END,
                "The selected symptoms do not strongly match any known disease patterns.\n"
                "Try selecting additional or different symptoms.\n",
                "warn",
            )
            self.output_text.configure(state=tk.DISABLED)
            return

        self.output_text.insert(tk.END, "Diagnostic Analysis Results\n", "heading")
        self.output_text.insert(
            tk.END,
            f"Analysis of {sum(1 for v in self.symptom_vars.values() if v.get())} symptom(s) - Ranked by confidence\n",
            "meta",
        )
        self.output_text.insert(tk.END, "\n" + "─" * 60 + "\n\n")

        for idx, result in enumerate(diagnoses, start=1):
            required = ", ".join(result.matched_required) if result.matched_required else "None"
            optional = ", ".join(result.matched_optional) if result.matched_optional else "None"

            confidence_bar = self._create_confidence_bar(result.confidence)

            self.output_text.insert(tk.END, f"{idx}. ", "disease")
            self.output_text.insert(tk.END, f"{result.disease}\n", "disease")
            self.output_text.insert(tk.END, f"    Confidence: {confidence_bar} {result.confidence}%\n", "ok")
            self.output_text.insert(tk.END, f"    Required match:  {required}\n")
            self.output_text.insert(tk.END, f"    Optional match:  {optional}\n")
            self.output_text.insert(tk.END, f"    Reasoning: {result.explanation}\n")
            self.output_text.insert(tk.END, "\n")

        self.output_text.insert(tk.END, "─" * 60 + "\n\n")
        self.output_text.insert(
            tk.END,
            "Disclaimer: This tool provides educational decision support only. "
            "It is NOT a substitute for professional medical advice. Always consult with qualified healthcare providers.\n",
            "warn",
        )
        self.output_text.configure(state=tk.DISABLED)

    @staticmethod
    def _create_confidence_bar(confidence: int) -> str:
        """Create a visual confidence bar."""
        filled = int(confidence / 10)
        empty = 10 - filled
        return f"[{'█' * filled}{'░' * empty}]"

    def _reset_output(self) -> None:
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)


def run_gui() -> None:
    root = tk.Tk()
    DiagnosisApp(root)
    root.mainloop()
