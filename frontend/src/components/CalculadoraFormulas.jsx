import React, { useState, useEffect } from 'react';
import { formulaService } from '../services/api';

function CalculadoraFormulas({ proyectoId }) {
  const [formulas, setFormulas] = useState([]);
  const [formulaSeleccionada, setFormulaSeleccionada] = useState(null);
  const [parametros, setParametros] = useState({});
  const [resultado, setResultado] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const loadFormulas = async () => {
      try {
        const response = await formulaService.getAll();
        setFormulas(response.data);
      } catch (err) {
        setError('Error cargando fórmulas');
      }
    };
    loadFormulas();
  }, []);

  const handleSeleccionarFormula = async (codigo) => {
    try {
      const response = await formulaService.getById(codigo);
      setFormulaSeleccionada(response.data);
      const params = {};
      response.data.parametros.forEach(param => {
        params[param] = '';
      });
      setParametros(params);
      setResultado(null);
    } catch (err) {
      setError('Error cargando fórmula');
    }
  };

  const handleParametroChange = (param, value) => {
    setParametros({
      ...parametros,
      [param]: value === '' ? '' : parseFloat(value)
    });
  };

  const handleCalcular = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await formulaService.calcular(formulaSeleccionada.codigo, {
        proyecto_id: proyectoId,
        parametros
      });
      setResultado(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Error al calcular');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Calculadora de Fórmulas ISO</h2>
      {error && <div className="error">{error}</div>}

      <div className="form-group">
        <label>Selecciona Fórmula</label>
        <select onChange={(e) => handleSeleccionarFormula(e.target.value)}>
          <option value="">-- Selecciona una fórmula --</option>
          {formulas.map((f) => (
            <option key={f.codigo} value={f.codigo}>
              {f.codigo} - {f.nombre}
            </option>
          ))}
        </select>
      </div>

      {formulaSeleccionada && (
        <div>
          <div className="metric-box">
            <div className="metric-box-label">Fórmula</div>
            <div style={{ color: '#2d3748', marginTop: '5px' }}>
              {formulaSeleccionada.formula}
            </div>
          </div>

          <h3>Ingresa los Parámetros</h3>
          {formulaSeleccionada.parametros.map((param) => (
            <div key={param} className="form-group">
              <label>{param}</label>
              <input
                type="number"
                step="0.01"
                value={parametros[param] || ''}
                onChange={(e) => handleParametroChange(param, e.target.value)}
                placeholder={param}
              />
            </div>
          ))}

          <button
            className="btn btn-primary"
            onClick={handleCalcular}
            disabled={loading || Object.values(parametros).some(v => v === '')}
          >
            {loading ? 'Calculando...' : 'CALCULAR'}
          </button>

          {resultado && (
            <div style={{ marginTop: '20px' }}>
              <h3>Resultado</h3>
              <div className="metric-box">
                <div className="metric-box-label">{formulaSeleccionada.codigo}</div>
                <div className="metric-box-value">{resultado.resultado.toFixed(4)}</div>
              </div>
              {resultado.unidad && (
                <p><strong>Unidad:</strong> {resultado.unidad}</p>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default CalculadoraFormulas;
