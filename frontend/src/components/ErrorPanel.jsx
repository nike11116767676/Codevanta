import React from 'react';
import { AlertCircle, AlertTriangle, Info, CheckCircle2, Wrench, BookOpen } from 'lucide-react';

export default function ErrorPanel({
  errors = [],
  warnings = [],
  summary = '',
  onFixError,
  onExplainError,
  onSelectLine
}) {
  const totalCount = errors.length + warnings.length;

  if (totalCount === 0) {
    return (
      <div className="panel-body" style={{ textAlign: 'center', padding: '30px 14px' }}>
        <CheckCircle2 size={36} color="var(--accent-emerald)" style={{ marginBottom: '10px' }} />
        <div style={{ fontWeight: 600, fontSize: '14px', color: 'var(--text-primary)', marginBottom: '4px' }}>
          Clean Code — No Issues Detected
        </div>
        <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
          All syntax and static rules passed compiler validation.
        </div>
      </div>
    );
  }

  return (
    <div className="panel-body">
      <div style={{ 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'space-between', 
        marginBottom: '12px',
        paddingBottom: '8px',
        borderBottom: '1px solid var(--border-subtle)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          {errors.length > 0 ? (
            <AlertCircle size={15} color="var(--accent-rose)" />
          ) : (
            <AlertTriangle size={15} color="var(--accent-amber)" />
          )}
          <span style={{ fontSize: '12px', fontWeight: 700, letterSpacing: '0.5px' }}>
            {errors.length > 0 ? `${errors.length} ERROR${errors.length > 1 ? 'S' : ''}` : ''}
            {errors.length > 0 && warnings.length > 0 ? ' • ' : ''}
            {warnings.length > 0 ? `${warnings.length} WARNING${warnings.length > 1 ? 'S' : ''}` : ''}
          </span>
        </div>
        <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>{summary}</span>
      </div>

      {/* Render Blocking Errors */}
      {errors.map((err, idx) => (
        <div 
          key={`err-${idx}`} 
          className="diag-card error"
          onClick={() => err.line && onSelectLine && onSelectLine(err.line)}
        >
          <div className="diag-header">
            <span className="diag-type" style={{ color: 'var(--accent-rose)' }}>
              Syntax Error
            </span>
            <span className="diag-location">
              Line {err.line}{err.column ? ` : Col ${err.column}` : ''}
            </span>
          </div>

          <div className="diag-title">{err.title}</div>
          <div className="diag-msg">{err.explanation}</div>

          <div style={{ 
            fontSize: '11px', 
            background: 'var(--bg-input)', 
            padding: '6px 8px', 
            borderRadius: '4px',
            border: '1px solid var(--border-subtle)',
            marginBottom: '10px',
            color: 'var(--text-secondary)'
          }}>
            <strong style={{ color: 'var(--accent-cyan)' }}>Suggestion: </strong>
            {err.solution}
          </div>

          <div className="diag-actions">
            <button 
              className="action-btn btn-correct" 
              style={{ fontSize: '11px', padding: '4px 10px' }}
              onClick={(e) => { e.stopPropagation(); onFixError && onFixError(err); }}
            >
              <Wrench size={12} />
              <span>Fix Error</span>
            </button>
            <button 
              className="action-btn" 
              style={{ fontSize: '11px', padding: '4px 10px' }}
              onClick={(e) => { e.stopPropagation(); onExplainError && onExplainError(err); }}
            >
              <BookOpen size={12} />
              <span>Explain</span>
            </button>
          </div>
        </div>
      ))}

      {/* Render Warnings & Lint */}
      {warnings.map((warn, idx) => (
        <div 
          key={`warn-${idx}`} 
          className="diag-card warning"
          onClick={() => warn.line && onSelectLine && onSelectLine(warn.line)}
        >
          <div className="diag-header">
            <span className="diag-type" style={{ color: 'var(--accent-amber)' }}>
              Warning
            </span>
            <span className="diag-location">
              Line {warn.line}{warn.column ? ` : Col ${warn.column}` : ''}
            </span>
          </div>

          <div className="diag-title">{warn.title}</div>
          <div className="diag-msg">{warn.explanation}</div>

          <div style={{ 
            fontSize: '11px', 
            background: 'var(--bg-input)', 
            padding: '6px 8px', 
            borderRadius: '4px',
            border: '1px solid var(--border-subtle)',
            marginBottom: '10px',
            color: 'var(--text-secondary)'
          }}>
            <strong style={{ color: 'var(--accent-amber)' }}>Advice: </strong>
            {warn.solution}
          </div>

          <div className="diag-actions">
            <button 
              className="action-btn" 
              style={{ fontSize: '11px', padding: '4px 10px' }}
              onClick={(e) => { e.stopPropagation(); onExplainError && onExplainError(warn); }}
            >
              <BookOpen size={12} />
              <span>Learn Concept</span>
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
