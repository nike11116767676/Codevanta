import axios from 'axios';

const API_BASE = 'https://codevanta-backend-zswn.onrender.com/api';

const client = axios.create({
  baseURL: API_BASE,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
});

export const checkHealth = async () => {
  const res = await client.get('/health');
  return res.data;
};

export const runCode = async (language, code, stdin_input = '') => {
  const res = await client.post('/run', {
    language,
    code,
    stdin_input
  });
  return res.data;
};

export const analyzeCode = async (language, code) => {
  const res = await client.post('/analyze', {
    language,
    code
  });
  return res.data;
};

export const liveAnalyze = async (language, code) => {
  const res = await client.post('/live-analyze', {
    language,
    code
  });
  return res.data;
};

export const correctCode = async (language, code) => {
  const res = await client.post('/correct', {
    language,
    code
  });
  return res.data;
};

export const getTeaching = async (error_id) => {
  const res = await client.get(`/teach/${error_id}`);
  return res.data;
};

export const checkQuizAnswer = async (question_id, selected_option_id) => {
  const res = await client.post('/quiz/check', {
    question_id,
    selected_option_id
  });
  return res.data;
};

export const getAST = async (language, code) => {
  const res = await client.post('/ast', {
    language,
    code
  });
  return res.data;
};
