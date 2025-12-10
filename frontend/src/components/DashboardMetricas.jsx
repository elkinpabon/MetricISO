import React, { useEffect, useState } from 'react';
import { TrendingUp, GitCommit, Code2, Zap, Calendar, Clock } from 'lucide-react';
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
      <h2>
        <TrendingUp size={24} />
        Dashboard - {proyecto.nombre}
      </h2>
      
      {metrica && (
        <div>
          <h3 style={{ marginTop: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Zap size={20} color="#667eea" />
            Métricas Base
          </h3>
          <div className="grid-3">
            <div className="metric-box">
              <div className="metric-box-label">
                <GitCommit size={16} style={{ marginRight: '4px' }} />
                Commits Totales
              </div>
              <div className="metric-box-value">{metrica.commits_totales}</div>
            </div>
            <div className="metric-box">
              <div className="metric-box-label">
                <Calendar size={16} style={{ marginRight: '4px' }} />
                Commits Mes
              </div>
              <div className="metric-box-value">{metrica.commits_mes}</div>
            </div>
            <div className="metric-box">
              <div className="metric-box-label">
                <Clock size={16} style={{ marginRight: '4px' }} />
                Commits Semana
              </div>
              <div className="metric-box-value">{metrica.commits_semana}</div>
            </div>
            <div className="metric-box">
              <div className="metric-box-label">
                <Code2 size={16} style={{ marginRight: '4px' }} />
                Líneas de Código
              </div>
              <div className="metric-box-value">{metrica.lineas_codigo}</div>
            </div>
            <div className="metric-box warning">
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
              <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <TrendingUp size={20} color="#667eea" />
                Histórico de Cálculos
              </h3>
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
                        <td>{item.resultado.toFixed(4)}</td>
                        <td>{new Date(item.fecha_calculo).toLocaleString('es-ES')}</td>
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
