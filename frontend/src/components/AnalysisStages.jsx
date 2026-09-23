import React from 'react';
import { CheckCircle2, Loader2, Circle } from 'lucide-react';

const STAGES = [
  'Initializing analyzer...',
  'Parsing source code...',
  'Building syntax tree...',
  'Checking syntax & tokens...',
  'Checking variable scopes...',
  'Checking types & symbols...',
  'Matching error knowledge base...',
  'Analysis complete'
];

export default function AnalysisStages({ currentStageIndex }) {
  return (
    <div style={{
      background: 'var(--bg-primary)',
      border: '1px solid var(--border-medium)',
      borderRadius: '8px',
      padding: '16px',
      margin: '12px',
      boxShadow: 'var(--shadow-md)'
    }}>
      <div style={{
        fontSize: '11px',
        fontWeight: 700,
        letterSpacing: '1px',
        color: 'var(--accent-cyan)',
        textTransform: 'uppercase',
        marginBottom: '12px'
      }}>
        Codevanta Diagnostic Pipeline
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {STAGES.map((stage, idx) => {
          const isDone = idx < currentStageIndex;
          const isCurrent = idx === currentStageIndex;

          return (
            <div
              key={idx}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                fontSize: '12px',
                color: isDone 
                  ? 'var(--accent-emerald)' 
                  : isCurrent 
                  ? 'var(--accent-cyan)' 
                  : 'var(--text-dim)',
                fontFamily: 'var(--font-mono)'
              }}
            >
              {isDone && <CheckCircle2 size={13} color="var(--accent-emerald)" />}
              {isCurrent && <Loader2 size={13} className="spin-icon" color="var(--accent-cyan)" />}
              {!isDone && !isCurrent && <Circle size={13} color="var(--text-dim)" />}
              <span>{stage}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
