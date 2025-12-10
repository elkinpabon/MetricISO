import React, { useState } from 'react';
import { proyectoService } from '../services/api';

function FormularioProyecto({ onProyectoCreado }) {
  const [nombre, setNombre] = useState('');
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await proyectoService.create({ nombre, url_github: url });
      onProyectoCreado(response.data);
      setNombre('');
      setUrl('');
    } catch (err) {
      setError(err.response?.data?.error || 'Error al crear proyecto');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Nuevo Proyecto</h2>
      {error && <div className="error">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Nombre del Proyecto</label>
          <input
            type="text"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            placeholder="Mi Proyecto"
            required
          />
        </div>
        <div className="form-group">
          <label>URL del Repositorio GitHub</label>
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://github.com/usuario/repo"
            required
          />
        </div>
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Creando...' : 'CREAR PROYECTO'}
        </button>
      </form>
    </div>
  );
}

export default FormularioProyecto;
