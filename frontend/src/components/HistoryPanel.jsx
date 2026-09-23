import React from 'react';
import { History, AlertCircle, CheckCircle2, Clock } from 'lucide-react';

export default function HistoryPanel({ historyItems = [], onSelectSnippet }) {
  if (!historyItems || historyItems.length === 0) {
    return (
      <div className="panel-body" style={{ textAlign: 'center', padding: '30px 14px' }}>
        <History size={32} color="var(--accent-blue)" style={{ marginBottom: '10px' }} />
        <div style={{ fontWeight: 600, fontSize: '13px', color: 'var(--text-primary)', marginBottom: '4px' }}>
          No History Recorded
        </div>
        <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
          Analysis events and error detections are saved into SQLite database history.
        </div>
      </div>
    );
  }

  return (
    <div className="panel-body">
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '6px',
        marginBottom: '12px',
        paddingBottom: '8px',
        borderBottom: '1px solid var(--border-subtle)'
      }}>
        <History size={15} color="var(--accent-blue)" />
        <span style={{ fontSize: '12px', fontWeight: 700, letterSpacing: '0.5px' }}>
          ERROR & ANALYSIS HISTORY
        </span>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {historyItems.map((item, idx) => (
          <div
            key={idx}
            style={{
              background: 'var(--bg-primary)',
              border: '1px solid var(--border-subtle)',
              borderRadius: '6px',
              padding: '8px 10px',
              fontSize: '11px'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
              <span style={{ fontWeight: 700, color: 'var(--accent-cyan)', textTransform: 'uppercase' }}>
                {item.language} • {item.error_title || item.error_id}
              </span>
              <span style={{ color: 'var(--text-dim)', display: 'flex', alignItems: 'center', gap: '3px' }}>
                <Clock size={10} />
                {item.timestamp || 'Recent'}
              </span>
            </div>
            {item.line > 0 && (
              <div style={{ color: 'var(--text-muted)', marginBottom: '4px' }}>
                Line {item.line}
              </div>
            )}
            {item.code_snippet && (
              <pre style={{
                fontFamily: 'var(--font-mono)',
                fontSize: '10px',
                background: 'var(--bg-secondary)',
                padding: '4px 6px',
                borderRadius: '4px',
                color: 'var(--text-secondary)',
                overflowX: 'auto'
              }}>
                {item.code_snippet}
              </pre>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
