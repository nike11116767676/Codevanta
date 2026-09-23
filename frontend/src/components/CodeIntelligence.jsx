import React, { useState } from 'react';
import { 
  Activity, 
  Layers, 
  Code, 
  Variable, 
  Repeat, 
  GitFork, 
  Package, 
  ChevronDown, 
  ChevronRight,
  ShieldCheck,
  Cpu
} from 'lucide-react';

function ASTTreeNode({ node, depth = 0 }) {
  const [expanded, setExpanded] = useState(depth < 2);
  const hasChildren = node.children && node.children.length > 0;

  const getIcon = (type) => {
    switch (type) {
      case 'Class': return <Layers size={12} color="var(--accent-cyan)" />;
      case 'Method':
      case 'Function': return <Code size={12} color="var(--accent-blue)" />;
      case 'Variable': return <Variable size={12} color="var(--accent-purple)" />;
      case 'Loop': return <Repeat size={12} color="var(--accent-emerald)" />;
      case 'Condition': return <GitFork size={12} color="var(--accent-amber)" />;
      case 'Import': return <Package size={12} color="var(--text-muted)" />;
      default: return <Cpu size={12} color="var(--text-secondary)" />;
    }
  };

  return (
    <div style={{ marginLeft: depth * 14, fontSize: '11px', fontFamily: 'var(--font-mono)' }}>
      <div 
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '5px',
          padding: '2px 4px',
          borderRadius: '4px',
          cursor: hasChildren ? 'pointer' : 'default',
          color: 'var(--text-primary)',
          userSelect: 'none'
        }}
        onClick={() => hasChildren && setExpanded(!expanded)}
      >
        {hasChildren ? (
          expanded ? <ChevronDown size={11} color="var(--text-muted)" /> : <ChevronRight size={11} color="var(--text-muted)" />
        ) : (
          <span style={{ width: 11 }} />
        )}
        {getIcon(node.node_type)}
        <span style={{ fontWeight: hasChildren ? 600 : 400 }}>{node.name}</span>
        {node.line && (
          <span style={{ fontSize: '9px', color: 'var(--text-dim)', marginLeft: 'auto' }}>
            L{node.line}
          </span>
        )}
      </div>

      {hasChildren && expanded && (
        <div style={{ borderLeft: '1px solid var(--border-subtle)', marginLeft: '6px' }}>
          {node.children.map((child, idx) => (
            <ASTTreeNode key={idx} node={child} depth={depth + 1} />
          ))}
        </div>
      )}
    </div>
  );
}

