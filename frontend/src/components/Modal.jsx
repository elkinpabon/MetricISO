import React from 'react';
import { AlertCircle, CheckCircle, Info, X } from 'lucide-react';

function Modal({ isOpen, title, message, type = 'info', onConfirm, onCancel, confirmText = 'Confirmar', cancelText = 'Cancelar', isDangerous = false }) {
  if (!isOpen) return null;

  const getIcon = () => {
    switch (type) {
      case 'success':
        return <CheckCircle size={32} color="#059669" />;
      case 'error':
        return <AlertCircle size={32} color="#dc2626" />;
      case 'warning':
        return <AlertCircle size={32} color="#f59e0b" />;
      case 'info':
      default:
        return <Info size={32} color="#059669" />;
    }
  };

  const getHeaderColor = () => {
    switch (type) {
      case 'success':
        return '#ecfdf5';
      case 'error':
        return '#fef2f2';
      case 'warning':
        return '#fffbeb';
      case 'info':
      default:
        return '#f0fdf4';
    }
  };

  const getHeaderBorderColor = () => {
    switch (type) {
      case 'success':
        return '#d1fae5';
      case 'error':
        return '#fee2e2';
      case 'warning':
        return '#fef3c7';
      case 'info':
      default:
        return '#d1fae5';
    }
  };

  const getTitleColor = () => {
    switch (type) {
      case 'success':
        return '#047857';
      case 'error':
        return '#b91c1c';
      case 'warning':
        return '#b45309';
      case 'info':
      default:
        return '#047857';
    }
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 9999,
      backdropFilter: 'blur(4px)'
    }}>
      <div style={{
        backgroundColor: 'white',
        borderRadius: '12px',
        boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
        maxWidth: '450px',
        width: '90%',
        overflow: 'hidden',
        animation: 'slideUp 0.3s ease-out'
      }}>
        {/* Header */}
        <div style={{
          backgroundColor: getHeaderColor(),
          borderBottom: `2px solid ${getHeaderBorderColor()}`,
          padding: '24px',
          display: 'flex',
          alignItems: 'center',
          gap: '16px'
        }}>
          {getIcon()}
          <h2 style={{
            margin: 0,
            color: getTitleColor(),
            fontSize: '1.25em',
            fontWeight: 700,
            flex: 1
          }}>
            {title}
          </h2>
          <button
            onClick={onCancel}
            style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              padding: '4px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            <X size={24} color="#6b7280" />
          </button>
        </div>

        {/* Content */}
        <div style={{
          padding: '24px',
          color: '#374151',
          fontSize: '0.95em',
          lineHeight: '1.6'
        }}>
          {message}
        </div>

        {/* Footer */}
        <div style={{
          padding: '16px 24px',
          borderTop: '1px solid #e5e7eb',
          display: 'flex',
          gap: '12px',
          justifyContent: 'flex-end'
        }}>
          <button
            onClick={onCancel}
            style={{
              padding: '10px 20px',
              border: '1px solid #d1d5db',
              borderRadius: '8px',
              backgroundColor: 'white',
              color: '#374151',
              cursor: 'pointer',
              fontWeight: 600,
              fontSize: '0.9em',
              transition: 'all 0.3s ease',
              hover: {
                backgroundColor: '#f3f4f6'
              }
            }}
            onMouseEnter={(e) => e.target.style.backgroundColor = '#f3f4f6'}
            onMouseLeave={(e) => e.target.style.backgroundColor = 'white'}
          >
            {cancelText}
          </button>
          <button
            onClick={onConfirm}
            style={{
              padding: '10px 20px',
              border: 'none',
              borderRadius: '8px',
              backgroundColor: isDangerous ? '#dc2626' : '#059669',
              color: 'white',
              cursor: 'pointer',
              fontWeight: 600,
              fontSize: '0.9em',
              transition: 'all 0.3s ease'
            }}
            onMouseEnter={(e) => {
              e.target.style.backgroundColor = isDangerous ? '#b91c1c' : '#047857';
              e.target.style.transform = 'translateY(-2px)';
              e.target.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
            }}
            onMouseLeave={(e) => {
              e.target.style.backgroundColor = isDangerous ? '#dc2626' : '#059669';
              e.target.style.transform = 'translateY(0)';
              e.target.style.boxShadow = 'none';
            }}
          >
            {confirmText}
          </button>
        </div>
      </div>

      <style>{`
        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
}

export default Modal;
