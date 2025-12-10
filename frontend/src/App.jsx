import React, { useState, useEffect } from 'react';
import { BarChart3 } from 'lucide-react';
import FormularioProyecto from './components/FormularioProyecto';
import ListaProyectos from './components/ListaProyectos';
import DetalleProyecto from './components/DetalleProyecto';
import { proyectoService } from './services/api';
import './App.css';

function App() {
  const [view, setView] = useState('main'); // 'main' o 'detail'
  const [proyectos, setProyectos] = useState([]);
  const [proyectoSeleccionado, setProyectoSeleccionado] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadProyectos();
  }, []);

  const loadProyectos = async () => {
    try {
      const response = await proyectoService.getAll();
      setProyectos(response.data);
    } catch (err) {
      setError('Error cargando proyectos');
    }
  };

  const handleProyectoCreado = (proyecto) => {
    setProyectos([...proyectos, proyecto]);
    setError('');
  };

  const handleSeleccionar = (proyecto) => {
    setProyectoSeleccionado(proyecto);
    setView('detail');
  };

  const handleAnalizar = async (id) => {
    setLoading(true);
    try {
      await proyectoService.analizar(id);
      await loadProyectos();
      if (proyectoSeleccionado?.id === id) {
        const updated = await proyectoService.getById(id);
        setProyectoSeleccionado(updated.data);
      }
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Error en análisis');
    } finally {
      setLoading(false);
    }
  };

  const handleEliminar = async (id) => {
    try {
      await proyectoService.delete(id);
      setProyectos(proyectos.filter(p => p.id !== id));
      if (proyectoSeleccionado?.id === id) {
        setProyectoSeleccionado(null);
        setView('main');
      }
    } catch (err) {
      setError('Error eliminando proyecto');
    }
  };

  const handleVolver = () => {
    setProyectoSeleccionado(null);
    setView('main');
  };

  return (
    <div className="app">
      <div className="app-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <BarChart3 size={48} strokeWidth={1.5} />
          <div>
            <h1>MetricISO</h1>
            <p>Dashboard automático de métricas ISO 29110/9001/25010/9241</p>
          </div>
        </div>
      </div>

      {error && (
        <div className="app-error">
          {error}
          <button onClick={() => setError('')}>×</button>
        </div>
      )}

      {view === 'main' ? (
        <div className="main-view">
          <div className="main-grid">
            <div className="form-column">
              <FormularioProyecto onProyectoCreado={handleProyectoCreado} />
            </div>
            <div className="projects-column">
              <ListaProyectos
                proyectos={proyectos}
                onSeleccionar={handleSeleccionar}
                onAnalizar={handleAnalizar}
                onEliminar={handleEliminar}
                loading={loading}
              />
            </div>
          </div>
        </div>
      ) : (
        <DetalleProyecto
          proyecto={proyectoSeleccionado}
          onVolver={handleVolver}
          onAnalizar={handleAnalizar}
          onEliminar={handleEliminar}
          loading={loading}
        />
      )}
    </div>
  );
}

export default App;