export default function CodeIntelligence({ intelligenceData, errorCount, warningCount }) {
  if (!intelligenceData) {
    return (
      <div className="panel-body" style={{ textAlign: 'center', padding: '30px 14px' }}>
        <Activity size={32} color="var(--accent-cyan)" style={{ marginBottom: '10px' }} />
        <div style={{ fontWeight: 600, fontSize: '13px', color: 'var(--text-primary)', marginBottom: '4px' }}>
          Code Intelligence Ready
        </div>
        <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
          Run an analysis to inspect AST structure, metrics, and genuine code health.
        </div>
      </div>
    );
  }

  const { classes, methods, variables, loops, conditions, imports, health_score, ast_tree } = intelligenceData;

  const getHealthColor = (score) => {
    if (score >= 80) return 'var(--accent-emerald)';
    if (score >= 50) return 'var(--accent-amber)';
    return 'var(--accent-rose)';
  };

  return (
    <div className="panel-body">
      {/* Code Health Header */}
      <div style={{ marginBottom: '16px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <ShieldCheck size={14} color={getHealthColor(health_score)} />
            <span style={{ fontSize: '11px', fontWeight: 700, letterSpacing: '0.5px' }}>
              CODE HEALTH RATING
            </span>
          </div>
          <span style={{ fontSize: '14px', fontWeight: 700, fontFamily: 'var(--font-mono)', color: getHealthColor(health_score) }}>
            {health_score}%
          </span>
        </div>

        <div className="health-bar-bg">
          <div 
            className="health-bar-fill" 
            style={{ 
              width: `${health_score}%`, 
              backgroundColor: getHealthColor(health_score),
              boxShadow: `0 0 10px ${getHealthColor(health_score)}`
            }} 
          />
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '10px', color: 'var(--text-muted)', marginTop: '4px' }}>
          <span>Errors: {errorCount}</span>
          <span>Warnings: {warningCount}</span>
          <span>Branches: {loops + conditions}</span>
        </div>
      </div>

      {/* Structural Metrics Cards */}
      <div style={{ marginBottom: '16px' }}>
        <div style={{ fontSize: '11px', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '8px' }}>
          Structural Elements (AST)
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '8px' }}>
          <div style={{ background: 'var(--bg-primary)', padding: '8px', borderRadius: '6px', border: '1px solid var(--border-subtle)', textAlign: 'center' }}>
            <div style={{ fontSize: '16px', fontWeight: 700, color: 'var(--accent-cyan)' }}>{classes}</div>
            <div style={{ fontSize: '10px', color: 'var(--text-muted)' }}>Classes</div>
          </div>
          <div style={{ background: 'var(--bg-primary)', padding: '8px', borderRadius: '6px', border: '1px solid var(--border-subtle)', textAlign: 'center' }}>
            <div style={{ fontSize: '16px', fontWeight: 700, color: 'var(--accent-blue)' }}>{methods}</div>
            <div style={{ fontSize: '10px', color: 'var(--text-muted)' }}>Methods</div>
          </div>
          <div style={{ background: 'var(--bg-primary)', padding: '8px', borderRadius: '6px', border: '1px solid var(--border-subtle)', textAlign: 'center' }}>
            <div style={{ fontSize: '16px', fontWeight: 700, color: 'var(--accent-purple)' }}>{variables}</div>
            <div style={{ fontSize: '10px', color: 'var(--text-muted)' }}>Variables</div>
          </div>
          <div style={{ background: 'var(--bg-primary)', padding: '8px', borderRadius: '6px', border: '1px solid var(--border-subtle)', textAlign: 'center' }}>
            <div style={{ fontSize: '16px', fontWeight: 700, color: 'var(--accent-emerald)' }}>{loops}</div>
            <div style={{ fontSize: '10px', color: 'var(--text-muted)' }}>Loops</div>
          </div>
          <div style={{ background: 'var(--bg-primary)', padding: '8px', borderRadius: '6px', border: '1px solid var(--border-subtle)', textAlign: 'center' }}>
            <div style={{ fontSize: '16px', fontWeight: 700, color: 'var(--accent-amber)' }}>{conditions}</div>
            <div style={{ fontSize: '10px', color: 'var(--text-muted)' }}>Conditions</div>
          </div>
          <div style={{ background: 'var(--bg-primary)', padding: '8px', borderRadius: '6px', border: '1px solid var(--border-subtle)', textAlign: 'center' }}>
            <div style={{ fontSize: '16px', fontWeight: 700, color: 'var(--text-secondary)' }}>{imports}</div>
            <div style={{ fontSize: '10px', color: 'var(--text-muted)' }}>Imports</div>
          </div>
        </div>
      </div>

      {/* Visual AST Hierarchy */}
      <div>
        <div style={{ fontSize: '11px', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '8px' }}>
          Abstract Syntax Tree (AST)
        </div>

        <div style={{ 
          background: 'var(--bg-primary)', 
          border: '1px solid var(--border-subtle)', 
          borderRadius: '6px', 
          padding: '10px',
          maxHeight: '260px',
          overflowY: 'auto'
        }}>
          {ast_tree ? (
            <ASTTreeNode node={ast_tree} depth={0} />
          ) : (
            <div style={{ fontSize: '11px', color: 'var(--text-dim)', fontStyle: 'italic' }}>
              AST tree unavailable due to syntax errors.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
