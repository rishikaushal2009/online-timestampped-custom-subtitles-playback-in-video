<template>
  <div>
    <h2>Video Player</h2>
    <video ref="videoPlayer" :src="videoSource" autoplay controls @play="handleVideoPlay"></video>
    <div v-if="displayedSubtitles.length > 0">
      <p v-for="(subtitle, index) in displayedSubtitles" :key="index">
        {{ subtitle.text }}
      </p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, computed } from 'vue';
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
    const videoPlayer = ref(null); // Create a ref to the video element

    const videoSource = ref('');
    const subtitles = ref([]);
    const subtitlesLoaded = ref(false);

    const fetchVideoSource = () => {
      const videoUrl = decodeURIComponent(props.videoUrl);
      axios
        .get('http://127.0.0.1:5000/api/uploads/'+ videoUrl, {
          responseType: 'blob'
        })
        .then(response => {
          const videoBlob = new Blob([response.data], { type: 'video/mp4' });
          videoSource.value = URL.createObjectURL(videoBlob);
        })
        .catch(error => {
          console.error('Error fetching video source:', error);
          videoSource.value = ''; // Set video source to an empty string or a default value
        });
    };

    const fetchSubtitles = () => {
      const subtitlesUrl = `${props.videoId}_subtitles.txt`;
      axios
        .get(`http://127.0.0.1:5000/api/subtitles/${subtitlesUrl}`)
        .then(response => {
          subtitles.value = response.data.subtitles;
          subtitlesLoaded.value = true;
        })
        .catch(error => {
          console.warn('Subtitles file not found:', error);
          subtitles.value = []; // Set subtitles to an empty array if file not found
          subtitlesLoaded.value = false;
        });
    };

    const isSubtitleVisible = (subtitle, currentTime) => {
      const startTime = parseTimestamp(subtitle.startTime);
      const endTime = parseTimestamp(subtitle.endTime);

      return currentTime >= startTime && currentTime <= endTime;
    };

    const parseTimestamp = timestamp => {
      const [hours, minutes, seconds] = timestamp.split(':');
      return (parseInt(hours) * 3600 + parseInt(minutes) * 60 + parseInt(seconds)) * 1000;
    };

    const displayedSubtitles = computed(() => {
      const currentTime = videoPlayer.value ? videoPlayer.value.currentTime * 1000 : 0;
      return subtitles.value.filter(subtitle => isSubtitleVisible(subtitle, currentTime));
    });

    onMounted(() => {
      fetchVideoSource();
    });

    /* eslint-disable no-unused-vars */
    const handleVideoPlay = () => {
      // Only fetch subtitles if the subtitles are not yet loaded
      if (!subtitlesLoaded.value) {
        fetchSubtitles();
      }
    };
    /* eslint-disable no-unused-vars */

    onUnmounted(() => {
      // Clean up any event listeners or subscriptions here
    });

    return {
      videoPlayer,
      videoSource,
      displayedSubtitles
    };
  }
};
</script>

<style scoped>
/* Your component styles here */
</style>
