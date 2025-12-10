import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

export const proyectoService = {
  getAll: () => API.get('/proyectos'),
  getById: (id) => API.get(`/proyectos/${id}`),
  create: (data) => API.post('/proyectos', data),
  analizar: (id) => API.post(`/proyectos/${id}/analizar`),
  delete: (id) => API.delete(`/proyectos/${id}`),
  getHistorico: (id) => API.get(`/proyectos/${id}/historico`)
};

export const formulaService = {
  getAll: () => API.get('/formulas'),
  getById: (codigo) => API.get(`/formulas/${codigo}`),
  calcular: (codigo, data) => API.post(`/formulas/${codigo}/calcular`, data)
};
