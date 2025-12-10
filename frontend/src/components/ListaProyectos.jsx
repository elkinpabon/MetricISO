import React, { useState } from 'react';
import { List, Zap, Trash2, GitBranch } from 'lucide-react';
import Modal from './Modal';

function ListaProyectos({ proyectos, onSeleccionar, onAnalizar, onEliminar, loading }) {
  const [modal, setModal] = useState({ isOpen: false, type: 'info', title: '', message: '', onConfirm: null });

  const handleEliminarClick = (proyectoId) => {
    setModal({
      isOpen: true,
      type: 'warning',
      title: 'Eliminar Proyecto',
      message: '¿Estás seguro de que deseas eliminar este proyecto? Esta acción no se puede deshacer.',
      confirmText: 'Eliminar',
      cancelText: 'Cancelar',
      isDangerous: true,
      onConfirm: () => {
        setModal({ ...modal, isOpen: false });
        onEliminar(proyectoId);
      }
    });
  };

  return (
    <div className="card">
      <h2>
        <List size={24} />
        Proyectos
      </h2>
      {proyectos.length === 0 ? (
        <p style={{ textAlign: 'center', color: '#718096', padding: '40px 0', fontSize: '1.05em' }}>
          No hay proyectos. Crea uno para comenzar.
        </p>
      ) : (
        <div className="grid-2">
          {proyectos.map((proyecto) => (
            <div 
              key={proyecto.id} 
              className="proyecto-item proyecto-clickable"
              onClick={() => onSeleccionar(proyecto)}
              style={{ cursor: 'pointer' }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
                <GitBranch size={18} color="#667eea" />
                <h3 style={{ margin: 0 }}>{proyecto.nombre}</h3>
              </div>
              <p><strong>URL:</strong> {proyecto.url_github}</p>
              <div className={`proyecto-status ${proyecto.estado}`}>
                {proyecto.estado.charAt(0).toUpperCase() + proyecto.estado.slice(1)}
              </div>
              <div style={{ marginTop: '15px', marginBottom: '15px' }}>
                <div className="metric-box">
                  <div className="metric-box-label">Commits</div>
                  <div className="metric-box-value">{proyecto.total_commits}</div>
                </div>
                <div className="metric-box">
                  <div className="metric-box-label">LOC</div>
                  <div className="metric-box-value">{proyecto.total_loc}</div>
                </div>
              </div>
              <div className="actions" onClick={(e) => e.stopPropagation()}>
                <button 
                  className="btn btn-secondary btn-small"
                  onClick={() => onAnalizar(proyecto.id)}
                  disabled={loading}
                  title="Analizar proyecto"
                >
                  <Zap size={16} />
                  {loading ? 'Analizando...' : 'Analizar'}
                </button>
                <button 
                  className="btn btn-danger btn-small"
                  onClick={() => handleEliminarClick(proyecto.id)}
                  disabled={loading}
                  title="Eliminar proyecto"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
      
      <Modal
        isOpen={modal.isOpen}
        type={modal.type}
        title={modal.title}
        message={modal.message}
        confirmText={modal.confirmText}
        cancelText={modal.cancelText}
        isDangerous={modal.isDangerous}
        onConfirm={() => modal.onConfirm?.()}
        onCancel={() => setModal({ ...modal, isOpen: false })}
      />
    </div>
  );
}

export default ListaProyectos;
