# DPS - Data Plane Signaling

Diagramas ASCII para los casos de uso del protocolo DPS (Data Plane Signaling) implementados en Eclipse DataSpace Components.

---

## Descripción

El protocolo DPS gestiona la comunicación **intra-organizacional** entre el Control Plane y el Data Plane para:
- Iniciar flujos de transferencia de datos
- Suspender y reanudar transferencias activas
- Terminar y limpiar recursos de transferencia

Es el protocolo de señalización interno que conecta la lógica de negocio (Control Plane) con la ejecución de datos (Data Plane).

---

## Diagramas Disponibles

| # | Archivo | Descripción | Dirección |
|---|---------|-------------|-----------|
| 01 | `DPS_start.txt` | Inicio de flujo de datos | CP → DP |
| 02 | `DPS_suspend.txt` | Suspensión temporal de flujo | CP → DP |
| 03 | `DPS_resume.txt` | Reanudación de flujo suspendido | CP → DP |
| 04 | `DPS_terminate.txt` | Terminación definitiva de flujo | CP → DP |

**CP** = Control Plane | **DP** = Data Plane

---

## Flujos Principales

### 1. Start (Inicio)
```
CONTROL PLANE                      DATA PLANE
    |                                  |
    |  DataFlowStartMessage           |
    | -------------------------------> |
    |                                  | [PUSH: Inicia Pipeline]
    |                                  | [PULL: Genera Token]
    |  DataFlowResponse + DataAddress |
    | <------------------------------- |
```

- **PUSH**: El Data Plane inicia la transferencia hacia el destino
- **PULL**: El Data Plane genera un token de acceso y devuelve un EDR

### 2. Suspend (Suspensión)
```
CONTROL PLANE                      DATA PLANE
    |                                  |
    |  DataFlowSuspendMessage         |
    | -------------------------------> |
    |                                  | [PULL: Revoca Token]
    |                                  | [PUSH: Pausa hilos]
    |  ACK (200 OK)                   |
    | <------------------------------- |
```

Pausa temporal. El proceso puede reanudarse posteriormente.

### 3. Resume (Reanudación)
```
CONTROL PLANE                      DATA PLANE
    |                                  |
    |  DataFlowStartMessage (mismo ID)|
    | -------------------------------> |
    |                                  | [PULL: Genera NUEVO Token]
    |                                  | [PUSH: Reactiva hilos]
    |  DataFlowResponse + Nueva EDR   |
    | <------------------------------- |
```

El protocolo es **idempotente**: enviar un StartMessage a un proceso existente lo reactiva.

### 4. Terminate (Terminación)
```
CONTROL PLANE                      DATA PLANE
    |                                  |
    |  DataFlowTerminateMessage       |
    | -------------------------------> |
    |                                  | [Elimina Token]
    |                                  | [Cierra conexiones]
    |                                  | [Limpia recursos]
    |  ACK (200 OK)                   |
    | <------------------------------- |
```

Finalización **definitiva**. Para transferir nuevamente se requiere un nuevo proceso.

---

## Tipos de Transferencia

| Tipo | Descripción | Flujo de Datos |
|------|-------------|----------------|
| **PUSH** | El proveedor envía datos al consumidor | Proveedor → Consumidor |
| **PULL** | El consumidor descarga datos del proveedor | Consumidor ← Proveedor |

---

## Triggers de Señalización

Los mensajes DPS pueden originarse por:

| Trigger | Ejemplo |
|---------|---------|
| **Policy Monitor** | Contrato expirado, violación de política |
| **DSP Remoto** | Mensaje de la contraparte vía DSP |
| **Management API** | Operador invoca manualmente |
| **Error del Sistema** | Fallo irrecuperable |

---

## Documentación Oficial

- **Data Plane Signaling**: https://eclipse-edc.github.io/documentation/for-contributors/data-plane/data-plane-signaling/
