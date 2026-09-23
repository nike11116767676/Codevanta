import React, { useState, useEffect, useRef } from 'react';
import { Search, Play, Terminal, Wrench, GraduationCap, Sun, Moon, FileCode, Trash2, X } from 'lucide-react';

export default function CommandPalette({
  isOpen,
  onClose,
  onRun,
  onAnalyze,
  onCorrect,
  onToggleTheme,
  theme,
  language,
  onSetLanguage,
  onClearTerminal,
  onOpenPresets,
  onOpenLearning
}) {
  const [search, setSearch] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef(null);

  const commands = [
    { id: 'run', label: 'Run Code', icon: <Play size={14} color="var(--accent-emerald)" />, shortcut: 'F5', action: onRun },
    { id: 'analyze', label: 'Analyze Code for Errors', icon: <Terminal size={14} color="var(--accent-cyan)" />, shortcut: 'Ctrl+Shift+A', action: onAnalyze },
    { id: 'correct', label: 'Auto-Fix Detected Errors', icon: <Wrench size={14} color="var(--accent-purple)" />, shortcut: 'Ctrl+Shift+F', action: onCorrect },
    { id: 'learn', label: 'Learn Concept & Take Quiz', icon: <GraduationCap size={14} color="var(--accent-amber)" />, shortcut: '', action: onOpenLearning },
    { id: 'lang-java', label: 'Switch Environment to Java', icon: <FileCode size={14} color="var(--accent-cyan)" />, shortcut: '', action: () => onSetLanguage('java') },
    { id: 'lang-py', label: 'Switch Environment to Python', icon: <FileCode size={14} color="var(--accent-blue)" />, shortcut: '', action: () => onSetLanguage('python') },
    { id: 'presets', label: 'Open Preset Scenarios & Test Snippets', icon: <FileCode size={14} />, shortcut: '', action: onOpenPresets },
    { id: 'theme', label: `Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Theme`, icon: theme === 'dark' ? <Sun size={14} /> : <Moon size={14} />, shortcut: '', action: onToggleTheme },
    { id: 'clear', label: 'Clear Execution Terminal', icon: <Trash2 size={14} />, shortcut: '', action: onClearTerminal }
  ];

  const filteredCommands = commands.filter(c => 
    c.label.toLowerCase().includes(search.toLowerCase())
  );

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
      setSearch('');
      setSelectedIndex(0);
    }
  }, [isOpen]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (!isOpen) return;

      if (e.key === 'Escape') {
        onClose();
      } else if (e.key === 'ArrowDown') {
        e.preventDefault();
        setSelectedIndex(prev => (prev + 1) % filteredCommands.length);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        setSelectedIndex(prev => (prev - 1 + filteredCommands.length) % filteredCommands.length);
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (filteredCommands[selectedIndex]) {
          filteredCommands[selectedIndex].action();
          onClose();
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, filteredCommands, selectedIndex, onClose]);

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="command-palette" onClick={e => e.stopPropagation()}>
        <div className="palette-input-wrapper">
          <Search size={16} color="var(--text-muted)" />
          <input
            ref={inputRef}
            type="text"
            className="palette-input"
            placeholder="Type a command or search action..."
            value={search}
            onChange={e => { setSearch(e.target.value); setSelectedIndex(0); }}
          />
          <button 
            style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}
            onClick={onClose}
          >
            <X size={16} />
          </button>
        </div>

        <div className="palette-items">
          {filteredCommands.length === 0 ? (
            <div style={{ padding: '16px', textAlign: 'center', fontSize: '12px', color: 'var(--text-muted)' }}>
              No matching commands found.
            </div>
          ) : (
            filteredCommands.map((cmd, idx) => (
              <div
                key={cmd.id}
                className={`palette-item ${selectedIndex === idx ? 'selected' : ''}`}
                onClick={() => { cmd.action(); onClose(); }}
                onMouseEnter={() => setSelectedIndex(idx)}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  {cmd.icon}
                  <span>{cmd.label}</span>
                </div>
                {cmd.shortcut && (
                  <span className="palette-shortcut">{cmd.shortcut}</span>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
