import React, { useState } from 'react';
import { GitCompare, Check, Copy, Undo, Wrench, AlertCircle } from 'lucide-react';

export default function CorrectionDiff({
  correctionData,
  onApplyFix,
  onDiscard
}) {
  const [copied, setCopied] = useState(false);

  if (!correctionData) {
    return (
      <div className="panel-body" style={{ textAlign: 'center', padding: '30px 14px' }}>
        <Wrench size={32} color="var(--accent-purple)" style={{ marginBottom: '10px' }} />
        <div style={{ fontWeight: 600, fontSize: '13px', color: 'var(--text-primary)', marginBottom: '4px' }}>
          No Active Correction
        </div>
        <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
          Click 'Auto-Fix' or [Fix Error] on any diagnostic to generate deterministic code corrections.
        </div>
      </div>
    );
  }

  const { can_auto_correct, message, changes, diff_unified, corrected_code } = correctionData;

  const handleCopy = () => {
    navigator.clipboard.writeText(corrected_code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

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
          <GitCompare size={15} color="var(--accent-purple)" />
          <span style={{ fontSize: '12px', fontWeight: 700, letterSpacing: '0.5px' }}>
            CORRECTION DIFF
          </span>
        </div>
        <div style={{ display: 'flex', gap: '6px' }}>
          {can_auto_correct && (
            <button 
              className="action-btn"
              onClick={handleCopy}
              style={{ fontSize: '11px', padding: '3px 8px' }}
              title="Copy Corrected Code"
            >
              {copied ? <Check size={12} color="var(--accent-emerald)" /> : <Copy size={12} />}
              <span>{copied ? 'Copied' : 'Copy'}</span>
            </button>
          )}
        </div>
      </div>

      <div style={{
        fontSize: '12px',
        padding: '8px 10px',
        borderRadius: '6px',
        background: can_auto_correct ? 'rgba(168, 85, 247, 0.1)' : 'rgba(245, 158, 11, 0.1)',
        border: `1px solid ${can_auto_correct ? 'var(--accent-purple)' : 'var(--accent-amber)'}`,
        color: 'var(--text-primary)',
        marginBottom: '12px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontWeight: 600 }}>
          {can_auto_correct ? <Check size={14} color="var(--accent-purple)" /> : <AlertCircle size={14} color="var(--accent-amber)" />}
          <span>{message}</span>
        </div>
      </div>

      {can_auto_correct && changes && changes.length > 0 && (
        <div style={{ marginBottom: '14px' }}>
          <div style={{ fontSize: '11px', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '6px', textTransform: 'uppercase' }}>
            Identified Modifications ({changes.length})
          </div>

          <div className="diff-container">
            {changes.map((chg, idx) => (
              <div key={idx} style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                <div style={{ fontSize: '10px', padding: '4px 8px', background: 'var(--bg-elevated)', color: 'var(--text-muted)' }}>
                  Line {chg.line} — {chg.description}
                </div>
                {chg.before && (
                  <div className="diff-line diff-del">
                    <span style={{ userSelect: 'none', width: '16px', color: 'var(--accent-rose)' }}>-</span>
                    <span>{chg.before}</span>
                  </div>
                )}
                {chg.after && (
                  <div className="diff-line diff-add">
                    <span style={{ userSelect: 'none', width: '16px', color: 'var(--accent-emerald)' }}>+</span>
                    <span>{chg.after}</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {can_auto_correct && (
        <div style={{ display: 'flex', gap: '10px', marginTop: '12px' }}>
          <button
            className="action-btn btn-run"
            style={{ flex: 1, justifyContent: 'center' }}
            onClick={() => onApplyFix && onApplyFix(corrected_code)}
          >
            <Check size={13} />
            <span>Apply Fix to Code</span>
          </button>
          <button
            className="action-btn"
            style={{ padding: '6px 12px' }}
            onClick={onDiscard}
            title="Discard Suggestion"
          >
            <Undo size={13} />
            <span>Discard</span>
          </button>
        </div>
      )}
    </div>
  );
}
