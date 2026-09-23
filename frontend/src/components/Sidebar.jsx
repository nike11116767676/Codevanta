import React from 'react';
import { 
  FolderGit2, 
  AlertTriangle, 
  GitCompare, 
  GraduationCap, 
  History, 
  Settings,
  ChevronRight,
  Code2
} from 'lucide-react';
import { PRESETS } from '../utils/presets';

export default function Sidebar({
  activeTab,
  setActiveTab,
  language,
  onSelectPreset,
  errorCount,
  historyCount
}) {
  const presetsForLang = PRESETS[language] || [];

  return (
    <>
      <aside className="nav-sidebar">
        <div className="nav-sidebar-top">
          <button
            className={`nav-item ${activeTab === 'presets' ? 'active' : ''}`}
            onClick={() => setActiveTab(activeTab === 'presets' ? null : 'presets')}
            title="Code Templates & Test Scenarios"
          >
            <FolderGit2 size={18} />
          </button>

          <button
            className={`nav-item ${activeTab === 'analyzer' ? 'active' : ''}`}
            onClick={() => setActiveTab(activeTab === 'analyzer' ? null : 'analyzer')}
            title="Diagnostics & Error Analysis"
          >
            <AlertTriangle size={18} />
            {errorCount > 0 && (
              <span style={{
                position: 'absolute',
                top: 4,
                right: 4,
                width: 7,
                height: 7,
                borderRadius: '50%',
                backgroundColor: 'var(--accent-rose)'
              }} />
            )}
          </button>

          <button
            className={`nav-item ${activeTab === 'diff' ? 'active' : ''}`}
            onClick={() => setActiveTab(activeTab === 'diff' ? null : 'diff')}
            title="Deterministic Fixes & Code Diff"
          >
            <GitCompare size={18} />
          </button>

          <button
            className={`nav-item ${activeTab === 'learning' ? 'active' : ''}`}
            onClick={() => setActiveTab(activeTab === 'learning' ? null : 'learning')}
            title="Programming Concept Teaching & Quiz"
          >
            <GraduationCap size={18} />
          </button>

          <button
            className={`nav-item ${activeTab === 'history' ? 'active' : ''}`}
            onClick={() => setActiveTab(activeTab === 'history' ? null : 'history')}
            title="Execution & Correction History"
          >
            <History size={18} />
          </button>
        </div>

        <div className="nav-sidebar-bottom">
          <button
            className={`nav-item ${activeTab === 'settings' ? 'active' : ''}`}
            onClick={() => setActiveTab(activeTab === 'settings' ? null : 'settings')}
            title="IDE Settings"
          >
            <Settings size={18} />
          </button>
        </div>
      </aside>

      {/* Expandable Drawer */}
      {activeTab === 'presets' && (
        <div className="drawer-sidebar">
          <div className="drawer-header">
            <span>{language.toUpperCase()} SCENARIOS</span>
            <Code2 size={14} />
          </div>
          <div className="drawer-content">
            {presetsForLang.map((preset) => (
              <div
                key={preset.id}
                className="preset-card"
                onClick={() => onSelectPreset(preset.code)}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span className="preset-title">{preset.name}</span>
                  <span style={{
                    fontSize: '9px',
                    fontWeight: 700,
                    textTransform: 'uppercase',
                    color: preset.category === 'Working' ? 'var(--accent-emerald)' : 'var(--accent-amber)'
                  }}>
                    {preset.category}
                  </span>
                </div>
                <div className="preset-desc">{preset.description}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </>
  );
}
