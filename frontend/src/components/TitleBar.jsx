import React from 'react';
import { 
  Play, 
  Cpu, 
  Wrench, 
  Sun, 
  Moon, 
  Terminal as TermIcon, 
  Command, 
  CheckCircle2, 
  AlertCircle, 
  Loader2 
} from 'lucide-react';

export default function TitleBar({
  language,
  setLanguage,
  onRun,
  onAnalyze,
  onCorrect,
  isRunning,
  isAnalyzing,
  isCorrecting,
  theme,
  setTheme,
  systemStatus,
  onOpenCommandPalette
}) {
  return (
    <header className="titlebar">
      <div className="brand-section">
        <div className="brand-logo">
          <Cpu size={18} color="var(--accent-cyan)" />
          <span>CODEVANTA</span>
        </div>
        <span className="brand-badge">Deterministic Engine</span>

        <div className="language-selector">
          <button
            className={`lang-btn ${language === 'java' ? 'active' : ''}`}
            onClick={() => setLanguage('java')}
            title="Switch to Java environment"
          >
            Java
          </button>
          <button
            className={`lang-btn ${language === 'python' ? 'active' : ''}`}
            onClick={() => setLanguage('python')}
            title="Switch to Python environment"
          >
            Python
          </button>
        </div>
      </div>

      <div className="actions-toolbar">
        <button
          className="action-btn btn-run"
          onClick={onRun}
          disabled={isRunning || isAnalyzing}
          title="Compile and execute program (F5)"
        >
          {isRunning ? (
            <>
              <Loader2 size={14} className="spin-icon" />
              <span>Running...</span>
            </>
          ) : (
            <>
              <Play size={14} fill="currentColor" />
              <span>Run Code</span>
            </>
          )}
        </button>

        <button
          className="action-btn btn-analyze"
          onClick={onAnalyze}
          disabled={isRunning || isAnalyzing}
          title="Perform static & compiler error analysis"
        >
          {isAnalyzing ? (
            <>
              <Loader2 size={14} className="spin-icon" />
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              <TermIcon size={14} />
              <span>Analyze</span>
            </>
          )}
        </button>

        <button
          className="action-btn btn-correct"
          onClick={onCorrect}
          disabled={isRunning || isAnalyzing || isCorrecting}
          title="Generate deterministic auto-corrections"
        >
          {isCorrecting ? (
            <>
              <Loader2 size={14} className="spin-icon" />
              <span>Fixing...</span>
            </>
          ) : (
            <>
              <Wrench size={14} />
              <span>Auto-Fix</span>
            </>
          )}
        </button>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <button 
          className="action-btn"
          onClick={onOpenCommandPalette}
          title="Open Command Palette (Ctrl+K)"
          style={{ padding: '4px 8px' }}
        >
          <Command size={13} />
          <span style={{ fontSize: '11px' }}>Ctrl+K</span>
        </button>

        <div className="system-status">
          <div 
            className={`status-dot ${isRunning || isAnalyzing ? 'busy' : systemStatus === 'online' ? '' : 'error'}`} 
          />
          <span>{systemStatus === 'online' ? 'Engine Ready' : 'Connecting...'}</span>
        </div>

        <button
          className="nav-item"
          style={{ width: '32px', height: '32px' }}
          onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
          title="Toggle Dark / Light Theme"
        >
          {theme === 'dark' ? <Sun size={15} /> : <Moon size={15} />}
        </button>
      </div>
    </header>
  );
}
