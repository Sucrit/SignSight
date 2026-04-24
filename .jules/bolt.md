## 2026-04-15 - Adaptive Frame Throttle in react-native-vision-camera
**Learning:** High-frequency MediaPipe landmarker execution in a continuous mobile frame processor can cause severe thermal build-up and battery drain, even when no target object (e.g., hands) is present.
**Action:** Use `react-native-worklets-core` `useSharedValue` to track consecutive empty frames natively inside the worklet, and dynamically back-off the processing interval when idle to significantly reduce sustained CPU/GPU load without missing the target's re-entry.
## 2024-04-24 - Prevent High-Frequency State Churn in Recognition Runtime

**Learning:** During continuous camera frame processing and ML inference, the recognition runtime was unnecessarily creating new state object references for `prediction` even when the underlying values (like `label` or `hasHand`) had not changed. This forced frequent, unnecessary React re-renders of the camera UI, increasing device thermal load.

**Action:** Apply a bailout pattern to state setter functions in high-frequency event streams (e.g., `setPrediction((current) => current.label === label ? current : ({ ...current, label }))`). Returning the existing reference when values are strictly equal prevents React from scheduling a re-render.
