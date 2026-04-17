## 2026-04-15 - Adaptive Frame Throttle in react-native-vision-camera
**Learning:** High-frequency MediaPipe landmarker execution in a continuous mobile frame processor can cause severe thermal build-up and battery drain, even when no target object (e.g., hands) is present.
**Action:** Use `react-native-worklets-core` `useSharedValue` to track consecutive empty frames natively inside the worklet, and dynamically back-off the processing interval when idle to significantly reduce sustained CPU/GPU load without missing the target's re-entry.
## 2024-04-17 - Prevent redundant re-renders from frame processors
 **Learning:** Redundant React state updates originating from native frame processor callbacks (e.g., repeatedly passing identical label/confidence values into new objects) cause severe cascading re-renders in the camera overlay. This rapid JS bridge activity and React rendering cycle significantly increases thermal load on mobile.
 **Action:** Always implement state value equality checks (throttling object recreation) when pushing high-frequency native streaming results into React state to preserve battery and keep devices cool.
