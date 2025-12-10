import React, { useEffect, useState } from 'react';
import { proyectoService } from '../services/api';

function DashboardMetricas({ proyecto }) {
  const [metrica, setMetrica] = useState(null);
  const [historico, setHistorico] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const response = await proyectoService.getById(proyecto.id);
        setMetrica(response.data.metrica_base);
        setHistorico(response.data.historico || []);
      } catch (err) {
        console.error('Error cargando datos:', err);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, [proyecto.id]);

  if (loading) {
    return <div className="loading">Cargando métricas...</div>;
  }

  return (
    <div className="card">
      <h2>Dashboard - {proyecto.nombre}</h2>
      
      {metrica && (
        <div>
          <h3>Métricas Base</h3>
          <div className="grid-3">
            <div className="metric-box">
              <div className="metric-box-label">Commits Totales</div>
              <div className="metric-box-value">{metrica.commits_totales}</div>
            </div>
            <div className="metric-box">
              <div className="metric-box-label">Commits Mes</div>
              <div className="metric-box-value">{metrica.commits_mes}</div>
            </div>
            <div className="metric-box">
              <div className="metric-box-label">Commits Semana</div>
              <div className="metric-box-value">{metrica.commits_semana}</div>
            </div>
            <div className="metric-box">
              <div className="metric-box-label">Líneas de Código</div>
              <div className="metric-box-value">{metrica.lineas_codigo}</div>
            </div>
            <div className="metric-box">
              <div className="metric-box-label">Complejidad</div>
              <div className="metric-box-value">{metrica.complejidad.toFixed(2)}</div>
            </div>
            <div className="metric-box">
              <div className="metric-box-label">Tiempo Promedio</div>
              <div className="metric-box-value">{metrica.tiempo_promedio_commit.toFixed(2)}h</div>
            </div>
          </div>

          {historico.length > 0 && (
            <div style={{ marginTop: '30px' }}>
              <h3>Histórico de Cálculos</h3>
              <div className="table-responsive">
                <table>
                  <thead>
                    <tr>
                      <th>Fórmula</th>
                      <th>Resultado</th>
                      <th>Fecha</th>
                    </tr>
                  </thead>
                  <tbody>
                    {historico.map((item) => (
                      <tr key={item.id}>
                        <td><strong>{item.formula}</strong></td>
                        <td>{item.resultado.toFixed(2)}</td>
                        <td>{new Date(item.fecha_calculo).toLocaleString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default DashboardMetricas;
