import React from 'react';
import { Cpu, FileCode, CheckCircle2, ShieldCheck } from 'lucide-react';

export default function StatusBar({
  language,
  lineCount,
  charCount,
  systemInfo,
  analyzerState = 'Ready'
}) {
  const runtimeVersion = language === 'java' 
    ? (systemInfo?.javac_version || 'Java 17') 
    : `Python ${systemInfo?.python_version || '3.14'}`;

  return (
    <footer className="status-bar">
      <div className="status-group">
        <div className="status-item" title="Active Language & Runtime Version">
          <FileCode size={13} color="var(--accent-cyan)" />
          <span>{runtimeVersion}</span>
        </div>
        <div className="status-item">
          <span>UTF-8</span>
        </div>
        <div className="status-item">
          <span>{lineCount} lines, {charCount} chars</span>
        </div>
      </div>

      <div className="status-group">
        <div className="status-item" title="Deterministic Engine without LLMs">
          <ShieldCheck size={13} color="var(--accent-emerald)" />
          <span>Deterministic Analyzer: {analyzerState}</span>
        </div>
        <div className="status-item">
          <Cpu size={13} color="var(--accent-cyan)" />
          <span>{language === 'java' ? 'javac: Connected' : 'Python: Connected'}</span>
        </div>
      </div>
    </footer>
  );
}
