import React, { useEffect, useState } from 'react';
import { ArrowLeft, Zap, TrendingUp, GitBranch, Code2, Calendar, Clock, ExternalLink, Trash2, RefreshCw, Download } from 'lucide-react';
import { proyectoService } from '../services/api';
import CalculadoraFormulas from './CalculadoraFormulas';
import Modal from './Modal';

const FORMULAS_NOMBRES = {
  'ICP': 'Índice de Cumplimiento de Planificación',
  'NC': 'Índice de No Conformidades',
  'FR': 'Tasa de Fallos',
  'MTBF': 'Tiempo Medio Entre Fallos',
  'TPR': 'Tiempo Promedio de Respuesta',
  'IVC': 'Índice de Vulnerabilidades Críticas',
  'CC': 'Complejidad Ciclomática',
  'TS': 'Tasa de Sobrevivencia',
  'IC': 'Índice de Compatibilidad',
  'Ef': 'Eficiencia',
  'E': 'Exactitud',
  'Uso': 'Tasa de Uso de Recursos',
  'IM': 'Índice de Interoperabilidad Multiplataforma'
};

function DetalleProyecto({ proyecto, onVolver, onAnalizar, onEliminar, loading }) {
  const [metrica, setMetrica] = useState(null);
  const [historico, setHistorico] = useState([]);
  const [loadingData, setLoadingData] = useState(true);
  const [modal, setModal] = useState({ isOpen: false, type: 'info', title: '', message: '', onConfirm: null });
  const [activeTab, setActiveTab] = useState('dashboard'); // 'dashboard', 'formulas', 'registro'

  useEffect(() => {
    if (proyecto?.id) {
      loadData();
    }
  }, [proyecto?.id]);

  const loadData = async () => {
    try {
      setLoadingData(true);
      console.log(`Cargando datos del proyecto ${proyecto.id}...`);
      
      const response = await proyectoService.getById(proyecto.id);
      const data = response.data;
      
      console.log('Datos recibidos del servidor:', data);
      console.log('metrica_base:', data.metrica_base);
      
      // Siempre usar metrica_base si existe
      if (data.metrica_base) {
        console.log('Usando metrica_base del servidor:', data.metrica_base);
        setMetrica(data.metrica_base);
      } else {
        // Fallback a valores por defecto
        const metricas_fallback = {
          proyecto_id: data.id,
          commits_totales: data.total_commits || 0,
          commits_mes: 0,
          commits_semana: 0,
          lineas_codigo: data.total_loc || 0,
          complejidad: data.complejidad_ciclomatica || 1.0,
          tiempo_promedio_commit: 0.0
        };
        console.log('Sin metrica_base, usando fallback:', metricas_fallback);
        setMetrica(metricas_fallback);
      }
      
      // Cargar histórico
      const historicoArray = Array.isArray(data.historico) ? data.historico : [];
      console.log(`Histórico: ${historicoArray.length} registros`);
      setHistorico(historicoArray);
    } catch (err) {
      console.error('Error cargando datos:', err);
      // Si falla, usar datos del proyecto pasado como fallback
      if (proyecto) {
        const metricas_fallback = {
          proyecto_id: proyecto.id,
          commits_totales: proyecto.total_commits || 0,
          commits_mes: 0,
          commits_semana: 0,
          lineas_codigo: proyecto.total_loc || 0,
          complejidad: proyecto.complejidad_ciclomatica || 1.0,
          tiempo_promedio_commit: 0.0
        };
        console.log('Error en carga, usando fallback del proyecto:', metricas_fallback);
        setMetrica(metricas_fallback);
      }
      setHistorico([]);
    } finally {
      setLoadingData(false);
    }
  };

  const handleAnalizar = async () => {
    await onAnalizar(proyecto.id);
    await loadData();
  };

  const handleEliminar = () => {
    setModal({
      isOpen: true,
      type: 'warning',
      title: 'Eliminar Proyecto',
      message: '¿Estás seguro de que deseas eliminar este proyecto? Esta acción no se puede deshacer.',
      isDangerous: true,
      onConfirm: async () => {
        setModal({ ...modal, isOpen: false });
        await onEliminar(proyecto.id);
      }
    });
  };

  const handleDescargarPDF = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/proyectos/${proyecto.id}/reporte-pdf`);
      if (!response.ok) {
        setModal({
          isOpen: true,
          type: 'error',
          title: 'Error en la Descarga',
          message: 'No se pudo generar el reporte PDF. Por favor, intenta más tarde.',
          confirmText: 'Aceptar'
        });
        return;
      }
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `reporte_${proyecto.nombre.replace(/\s+/g, '_')}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      setModal({
        isOpen: true,
        type: 'success',
        title: 'Descarga Completada',
        message: 'El reporte PDF se descargó correctamente.',
        confirmText: 'Aceptar'
      });
    } catch (err) {
      console.error('Error descargando PDF:', err);
      setModal({
        isOpen: true,
        type: 'error',
        title: 'Error en la Descarga',
        message: 'Hubo un error al descargar el reporte PDF. Por favor, intenta más tarde.',
        confirmText: 'Aceptar'
      });
    }
  };

  const abrirRepo = () => {
    window.open(proyecto.url_github, '_blank');
  };

  return (
    <div className="detalle-view">
      <Modal
        isOpen={modal.isOpen}
        type={modal.type}
        title={modal.title}
        message={modal.message}
        isDangerous={modal.isDangerous}
        confirmText={modal.confirmText || 'Confirmar'}
        cancelText="Cancelar"
        onConfirm={() => {
          if (modal.onConfirm) modal.onConfirm();
          else setModal({ ...modal, isOpen: false });
        }}
        onCancel={() => setModal({ ...modal, isOpen: false })}
      />
      <div className="detalle-header">
        <button className="btn-back" onClick={onVolver}>
          <ArrowLeft size={24} />
        </button>
        <div className="detalle-title">
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <GitBranch size={32} color="#059669" />
            <div>
              <h1>{proyecto.nombre}</h1>
              <p>{proyecto.url_github}</p>
            </div>
          </div>
        </div>
        <div className="detalle-actions">
          <button className="btn btn-secondary" onClick={abrirRepo}>
            <ExternalLink size={16} />
            Ver Repo
          </button>
          <button 
            className="btn btn-secondary" 
            onClick={handleDescargarPDF}
            title="Descargar reporte PDF"
          >
            <Download size={16} />
            Reporte PDF
          </button>
          <button 
            className="btn btn-primary" 
            onClick={handleAnalizar}
            disabled={loading}
          >
            <RefreshCw size={16} />
            {loading ? 'Analizando...' : 'Analizar'}
          </button>
          <button 
            className="btn btn-danger" 
            onClick={handleEliminar}
            disabled={loading}
          >
            <Trash2 size={16} />
            Eliminar
          </button>
        </div>
      </div>

      {loadingData ? (
        <div className="loading">Cargando información del proyecto...</div>
      ) : (
        <div className="detalle-content">
          {/* Información del Proyecto (siempre visible) */}
          <div className="info-section">
            <h2>
              <Zap size={24} />
              Información del Proyecto
            </h2>
            <div className="info-grid">
              <div className="info-card">
                <div className="info-label">Estado</div>
                <div className={`info-value status-${proyecto.estado}`}>
                  {proyecto.estado.charAt(0).toUpperCase() + proyecto.estado.slice(1)}
                </div>
              </div>
              <div className="info-card">
                <div className="info-label">Fecha de Creación</div>
                <div className="info-value">
                  {new Date(proyecto.fecha_creacion).toLocaleDateString('es-ES')}
                </div>
              </div>
              <div className="info-card">
                <div className="info-label">Última Actualización</div>
                <div className="info-value">
                  {new Date(proyecto.fecha_actualizacion).toLocaleDateString('es-ES')}
                </div>
              </div>
            </div>
          </div>

          {/* Tabs Navigation */}
          <div className="tabs-container">
            <div className="tabs-nav">
              <button
                className={`tab-button ${activeTab === 'dashboard' ? 'active' : ''}`}
                onClick={() => setActiveTab('dashboard')}
              >
                <TrendingUp size={18} />
                Dashboard
              </button>
              <button
                className={`tab-button ${activeTab === 'formulas' ? 'active' : ''}`}
                onClick={() => setActiveTab('formulas')}
              >
                <Zap size={18} />
                Calculadora de Fórmulas
              </button>
              <button
                className={`tab-button ${activeTab === 'registro' ? 'active' : ''}`}
                onClick={() => setActiveTab('registro')}
              >
                <Code2 size={18} />
                Registro de Cálculos ({historico.length})
              </button>
            </div>

            {/* Tab: Dashboard */}
            {activeTab === 'dashboard' && metrica && (
              <div className="tab-content">
                <div className="metrics-section">
                  <h3>Métricas del Repositorio</h3>
                  {proyecto.estado === 'pendiente' && (
                    <div style={{ padding: '20px', background: '#fffacd', borderRadius: '8px', marginBottom: '20px', color: '#d69e2e' }}>
                      ⚠️ Proyecto pendiente de análisis. Haz clic en "Analizar" en la parte superior para obtener las métricas.
                    </div>
                  )}
                  <div className="metrics-grid">
                    <div className="metric-card">
                      <div className="metric-icon">
                        <GitBranch size={28} />
                      </div>
                      <div className="metric-content">
                        <div className="metric-label">Commits Totales</div>
                        <div className="metric-value">{metrica.commits_totales}</div>
                        <div className="metric-detail">Total histórico</div>
                      </div>
                    </div>

                    <div className="metric-card">
                      <div className="metric-icon">
                        <Calendar size={28} />
                      </div>
                      <div className="metric-content">
                        <div className="metric-label">Commits Último Mes</div>
                        <div className="metric-value">{metrica.commits_mes}</div>
                        <div className="metric-detail">30 días anteriores</div>
                      </div>
                    </div>

                    <div className="metric-card">
                      <div className="metric-icon">
                        <Clock size={28} />
                      </div>
                      <div className="metric-content">
                        <div className="metric-label">Commits Última Semana</div>
                        <div className="metric-value">{metrica.commits_semana}</div>
                        <div className="metric-detail">7 días anteriores</div>
                      </div>
                    </div>

                    <div className="metric-card">
                      <div className="metric-icon">
                        <Code2 size={28} />
                      </div>
                      <div className="metric-content">
                        <div className="metric-label">Líneas de Código</div>
                        <div className="metric-value">{metrica.lineas_codigo.toLocaleString()}</div>
                        <div className="metric-detail">Total en repositorio</div>
                      </div>
                    </div>

                    <div className="metric-card warning">
                      <div className="metric-icon">
                        <TrendingUp size={28} />
                      </div>
                      <div className="metric-content">
                        <div className="metric-label">Complejidad Ciclomática</div>
                        <div className="metric-value">{metrica.complejidad.toFixed(2)}</div>
                        <div className="metric-detail">Complejidad promedio</div>
                      </div>
                    </div>

                    <div className="metric-card">
                      <div className="metric-icon">
                        <Clock size={28} />
                      </div>
                      <div className="metric-content">
                        <div className="metric-label">Tiempo Promedio entre Commits</div>
                        <div className="metric-value">{metrica.tiempo_promedio_commit.toFixed(2)}h</div>
                        <div className="metric-detail">Promedio en horas</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Tab: Calculadora de Fórmulas */}
            {activeTab === 'formulas' && (
              <div className="tab-content">
                <div className="formulas-section">
                  <CalculadoraFormulas proyectoId={proyecto.id} onCalculoCompleto={loadData} />
                </div>
              </div>
            )}

            {/* Tab: Registro de Cálculos */}
            {activeTab === 'registro' && (
              <div className="tab-content">
                {historico.length > 0 ? (
                  <div className="historico-section">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
                      <h3 style={{ margin: 0, color: '#047857' }}>Histórico de Cálculos de Fórmulas</h3>
                      <button
                        onClick={() => loadData()}
                        className="refresh-btn"
                        title="Actualizar histórico"
                      >
                        <RefreshCw size={18} />
                        Actualizar
                      </button>
                    </div>
                    <div className="historico-table">
                      <table>
                        <thead>
                          <tr>
                            <th>Fórmula</th>
                            <th>Nombre Completo</th>
                            <th>Resultado</th>
                            <th>Fecha de Cálculo</th>
                          </tr>
                        </thead>
                        <tbody>
                          {historico.map((item) => (
                            <tr key={item.id}>
                              <td><strong className="formula-code">{item.formula}</strong></td>
                              <td>{FORMULAS_NOMBRES[item.formula] || 'Fórmula Desconocida'}</td>
                              <td className="resultado-valor">{item.resultado.toFixed(4)}</td>
                              <td>{new Date(item.fecha_calculo).toLocaleString('es-ES')}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                ) : (
                  <div style={{ padding: '40px', textAlign: 'center', color: '#718096' }}>
                    <p>No hay cálculos registrados aún.</p>
                    <p style={{ fontSize: '0.9em', marginTop: '10px' }}>Ve a la pestaña "Calculadora de Fórmulas" para calcular.</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default DetalleProyecto;
