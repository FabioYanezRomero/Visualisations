# DSP - Dataspace Protocol

Diagramas ASCII para los casos de uso del protocolo DSP (Dataspace Protocol) implementados en Eclipse DataSpace Components.

---

## Descripción

El protocolo DSP gestiona la comunicación entre Control Planes de diferentes organizaciones para:
- Descubrimiento de catálogos de datos
- Negociación de contratos de acceso
- Coordinación de transferencias de datos

Es el protocolo **inter-organizacional** principal para la gestión de contratos y metadatos.

---

## Diagramas Disponibles

| # | Archivo | Descripción | Tipo de Proceso |
|---|---------|-------------|-----------------|
| 01 | `DSP_discovery.txt` | Descubrimiento de catálogo | Síncrono |
| 02 | `DSP_negotiation.txt` | Negociación de contrato | Asíncrono |
| 03 | `DSP_transfer.txt` | Coordinación de transferencia | Asíncrono |

---

## Flujos Principales

### 1. Discovery (Descubrimiento)
```
CONSUMIDOR                         PROVEEDOR
    |                                  |
    |  (1) CatalogRequest             |
    | -------------------------------> |
    |                                  | [Valida identidad]
    |                                  | [Filtra por política]
    |  (2) CatalogMessage (DCAT)      |
    | <------------------------------- |
```

El proveedor genera el catálogo **dinámicamente** filtrando activos según las credenciales del consumidor.

### 2. Negotiation (Negociación)
```
CONSUMIDOR                         PROVEEDOR
    |                                  |
    |  (1) ContractRequest            |
    | -------------------------------> |
    |                                  | [Evalúa políticas]
    |  (2) ACK                        | [Crea proceso]
    | <------------------------------- |
    |         ...                      |
    |  (N) ContractAgreement          |
    | <------------------------------- |
```

Proceso **asíncrono** que resulta en un ContractAgreement firmado por ambas partes.

### 3. Transfer (Transferencia)
```
CONSUMIDOR                         PROVEEDOR
    |                                  |
    |  (1) TransferRequest            |
    | -------------------------------> |
    |                                  | [Provisiona Data Plane]
    |  (2) TransferStart + EDR        |
    | <------------------------------- |
    |         ...                      |
    |  (N) TransferTermination        |
    | <------------------------------> |
```

Coordina el acceso a datos. En flujos PULL, el consumidor recibe un EDR (Endpoint Data Reference) con el token de acceso.

---

## Norma Base

- **Dataspace Protocol Specification**: https://github.com/eclipse-dataspace-protocol-base/DataspaceProtocol

---

## Relación con Otros Protocolos

| Protocolo | Relación |
|-----------|----------|
| **DCP** | DSP usa tokens DCP para autenticación en cabeceras |
| **DPS** | DSP coordina con DPS para iniciar transferencias en Data Plane |
