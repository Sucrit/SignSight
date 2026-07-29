import React, { useCallback, useEffect, useRef } from "react";
import { StyleSheet, Pressable } from "react-native";
import { useVideoPlayer, VideoView } from "expo-video";

export default function VideoSplashScreen({ onFinish }: { onFinish: () => void }) {
  const doneRef = useRef(false);

  const finishOnce = useCallback(() => {
    if (doneRef.current) return;
    doneRef.current = true;
    onFinish();
  }, [onFinish]);

  const player = useVideoPlayer(require("../../assets/splash/splash.mp4"), (videoPlayer) => {
    videoPlayer.loop = false;
    videoPlayer.play();
  });

  useEffect(() => {
    const subscription = player.addListener("playToEnd", finishOnce);
    return () => subscription.remove();
  }, [finishOnce, player]);

  return (
    <Pressable style={styles.container} onPress={finishOnce}>
      <VideoView
        player={player}
        style={StyleSheet.absoluteFill}
        contentFit="cover"
        nativeControls={false}
        allowsFullscreen={false}
      />
    </Pressable>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "black" },
});
