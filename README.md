# MetricISO - Dashboard de Métricas ISO

Dashboard web que automatiza métricas de calidad ISO 29110/9001/25010/9241. Solo ingresas la URL de un repositorio GitHub y obtienes análisis automático.

## Características

- Análisis automático de GitHub (clone ligero --depth 1)
- 13 Fórmulas ISO exactas: ICP, NC, FR, MTBF, TPR, IVC, CC, TS, IC, Ef, E, Uso, IM
- Dashboard en tiempo real con métricas por proyecto
- Histórico de cálculos
- Interfaz multi-vista: Lista principal + Detalle por proyecto
- Flask + React + MySQL/TiDB

## Requisitos

- Python 3.8+
- Node.js 14+
- MySQL 5.7+ (o TiDB Cloud)
- Git

## Instalación Rápida

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# Configurar .env
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Flujo (3 Clics)

1. **Crear**: Nombre + URL GitHub
2. **Analizar**: GitHub API + clone ligero (2-3 min)
3. **Dashboard**: Métricas + 13 Fórmulas + Histórico

## Arquitectura de Interfaz

### Vista Principal
- Columna izquierda: Formulario para crear proyectos
- Columna derecha: Grid de proyectos existentes
- Click en proyecto → abre vista de detalle

### Vista de Detalle
- Información del proyecto (estado, fechas)
- Métricas del repositorio (commits, LOC, complejidad)
- Calculadora de fórmulas ISO
- Histórico de cálculos
- Acciones: Volver, Analizar, Eliminar

**Ver `ARCHITECTURE.md` para diagrama completo**

## Endpoints API

```
GET    /api/proyectos              - Listar todos
POST   /api/proyectos              - Crear nuevo
GET    /api/proyectos/<id>         - Obtener con métricas
POST   /api/proyectos/<id>/analizar - Analizar repositorio
DELETE /api/proyectos/<id>         - Eliminar proyecto
GET    /api/proyectos/<id>/historico - Histórico de cálculos
GET    /api/formulas               - Listar fórmulas
GET    /api/formulas/<codigo>      - Obtener fórmula
POST   /api/formulas/<codigo>/calcular - Calcular fórmula
```
GET /api/formulas - Formulas
POST /api/formulas/<codigo>/calcular - Calcular

## 13 Formulas ISO

- ICP: (Realizadas/Planificadas)*100
- NC: NoConformidades/Auditados
- FR: Fallos/Tiempo
- MTBF: TiempoTotal/Fallos
- TPR: SumaTiempos/Solicitudes
- IVC: (Criticas/Totales)*100
- CC: E-N+2P
- TS: (Correctas/Totales)*100
- IC: (Soportados/Objetivo)*100
- Ef: TareasCompletadas/Tiempo
- E: (Correctas/Totales)*100
- Uso: (RecursoUtilizado/Total)*100
- IM: (PlataformasSoportadas/Objetivo)*100

## Estructura

MetricISO/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── controllers/
│   │   ├── views/
│   │   └── utils/
│   ├── config.py
│   ├── app.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── App.js
│   └── package.json
└── README.md

## Licencia

MIT
