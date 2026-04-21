## 2026-04-15 - Adaptive Frame Throttle in react-native-vision-camera
**Learning:** High-frequency MediaPipe landmarker execution in a continuous mobile frame processor can cause severe thermal build-up and battery drain, even when no target object (e.g., hands) is present.
**Action:** Use `react-native-worklets-core` `useSharedValue` to track consecutive empty frames natively inside the worklet, and dynamically back-off the processing interval when idle to significantly reduce sustained CPU/GPU load without missing the target's re-entry.

## 2026-04-21 - Reduce redundant React state churn in camera experience
**Learning:** High-frequency MediaPipe landmarker execution triggers frequent state updates in `useRecognitionRuntime.ts`. Without strict equality checks, these `setPrediction` calls create new object references even when prediction values (like confidence, label, handedness) haven't changed, causing the entire `CameraExperience` to re-render excessively and generating unnecessary memory churn.
**Action:** When working with high-frequency streams in React, always apply strict equality checks in state setters (e.g., `return current.val === newVal ? current : { ...current, val: newVal }`) to prevent returning new object references when values are identical, minimizing UI re-render pressure and GC load.
