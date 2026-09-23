import React, { useRef, useEffect } from 'react';
import { Terminal as TerminalIcon, Trash2, Copy, Check, Clock } from 'lucide-react';

export default function Terminal({ logs, onClear }) {
  const terminalEndRef = useRef(null);
  const [copied, setCopied] = React.useState(false);

  useEffect(() => {
    if (terminalEndRef.current) {
      terminalEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [logs]);

  const handleCopy = () => {
    if (!logs || logs.length === 0) return;
    const text = logs.map(l => `${l.command || ''}\n${l.output || ''}\n${l.error_output || ''}`).join('\n');
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="terminal-container">
      <div className="terminal-header">
        <div className="terminal-title">
          <TerminalIcon size={14} color="var(--accent-cyan)" />
          <span>EXECUTION TERMINAL</span>
          {logs.length > 0 && logs[logs.length - 1].execution_time !== undefined && (
            <span style={{ display: 'flex', alignItems: 'center', gap: '4px', marginLeft: '12px', color: 'var(--text-muted)' }}>
              <Clock size={12} />
              <span>{logs[logs.length - 1].execution_time.toFixed(3)}s</span>
            </span>
          )}
        </div>
        <div className="terminal-actions">
          <button className="term-action-btn" onClick={handleCopy} title="Copy Output">
            {copied ? <Check size={13} color="var(--accent-emerald)" /> : <Copy size={13} />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>
          <button className="term-action-btn" onClick={onClear} title="Clear Terminal">
            <Trash2 size={13} />
            <span>Clear</span>
          </button>
        </div>
      </div>

      <div className="terminal-body">
        {logs.length === 0 ? (
          <div style={{ color: 'var(--text-dim)', fontStyle: 'italic', padding: '10px 0' }}>
            Ready to execute. Click 'Run Code' or press F5 to compile and execute program.
          </div>
        ) : (
          logs.map((entry, index) => (
            <div key={index} style={{ marginBottom: '14px' }}>
              {entry.command && (
                <div className="term-line-cmd">
                  {entry.command.split('\n').map((cmdLine, i) => (
                    <div key={i}>{cmdLine}</div>
                  ))}
                </div>
              )}
              {entry.output && (
                <div className="term-line-stdout">{entry.output}</div>
              )}
              {entry.error_output && (
                <div className="term-line-stderr">{entry.error_output}</div>
              )}
              {entry.status && (
                <div style={{ marginTop: '6px' }}>
                  {entry.status === 'success' && (
                    <span className="term-status-badge badge-success">
                      ✓ Program completed successfully (exit code {entry.exit_code})
                    </span>
                  )}
                  {entry.status === 'compilation_error' && (
                    <span className="term-status-badge badge-error">
                      ✕ Compilation failed with exit code {entry.exit_code}
                    </span>
                  )}
                  {entry.status === 'runtime_error' && (
                    <span className="term-status-badge badge-error">
                      ✕ Runtime error occurred (exit code {entry.exit_code})
                    </span>
                  )}
                  {entry.status === 'timeout' && (
                    <span className="term-status-badge badge-timeout">
                      ⚠ Execution terminated: process timed out
                    </span>
                  )}
                </div>
              )}
            </div>
          ))
        )}
        <div ref={terminalEndRef} />
      </div>
    </div>
  );
}
