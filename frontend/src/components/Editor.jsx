import React, { useRef, useEffect } from 'react';
import MonacoEditor from '@monaco-editor/react';

export default function Editor({
  language,
  code,
  onChange,
  theme,
  markers = [],
  onFixError,
  onExplainError
}) {
  const editorRef = useRef(null);
  const monacoRef = useRef(null);

  const handleEditorDidMount = (editor, monaco) => {
    editorRef.current = editor;
    monacoRef.current = monaco;

    // Configure editor preferences
    editor.updateOptions({
      fontSize: 14,
      fontFamily: "'JetBrains Mono', 'Fira Code', Consolas, monospace",
      fontLigatures: true,
      minimap: { enabled: true, maxColumn: 80 },
      scrollBeyondLastLine: false,
      renderLineHighlight: 'all',
      bracketPairColorization: { enabled: true },
      lineNumbers: 'on',
      roundedSelection: true,
      cursorBlinking: 'smooth',
      smoothScrolling: true,
      tabSize: 4
    });

    // Register hover provider for Codevanta error explain/fix
    monaco.languages.registerHoverProvider(language, {
      provideHover: (model, position) => {
        const line = position.lineNumber;
        const activeMarker = markers.find(m => m.startLineNumber === line);
        if (activeMarker) {
          return {
            range: new monaco.Range(line, 1, line, model.getLineMaxColumn(line)),
            contents: [
              { value: `**Codevanta Diagnostic: ${activeMarker.title || 'Syntax Error'}**` },
              { value: activeMarker.message },
              { value: activeMarker.explanation ? `*${activeMarker.explanation}*` : '' }
            ]
          };
        }
        return null;
      }
    });
  };

  // Sync markers whenever markers state changes
  useEffect(() => {
    if (editorRef.current && monacoRef.current) {
      const model = editorRef.current.getModel();
      if (model) {
        monacoRef.current.editor.setModelMarkers(
          model,
          'codevanta',
          markers.map(m => ({
            startLineNumber: m.startLineNumber,
            startColumn: m.startColumn || 1,
            endLineNumber: m.endLineNumber || m.startLineNumber,
            endColumn: m.endColumn || 100,
            message: m.message,
            severity: m.severity === 'warning' 
              ? monacoRef.current.MarkerSeverity.Warning 
              : monacoRef.current.MarkerSeverity.Error
          }))
        );
      }
    }
  }, [markers]);

  return (
    <div className="editor-wrapper">
      <MonacoEditor
        height="100%"
        language={language === 'java' ? 'java' : 'python'}
        value={code}
        onChange={onChange}
        theme={theme === 'dark' ? 'vs-dark' : 'light'}
        onMount={handleEditorDidMount}
        options={{
          automaticLayout: true,
          quickSuggestions: true
        }}
      />
    </div>
  );
}
