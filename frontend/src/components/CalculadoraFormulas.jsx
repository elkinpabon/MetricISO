import React, { useState, useEffect, useMemo } from 'react';
import { Calculator, AlertCircle, CheckCircle, ArrowRight } from 'lucide-react';
import { formulaService } from '../services/api';

function CalculadoraFormulas({ proyectoId }) {
  const [formulas, setFormulas] = useState([]);
  const [normaisoSeleccionada, setNormaISOSeleccionada] = useState(null);
  const [formulaSeleccionada, setFormulaSeleccionada] = useState(null);
  const [parametros, setParametros] = useState({});
  const [resultado, setResultado] = useState(null);
  const [loading, setLoading] = useState(false);
  const [referencias, setReferencias] = useState(null);
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

  // Agrupar fórmulas por norma ISO
  const formulasPorNormaISO = useMemo(() => {
    const grupos = {};
    formulas.forEach(formula => {
      const norma = formula.norma_iso || 'General';
      if (!grupos[norma]) {
        grupos[norma] = [];
      }
      grupos[norma].push(formula);
    });
    return grupos;
  }, [formulas]);

  const normasISO = useMemo(() => Object.keys(formulasPorNormaISO).sort(), [formulasPorNormaISO]);

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
      
      // Cargar referencias de la fórmula
      try {
        const refResponse = await fetch(`http://localhost:5000/api/formulas/${codigo}/referencias`);
        if (refResponse.ok) {
          const refData = await refResponse.json();
          setReferencias(refData);
        } else {
          setReferencias(null);
        }
      } catch (refErr) {
        console.error('Error cargando referencias:', refErr);
        setReferencias(null);
      }
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
      
      // Nota: El histórico se actualiza automáticamente en el componente DetalleProyecto
    } catch (err) {
      setError(err.response?.data?.error || 'Error al calcular');
    } finally {
      setLoading(false);
    }
  };

  const getParameterDescription = (param) => {
    const descriptions = {
      'ICP': 'Índice de Complejidad de Proceso',
      'FR': 'Funcionamiento Requerido',
      'MTBF': 'Tiempo Medio Entre Fallos',
      'NC': 'Número de No Conformidades',
      'IVC': 'Índice de Vulnerabilidades Críticas',
      'CC': 'Cobertura de Código',
      'E': 'Eficiencia del Sistema',
      'TRF': 'Tiempo de Respuesta Funcional',
      'TCR': 'Tiempo de Corrección de Defectos',
      'DCR': 'Densidad de Cambios de Requerimientos',
      'CA': 'Cobertura de Análisis',
      'TC': 'Tasa de Cobertura',
      'VF': 'Validación de Funcionalidad'
    };
    return descriptions[param] || `Ingrese el valor de ${param}`;
  };

  const getInterpretacionColor = (nivel) => {
    const colors = {
      'excelente': '#059669',
      'bueno': '#10b981',
      'aceptable': '#f59e0b',
      'malo': '#ef4444',
      'critico': '#dc2626'
    };
    return colors[nivel?.toLowerCase()] || '#6b7280';
  };

  const allParametrosCompletos = formulaSeleccionada && Object.values(parametros).every(v => v !== '');

  return (
    <div className="card">
      <h2>
        <Calculator size={20} />
        Calculadora de Fórmulas ISO
      </h2>
      
      {error && (
        <div className="error">
          <AlertCircle size={18} />
          {error}
        </div>
      )}

      {/* Selector de norma ISO */}
      <div className="normas-container">
        <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9em', fontWeight: 600, color: '#1a202c' }}>
          Norma ISO
        </label>
        <div className="normas-grid">
          {normasISO.map((norma) => (
            <button
              key={norma}
              className={`norma-button ${normaisoSeleccionada === norma ? 'active' : ''}`}
              onClick={() => {
                setNormaISOSeleccionada(norma);
                setFormulaSeleccionada(null);
                setResultado(null);
              }}
            >
              {norma}
              <span className="norma-count">({formulasPorNormaISO[norma].length})</span>
            </button>
          ))}
        </div>
      </div>

      {/* Selector de fórmula */}
      {normaisoSeleccionada && (
        <div style={{ marginTop: '16px' }}>
          <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9em', fontWeight: 600, color: '#1a202c' }}>
            Fórmula
          </label>
          <div className="formula-selector-grid">
            {formulasPorNormaISO[normaisoSeleccionada].map((f) => (
              <button
                key={f.codigo}
                className={`formula-card ${formulaSeleccionada?.codigo === f.codigo ? 'active' : ''}`}
                onClick={() => handleSeleccionarFormula(f.codigo)}
              >
                <div className="formula-card-code">{f.codigo}</div>
                <div className="formula-card-name">{f.nombre}</div>
                <div className="formula-card-type">{f.tipo}</div>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Formulario de cálculo */}
      {formulaSeleccionada && (
        <div style={{ marginTop: '16px', borderTop: '1px solid #d1d5db', paddingTop: '16px' }}>
          <div className="formula-header">
            <div className="formula-code">{formulaSeleccionada.codigo}</div>
            <div>
              <div className="formula-name">{formulaSeleccionada.nombre}</div>
              <div style={{ display: 'flex', gap: '12px', marginTop: '4px', fontSize: '0.8em' }}>
                <span style={{ color: '#059669', fontWeight: 600 }}>{formulaSeleccionada.tipo}</span>
                <span style={{ color: '#9ca3af' }}>•</span>
                <span style={{ color: '#059669' }}>{formulaSeleccionada.norma_iso}</span>
              </div>
              {formulaSeleccionada.descripcion && (
                <p style={{ margin: '4px 0 0 0', color: '#6b7280', fontSize: '0.8em' }}>
                  {formulaSeleccionada.descripcion}
                </p>
              )}
            </div>
          </div>

          {formulaSeleccionada.formula && (
            <div className="formula-math">
              {formulaSeleccionada.formula}
            </div>
          )}

          <div className="parameters-section">
            <h3 style={{ marginTop: 0, color: '#059669', fontSize: '1em', marginBottom: '12px' }}>
              Parámetros
            </h3>
            
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '14px' }}>
              {formulaSeleccionada.parametros.map((param) => (
                <div key={param} style={{ border: '1px solid #d1fae5', borderRadius: '6px', padding: '10px', backgroundColor: '#f0fdf4' }}>
                  <label style={{ display: 'block', fontSize: '0.85em', fontWeight: 600, color: '#1a202c', marginBottom: '4px' }}>
                    {param}
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    value={parametros[param] || ''}
                    onChange={(e) => handleParametroChange(param, e.target.value)}
                    placeholder={`Ingrese ${param}`}
                    style={{ width: '100%', padding: '6px', border: '1px solid #d1d5db', borderRadius: '4px', fontSize: '0.9em' }}
                  />
                  <div style={{ marginTop: '6px', fontSize: '0.75em', color: '#6b7280', fontStyle: 'italic', lineHeight: '1.3' }}>
                    {getParameterDescription(param)}
                  </div>
                </div>
              ))}
            </div>

            <button
              className="btn btn-primary"
              onClick={handleCalcular}
              disabled={loading || !allParametrosCompletos}
              style={{ width: '100%', marginTop: '12px', fontSize: '0.9em' }}
            >
              <ArrowRight size={16} />
              {loading ? 'Calculando...' : 'CALCULAR'}
            </button>
          </div>

          {resultado && (
            <>
              <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'center', flexDirection: 'column', alignItems: 'center' }}>
                <div style={{ maxWidth: '500px', width: '100%', padding: '20px', border: '2px solid #059669', borderRadius: '12px', backgroundColor: 'rgba(5, 150, 105, 0.04)', textAlign: 'center' }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px', marginBottom: '16px' }}>
                    <CheckCircle size={20} color="#16a34a" />
                    <div className="resultado-label">Resultado</div>
                  </div>
                  <div className="resultado-valor">
                    {resultado.resultado.toFixed(4)}
                  </div>
                  {resultado.unidad && (
                    <div className="resultado-unit">{resultado.unidad}</div>
                  )}
                </div>
              </div>

              {resultado.interpretacion && (
                <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'center' }}>
                  <div style={{ maxWidth: '500px', padding: '18px', border: '2px solid', borderColor: getInterpretacionColor(resultado.interpretacion.nivel), borderRadius: '10px', backgroundColor: getInterpretacionColor(resultado.interpretacion.nivel) + '10' }}>
                    <h4 style={{ margin: '0 0 14px 0', color: '#047857', fontSize: '1.1em', fontWeight: 700, letterSpacing: '-0.3px', textAlign: 'center' }}>
                      Interpretación del Resultado
                    </h4>
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '12px', marginBottom: '14px' }}>
                      <div style={{
                        width: '28px',
                        height: '28px',
                        borderRadius: '6px',
                        backgroundColor: getInterpretacionColor(resultado.interpretacion.nivel),
                        boxShadow: `0 0 12px ${getInterpretacionColor(resultado.interpretacion.nivel)}60`,
                        flexShrink: 0
                      }}></div>
                      <span style={{ fontSize: '1.05em', fontWeight: 700, color: getInterpretacionColor(resultado.interpretacion.nivel) }}>
                        {resultado.interpretacion.nivel?.toUpperCase()}
                      </span>
                    </div>
                    <p style={{ margin: '0 0 12px 0', fontSize: '0.95em', color: '#1f2937', lineHeight: '1.6', fontWeight: 500, textAlign: 'center' }}>
                      {resultado.interpretacion.descripcion}
                    </p>
                    {resultado.interpretacion.recomendacion && (
                      <p style={{ margin: '8px 0 0 0', fontSize: '0.85em', color: '#059669', fontStyle: 'italic', fontWeight: 600, textAlign: 'center' }}>
                        {resultado.interpretacion.recomendacion}
                      </p>
                    )}
                  </div>
                </div>
              )}

              {referencias && referencias.rangos && Object.keys(referencias.rangos).length > 0 && (
                <div style={{ marginTop: '16px', padding: '16px', border: '1px solid #d1fae5', borderRadius: '8px', backgroundColor: '#f0fdf4' }}>
                  <h4 style={{ margin: '0 0 14px 0', color: '#047857', fontSize: '0.95em', fontWeight: 700, letterSpacing: '-0.2px' }}>
                    Rangos de Referencia (ISO)
                  </h4>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '12px' }}>
                    {Object.entries(referencias.rangos).map(([nivel, rango]) => (
                      <div key={nivel} style={{
                        padding: '14px',
                        borderRadius: '8px',
                        border: `2px solid ${getInterpretacionColor(nivel)}`,
                        backgroundColor: getInterpretacionColor(nivel) + '15',
                        textAlign: 'center'
                      }}>
                        <div style={{
                          color: getInterpretacionColor(nivel),
                          fontWeight: 700,
                          fontSize: '0.85em',
                          textTransform: 'uppercase',
                          letterSpacing: '0.3px',
                          marginBottom: '8px'
                        }}>
                          {nivel}
                        </div>
                        <div style={{
                          color: '#1f2937',
                          fontWeight: 600,
                          fontSize: '0.9em',
                          marginBottom: '6px'
                        }}>
                          {rango.min !== null ? rango.min : '-∞'} - {rango.max !== null ? rango.max : '+∞'}
                        </div>
                        {rango.descripcion && (
                          <div style={{
                            color: '#6b7280',
                            fontSize: '0.75em',
                            fontStyle: 'italic',
                            marginTop: '6px'
                          }}>
                            {rango.descripcion}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default CalculadoraFormulas;


