import React from 'react';

function ListaProyectos({ proyectos, onSeleccionar, onAnalizar, onEliminar, loading }) {
  return (
    <div className="card">
      <h2>Proyectos</h2>
      {proyectos.length === 0 ? (
        <p>No hay proyectos. Crea uno para comenzar.</p>
      ) : (
        <div className="grid-2">
          {proyectos.map((proyecto) => (
            <div key={proyecto.id} className="proyecto-item">
              <h3>{proyecto.nombre}</h3>
              <p><strong>URL:</strong> {proyecto.url_github}</p>
              <div className={`proyecto-status ${proyecto.estado}`}>
                {proyecto.estado.toUpperCase()}
              </div>
              <div className="metric-box">
                <div className="metric-box-label">Commits</div>
                <div className="metric-box-value">{proyecto.total_commits}</div>
              </div>
              <div className="metric-box">
                <div className="metric-box-label">LOC</div>
                <div className="metric-box-value">{proyecto.total_loc}</div>
              </div>
              <div className="actions">
                <button 
                  className="btn btn-primary btn-small"
                  onClick={() => onSeleccionar(proyecto)}
                >
                  Ver
                </button>
                <button 
                  className="btn btn-secondary btn-small"
                  onClick={() => onAnalizar(proyecto.id)}
                  disabled={loading}
                >
                  {loading ? 'Analizando...' : 'Analizar'}
                </button>
                <button 
                  className="btn btn-danger btn-small"
                  onClick={() => onEliminar(proyecto.id)}
                  disabled={loading}
                >
                  Eliminar
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ListaProyectos;
