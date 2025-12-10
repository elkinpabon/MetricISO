import React, { useState, useEffect } from 'react';
import FormularioProyecto from './components/FormularioProyecto';
import ListaProyectos from './components/ListaProyectos';
import DashboardMetricas from './components/DashboardMetricas';
import CalculadoraFormulas from './components/CalculadoraFormulas';
import { proyectoService } from './services/api';

function App() {
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
  };

  const handleAnalizar = async (id) => {
    setLoading(true);
    try {
      await proyectoService.analizar(id);
      await loadProyectos();
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Error en análisis');
    } finally {
      setLoading(false);
    }
  };

  const handleEliminar = async (id) => {
    if (window.confirm('¿Estás seguro de eliminar este proyecto?')) {
      try {
        await proyectoService.delete(id);
        setProyectos(proyectos.filter(p => p.id !== id));
        if (proyectoSeleccionado?.id === id) {
          setProyectoSeleccionado(null);
        }
      } catch (err) {
        setError('Error eliminando proyecto');
      }
    }
  };

  return (
    <div className="container">
      <div className="header">
        <h1>📊 MetricISO</h1>
        <p>Dashboard automático de métricas ISO 29110/9001/25010/9241</p>
      </div>

      {error && <div className="error">{error}</div>}

      <FormularioProyecto onProyectoCreado={handleProyectoCreado} />

      <ListaProyectos
        proyectos={proyectos}
        onSeleccionar={handleSeleccionar}
        onAnalizar={handleAnalizar}
        onEliminar={handleEliminar}
        loading={loading}
      />

      {proyectoSeleccionado && (
        <div>
          <DashboardMetricas proyecto={proyectoSeleccionado} />
          <CalculadoraFormulas proyectoId={proyectoSeleccionado.id} />
          <button 
            className="btn btn-primary"
            onClick={() => setProyectoSeleccionado(null)}
          >
            Cerrar
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
