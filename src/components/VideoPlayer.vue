<template>
  <div>
    <h2>Video Player</h2>
    <div id="player-container"></div>
    <div v-if="subtitlesLoaded && savedSubtitles.length > 0">
      <h3>Saved Subtitles:</h3>
      <p v-for="(subtitle, index) in savedSubtitles" :key="index">
        {{ subtitle.text }}
      </p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, inject, watch } from 'vue';
import axios from 'axios';

export default {
  props: {
    videoId: {
      type: [String, null],
      required: true
    },
    videoUrl: {
      type: String,
      required: true
    },
    subtitlesUrl: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const playerContainer = ref(null);
    const subtitlesLoaded = ref(false);
    const savedSubtitles = ref([]);

    const fetchSubtitles = () => {
      axios
        .get('http://127.0.0.1:5000/api/subtitles/' + props.subtitlesUrl)
        .then(response => {
          savedSubtitles.value = response.data.subtitles;
          subtitlesLoaded.value = true;
          addSubtitlesToVideo(response.data.subtitles);
        })
        .catch(error => {
          console.warn('Subtitles file not found:', error);
          savedSubtitles.value = [];
          subtitlesLoaded.value = false;
        });
    };

    const addSubtitlesToVideo = (subtitles) => {
      const videoElement = playerContainer.value.querySelector('video');
      subtitles.forEach(subtitle => {
        const trackElement = document.createElement('track');
        trackElement.kind = 'subtitles';
        trackElement.src = subtitle.src;
        trackElement.srclang = subtitle.language;
        trackElement.label = subtitle.label;
        videoElement.appendChild(trackElement);
      });
    };

    let videoElement = null;

    onMounted(() => {
      const eventBus = inject('$eventBus');
      if (eventBus && eventBus.on) {
        eventBus.on('subtitles-saved', fetchSubtitles);
      }

      playerContainer.value = document.querySelector('#player-container');
      videoElement = document.createElement('video');
      videoElement.src = 'http://127.0.0.1:5000' + props.videoUrl;
      videoElement.controls = true; // Enable video controls
      playerContainer.value.appendChild(videoElement);
    });

    onUnmounted(() => {
      const eventBus = inject('$eventBus');
      if (eventBus && eventBus.off) {
        eventBus.off('subtitles-saved', fetchSubtitles);
      }
    });

    watch(
      () => props.subtitlesUrl,
      (newSubtitlesUrl) => {
        if (newSubtitlesUrl) {
          fetchSubtitles();
        }
      }
    );

    return {
      playerContainer,
      subtitlesLoaded,
      savedSubtitles
    };
  }
};
</script>

<style scoped>
/* Your component styles here */
</style>
