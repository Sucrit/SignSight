## 2026-04-23 - Prevent Unnecessary React Re-renders from Frame Processor
**Learning:** During continuous recognition flows, the frame processor updates state objects like `prediction` every 30-100ms. Blindly creating new state references on every tick causes extreme React render churn, increasing thermal load.
**Action:** Always perform strict equality checks before calling `setState` on complex objects, returning the same reference if nothing changed.
