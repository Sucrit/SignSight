## 2024-04-21 - Prevent redundant React state churn from high-frequency frame processors

**Learning:** When using high-frequency frame processors (like VisionCamera's `useFrameProcessor`), mapping frame results to React state (e.g., `setPrediction((current) => ({...current, label}))`) can trigger hundreds of redundant re-renders per second if object references change on every tick, even when actual primitive values (like `label` or `hasHand`) are identical. This creates massive JS bridge pressure and increases thermal load on mobile devices.

**Action:** Always perform strict equality checks inside state setter callbacks attached to high-frequency worklets/event emitters. If the specific values being updated are identical to the current state, return the exact same `current` reference to bail out of the React render cycle early (e.g., `current.label === label ? current : {...current, label}`).
