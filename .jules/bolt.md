## 2026-04-15 - Adaptive Frame Throttle in react-native-vision-camera
**Learning:** High-frequency MediaPipe landmarker execution in a continuous mobile frame processor can cause severe thermal build-up and battery drain, even when no target object (e.g., hands) is present.
**Action:** Use `react-native-worklets-core` `useSharedValue` to track consecutive empty frames natively inside the worklet, and dynamically back-off the processing interval when idle to significantly reduce sustained CPU/GPU load without missing the target's re-entry.
## 2026-04-20 - Prevent upper body from overriding hand presence thermal throttle
**Learning:** The adaptive thermal throttle for hand tracking was mistakenly keeping the camera at 33 FPS because the upper body was almost always in the frame. Only tracking `hasHand` allows the app to correctly drop the frame rate when no hands are present.
**Action:** Ensure thermal throttle criteria strictly reflect the condition where work is actually required, excluding unneeded bounding boxes like the upper body.
## 2026-04-20 - Prevent identical state object creations on every frame
**Learning:** React state updaters were creating new object references continuously at 30+ FPS even when state values remained the same, causing severe React Native bridge churn.
**Action:** Perform strict equality checks within state updater callbacks to return the current state object if unmodified, allowing React to bail out of unnecessary re-renders.
