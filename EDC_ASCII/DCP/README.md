# DCP - Decentralized Claims Protocol

Diagramas ASCII para los casos de uso del protocolo DCP (Decentralized Claims Protocol) implementados en Eclipse DataSpace Components.

---

## Estructura de Carpetas

| Carpeta | Descripción | Diagramas |
|---------|-------------|-----------|
| `credential_exchange/` | Intercambio de credenciales inter-organizacional | 01-08 |
| `Identity_management/` | Gestión de identidad intra-organizacional | 01-04 |
| `Issuer_management/` | Administración del Issuer Service | 01-03 |
| `automation/` | Procesos automatizados | 01-02 |

---

## 1. Familia Intercambio de Credenciales (credential_exchange/)

Implementa la especificación DCP para procesos **inter-organizacionales**.

| # | Archivo | Descripción | Estado |
|---|---------|-------------|--------|
| 01 | `Issuer_metadata_discovery.txt` | Descubrimiento de metadatos del emisor | ✅ Documentado |
| 02 | `Issuance_request.txt` | Solicitud de emisión de credencial | ✅ Documentado |
| 03 | `Issuance_status.txt` | Consulta de estado de emisión | ✅ Documentado |
| 04 | `credential_delivery.txt` | Entrega de credencial (modelo Push) | ✅ Documentado |
| 05 | `credential_offer.txt` | Oferta de credencial del emisor | ✅ Documentado |
| 06 | `presentation_query.txt` | Consulta de presentación verificable | ✅ Documentado |
| 07 | `revocation_check.txt` | Verificación de revocación | ✅ Documentado |
| 08 | `credential_verification.txt` | Verificación completa de VP | ✅ Documentado |

> **Nota**: El soporte de emisión en el Identity Hub (lado Holder) está marcado como "trabajo en progreso" en la documentación oficial.

---

## 2. Familia Gestión de Identidad (Identity_management/)

Define la administración interna del Identity Hub para procesos **intra-organizacionales**.

| # | Archivo | Descripción | Estado |
|---|---------|-------------|--------|
| 01 | `Participant_Context_Lifecycle.txt` | Ciclo de vida del contexto | ✅ Documentado |
| 02 | `DID_document_publishing.txt` | Publicación de documento DID | ✅ Documentado |
| 03 | `key_rotation.txt` | Rotación de claves criptográficas | ✅ Documentado |
| 04 | `key_revocation.txt` | Revocación de claves | ✅ Documentado |

---

## 3. Familia Gestión del Emisor (Issuer_management/)

Define la administración del Issuer Service.

| # | Archivo | Descripción | Estado |
|---|---------|-------------|--------|
| 01 | `holder_onboarding.txt` | Registro de clientes/holders | ✅ Documentado |
| 02 | `attestation_definition.txt` | Definición de fuentes de atestación | ⚠️ Parcial |
| 03 | `credential_definition.txt` | Definición de estructura de credencial | ✅ Documentado |

> **Nota**: Las fuentes de atestación complejas (ej. `PresentationAttestationSource`) están marcadas como "bajo desarrollo".

---

## 4. Familia Automatización (automation/)

Procesos automatizados que dependen de componentes auxiliares.

| # | Archivo | Descripción | Estado |
|---|---------|-------------|--------|
| 01 | `credential_renewal.txt` | Renovación automática de credenciales | ⚠️ Inferido |
| 02 | `token_renewal.txt` | Renovación de tokens de Data Plane | ❌ No implementado |

> **Nota**: La renovación de tokens de Data Plane "actualmente no está implementada" según la documentación oficial de EDC.

---

## Normas Consideradas

| Norma | Descripción |
|-------|-------------|
| **DCP** | Decentralized Claims Protocol - Define mensajes y flujos de tokens |
| **W3C VC 1.1** | Verifiable Credentials Data Model - Estructura de credenciales |
| **W3C DIDs** | Decentralized Identifiers - Método `did:web` |
| **DIF PE** | Presentation Exchange - Requisitos complejos de verificación (en desarrollo) |

---

## Leyenda de Estados

- ✅ **Documentado**: Flujo explícitamente documentado en EDC
- ⚠️ **Parcial/Inferido**: Flujo parcialmente documentado o inferido de la arquitectura
- ❌ **No implementado**: Funcionalidad no implementada actualmente en EDC