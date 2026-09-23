import React, { useState } from 'react';
import { GraduationCap, Lightbulb, CheckCircle2, XCircle, HelpCircle, BookOpen } from 'lucide-react';
import { checkQuizAnswer } from '../services/api';

export default function TeachingPanel({ teachingData }) {
  const [selectedOption, setSelectedOption] = useState(null);
  const [quizResult, setQuizResult] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!teachingData) {
    return (
      <div className="panel-body" style={{ textAlign: 'center', padding: '30px 14px' }}>
        <GraduationCap size={34} color="var(--accent-cyan)" style={{ marginBottom: '10px' }} />
        <div style={{ fontWeight: 600, fontSize: '13px', color: 'var(--text-primary)', marginBottom: '4px' }}>
          Interactive Programming Teacher
        </div>
        <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
          Click [Explain] or [Learn Concept] on any error diagnostic to access concept lessons, code comparisons, and quizzes.
        </div>
      </div>
    );
  }

  const { title, what_happened, why_it_happened, wrong_example, correct_example, memory_rule, quiz } = teachingData;

  const handleOptionSelect = (optId) => {
    setSelectedOption(optId);
    setQuizResult(null);
  };

  const handleQuizSubmit = async () => {
    if (!selectedOption || !quiz) return;
    setIsSubmitting(true);
    try {
      const res = await checkQuizAnswer(quiz.question_id, selectedOption);
      setQuizResult(res);
    } catch (err) {
      console.error('Quiz submit failed:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

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
        <GraduationCap size={16} color="var(--accent-cyan)" />
        <span style={{ fontSize: '12px', fontWeight: 700, letterSpacing: '0.5px' }}>
          TEACHING LAB: {title.toUpperCase()}
        </span>
      </div>

      {/* What Happened Section */}
      <div style={{ marginBottom: '14px' }}>
        <div style={{ fontSize: '11px', fontWeight: 700, color: 'var(--accent-cyan)', textTransform: 'uppercase', marginBottom: '4px' }}>
          What Happened?
        </div>
        <div style={{ fontSize: '12px', color: 'var(--text-primary)', lineHeight: 1.5, background: 'var(--bg-primary)', padding: '10px', borderRadius: '6px', border: '1px solid var(--border-subtle)' }}>
          {what_happened}
        </div>
      </div>

      {/* Why Did It Happen Section */}
      <div style={{ marginBottom: '14px' }}>
        <div style={{ fontSize: '11px', fontWeight: 700, color: 'var(--accent-blue)', textTransform: 'uppercase', marginBottom: '4px' }}>
          Why Did It Happen? (Language Rule)
        </div>
        <div style={{ fontSize: '12px', color: 'var(--text-secondary)', lineHeight: 1.5, background: 'var(--bg-primary)', padding: '10px', borderRadius: '6px', border: '1px solid var(--border-subtle)' }}>
          {why_it_happened}
        </div>
      </div>

      {/* Code Comparison: Wrong vs Correct */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginBottom: '14px' }}>
        <div>
          <div style={{ fontSize: '10px', fontWeight: 700, color: 'var(--accent-rose)', textTransform: 'uppercase', marginBottom: '3px' }}>
            ✕ Incorrect Syntax
          </div>
          <pre style={{
            fontSize: '11px',
            fontFamily: 'var(--font-mono)',
            padding: '8px 10px',
            borderRadius: '6px',
            background: 'rgba(244, 63, 94, 0.08)',
            border: '1px solid rgba(244, 63, 94, 0.3)',
            color: '#fca5a5',
            overflowX: 'auto'
          }}>
            {wrong_example}
          </pre>
        </div>

        <div>
          <div style={{ fontSize: '10px', fontWeight: 700, color: 'var(--accent-emerald)', textTransform: 'uppercase', marginBottom: '3px' }}>
            ✓ Correct Syntax
          </div>
          <pre style={{
            fontSize: '11px',
            fontFamily: 'var(--font-mono)',
            padding: '8px 10px',
            borderRadius: '6px',
            background: 'rgba(16, 185, 129, 0.08)',
            border: '1px solid rgba(16, 185, 129, 0.3)',
            color: '#86efac',
            overflowX: 'auto'
          }}>
            {correct_example}
          </pre>
        </div>
      </div>

      {/* Memory Rule Box */}
      <div style={{
        background: 'linear-gradient(135deg, rgba(0, 240, 255, 0.08), rgba(99, 102, 241, 0.08))',
        border: '1px solid var(--border-bright)',
        borderRadius: '6px',
        padding: '10px 12px',
        marginBottom: '16px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '4px' }}>
          <Lightbulb size={13} color="var(--accent-cyan)" />
          <span style={{ fontSize: '11px', fontWeight: 700, color: 'var(--accent-cyan)', textTransform: 'uppercase' }}>
            Memory Rule
          </span>
        </div>
        <div style={{ fontSize: '12px', fontWeight: 500, color: 'var(--text-primary)' }}>
          {memory_rule}
        </div>
      </div>

      {/* Interactive Quiz */}
      {quiz && (
        <div style={{
          background: 'var(--bg-primary)',
          border: '1px solid var(--border-medium)',
          borderRadius: '8px',
          padding: '12px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px' }}>
            <HelpCircle size={14} color="var(--accent-amber)" />
            <span style={{ fontSize: '11px', fontWeight: 700, color: 'var(--accent-amber)', textTransform: 'uppercase' }}>
              Concept Quiz
            </span>
          </div>

          <div style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '10px', lineHeight: 1.4 }}>
            {quiz.question}
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', marginBottom: '10px' }}>
            {quiz.options.map((opt) => (
              <div
                key={opt.id}
                onClick={() => handleOptionSelect(opt.id)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  padding: '8px 10px',
                  borderRadius: '6px',
                  background: selectedOption === opt.id ? 'var(--bg-elevated)' : 'var(--bg-secondary)',
                  border: selectedOption === opt.id ? '1px solid var(--accent-cyan)' : '1px solid var(--border-subtle)',
                  cursor: 'pointer',
                  fontSize: '11px',
                  fontFamily: 'var(--font-mono)',
                  color: selectedOption === opt.id ? 'var(--accent-cyan)' : 'var(--text-primary)',
                  transition: 'all 0.15s ease'
                }}
              >
                <span style={{ fontWeight: 700 }}>{opt.id}.</span>
                <span>{opt.text}</span>
              </div>
            ))}
          </div>

          <button
            className="action-btn btn-analyze"
            style={{ width: '100%', justifyContent: 'center', fontSize: '11px', padding: '6px' }}
            disabled={!selectedOption || isSubmitting}
            onClick={handleQuizSubmit}
          >
            Check Answer
          </button>

          {quizResult && (
            <div style={{
              marginTop: '10px',
              padding: '8px 10px',
              borderRadius: '6px',
              background: quizResult.correct ? 'rgba(16, 185, 129, 0.1)' : 'rgba(244, 63, 94, 0.1)',
              border: `1px solid ${quizResult.correct ? 'var(--accent-emerald)' : 'var(--accent-rose)'}`,
              fontSize: '11px'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontWeight: 700, marginBottom: '4px', color: quizResult.correct ? 'var(--accent-emerald)' : 'var(--accent-rose)' }}>
                {quizResult.correct ? <CheckCircle2 size={13} /> : <XCircle size={13} />}
                <span>{quizResult.correct ? 'Correct! Excellent understanding.' : `Incorrect. The correct answer is ${quizResult.correct_option_id}.`}</span>
              </div>
              <div style={{ color: 'var(--text-secondary)' }}>
                {quizResult.explanation}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
