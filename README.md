# MetricISO - Dashboard de Metricas ISO

Dashboard web que automatiza metricas de calidad ISO 29110/9001/25010/9241. Solo ingresas la URL de un repositorio GitHub y obtienes analisis automatico.

## Caracteristicas

- Analisis automatico de GitHub (clone ligero --depth 1)
- 13 Formulas ISO exactas: ICP, NC, FR, MTBF, TPR, IVC, CC, TS, IC, Ef, E, Uso, IM
- Dashboard en tiempo real con metricas por proyecto
- Historico de calculos
- Flask + React + MySQL

## Requisitos

- Python 3.8+
- Node.js 14+
- MySQL 5.7+
- Git

## Instalacion Rapida

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

1. Crear: Nombre + URL GitHub
2. Analizar: GitHub API + clone ligero (2-3 min)
3. Dashboard: Metricas + 13 Formulas + Historico

## Endpoints API

GET /api/proyectos - Listar
POST /api/proyectos - Crear
GET /api/proyectos/<id> - Obtener
POST /api/proyectos/<id>/analizar - Analizar
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
