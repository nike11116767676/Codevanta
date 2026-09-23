# Codevanta — Intelligent Java & Python Code Analyzer

**Codevanta** is a specialized, full-stack programming analysis environment for **Java and Python** built with traditional software engineering, static analysis, compiler diagnostics, and deterministic rule engines.

> **Zero LLM / No External Generative AI**: 
> Codevanta does not use any OpenAI, Gemini, Claude, or cloud LLM APIs. Every syntax check, error diagnosis, correction diff, code health rating, and concept quiz is produced deterministically via the installed JDK (`javac`/`java`), Python runtime (`ast`/`compile`/`traceback`), pattern matchers, and a structured knowledge base.

---

## Key Features

1. **Integrated Developer IDE & Monaco Editor**:
   - Full Monaco Editor with syntax highlighting, line numbers, code folding, minimap, bracket pair colorization, and line error squiggles.
   - Real-time debounced live analysis (500ms) that highlights issues as you type.
   - Futuristic dark and light developer themes with high-contrast syntax tokens.
   - Command Palette (`Ctrl + K`) for instant navigation and action triggering.

2. **Real Compilation & Execution Engine**:
   - **Java Engine**: Direct invocation of `javac` and `java` in isolated sandboxes with microsecond-accurate timing (`time.perf_counter()`).
   - **Python Engine**: Direct execution via local Python interpreter with stdout/stderr capture and runtime traceback inspection.
   - Integrated terminal echoing real system commands (`$ javac Main.java`, `$ java Main`) and exit codes.

3. **Deterministic Error Analyzer**:
   - Parses compiler outputs and stacktraces to pinpoint exact **line** and **column**.
   - Identifies missing semicolons, unbalanced parentheses/brackets/braces, unclosed strings, type mismatches, undeclared symbols, and zero divisions.
   - Categorizes diagnostics into Syntax Errors, Compilation Errors, Runtime Errors, and Logic Warnings.

4. **Deterministic Correction Engine & Diff Viewer**:
   - Automatically repairs unambiguous syntax errors (e.g. missing `;` in Java statements, missing `:` in Python compound headers, unbalanced delimiters, name typos).
   - Shows a line-by-line before-and-after unified diff with added (`+`) and removed (`-`) lines.
   - **User in full control**: Click **[Apply Fix to Code]**, **[Undo]**, or **[Copy Corrected Code]**. Safe correction policy prevents destructive edits when ambiguous.

5. **Programming Teacher & Interactive Quiz**:
   - Explains errors in beginner-friendly language ("What happened?", "Why did it happen?", "Memory Rule").
   - Side-by-side Wrong Code vs. Correct Code comparisons.
   - Interactive multiple-choice quizzes with deterministic instant scoring and explanations.

6. **AST Code Intelligence & Dynamic Code Health**:
   - **Python AST**: Traversed using standard library `ast`.
   - **Java AST**: Traversed using `javalang`.
   - Structural counts for Classes, Methods, Variables, Loops, Conditions, and Imports.
   - Interactive hierarchical AST tree viewer.
   - **Genuine Code Health Score (0–100%)**: Dynamically calculated from errors, warnings, and branching complexity (never fake metrics).

7. **Process Isolation & Security Guard**:
   - Execution timeouts (default 5.0 seconds) guarding against infinite loops.
   - Destructive command filters preventing unauthorized operating system operations.

---

## Architecture & Directory Structure

```text
CODEVANTA/
├── backend/
│   ├── main.py                  # FastAPI app entry point & CORS
│   ├── config.py                # System timeouts & runtime paths
│   ├── database/
│   │   ├── db.py                # SQLite database manager & history
│   │   ├── errors.json          # Error knowledge base rules
│   │   ├── concepts.json        # Programming lessons & quizzes
│   │   └── models.py            # Pydantic models
│   ├── execution/
│   │   ├── java_executor.py     # javac/java compiler & runner
│   │   └── python_executor.py   # Python execution runner
│   ├── analyzers/
│   │   ├── error_parser.py      # Compiler output & traceback regex parsers
│   │   ├── java_analyzer.py     # Java syntax & static analyzer
│   │   └── python_analyzer.py   # Python syntax & static analyzer
│   ├── correction/
│   │   ├── java_corrector.py    # Java deterministic fix engine
│   │   ├── python_corrector.py  # Python deterministic fix engine
│   │   └── diff_generator.py    # Unified diff builder
│   ├── teaching/
│   │   └── (integrated via teaching routes & DB)
│   ├── ast_engine/
│   │   ├── java_ast.py          # Java AST parser (javalang)
│   │   └── python_ast.py        # Python AST parser (ast)
│   ├── security/
│   │   └── sandbox.py           # Subprocess timeout & security rules
│   └── routes/
│       ├── execution_routes.py  # POST /api/run
│       ├── analysis_routes.py   # POST /api/analyze, POST /api/live-analyze
│       ├── correction_routes.py # POST /api/correct
│       ├── teaching_routes.py   # GET /api/teach/{id}, POST /api/quiz/check
│       └── ast_routes.py        # POST /api/ast
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── TitleBar.jsx         # Language toggle, Run/Analyze/Fix buttons
    │   │   ├── Sidebar.jsx          # Navigation & Presets drawer
    │   │   ├── Editor.jsx           # Monaco Editor with diagnostics markers
    │   │   ├── Terminal.jsx         # Developer terminal with command echo
    │   │   ├── ErrorPanel.jsx       # Diagnostics cards with [Fix] [Explain]
    │   │   ├── CorrectionDiff.jsx   # Line-by-line diff with Apply Fix
    │   │   ├── TeachingPanel.jsx    # Concept explanations, examples, quiz
    │   │   ├── CodeIntelligence.jsx # Structural counts, AST tree, Code Health
    │   │   ├── CommandPalette.jsx   # Ctrl+K developer quick actions
    │   │   ├── AnalysisStages.jsx   # Sequential authentic analysis stages
    │   │   └── StatusBar.jsx        # Compiler/Interpreter status & metrics
    │   ├── services/
    │   │   └── api.js               # Axios API client
    │   ├── styles/
    │   │   ├── theme.css            # Dark/Light theme custom properties
    │   │   └── main.css             # Layout & futuristic IDE styling
    │   ├── utils/
    │   │   └── presets.js           # Test scenarios for Java & Python
    │   └── App.jsx                  # IDE Root application
    └── package.json
```

---

## Getting Started

### Prerequisites
- **Python 3.10+**
- **Java JDK 11+** (`javac` and `java` available on PATH)
- **Node.js 18+** and **npm**

### 1. Run the Backend Server
From the root directory:
```bash
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
API Documentation will be accessible at: `http://127.0.0.1:8000/docs`

### 2. Run the Frontend IDE
In another terminal:
```bash
cd frontend
npm install
npm run dev
```
Open your browser at: `http://127.0.0.1:5173`

---

## Keyboard Shortcuts
- `F5`: Compile & Run Code
- `Ctrl + K`: Open Developer Command Palette
