<template>
  <div>
    <h2>Video Player</h2>
    <video ref="videoPlayer" :src="videoUrl" @timeupdate="updateSubtitle" controls></video>
    <div v-if="displayedSubtitles.length > 0">
      <p v-for="(subtitle, index) in displayedSubtitles" :key="index">
        {{ subtitle.text }}
      </p>
    </div>
    <div v-if="subtitles.length > 0">
      <h3>Play with Subtitles</h3>
      <ul>
        <li v-for="(subtitle, index) in subtitles" :key="index">
          <button @click="playWithSubtitle(subtitle)">{{ subtitle.text }}</button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  props: {
    videoUrl: {
      type: String,
      required: true
    },
    subtitlesUrl: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      subtitles: [],
      currentTime: 0
    };
  },
  computed: {
    displayedSubtitles() {
      return this.subtitles.filter(subtitle => this.isSubtitleVisible(subtitle));
    }
  },
  mounted() {
    this.loadSubtitles();
  },
  methods: {
    loadSubtitles() {
      // Your code to load subtitles from the subtitlesUrl
      // For example, using Axios:
      axios
        .get(this.subtitlesUrl)
        .then(response => {
          this.subtitles = response.data.subtitles;
        })
        .catch(error => {
          console.error('Error loading subtitles:', error);
        });
    },
    updateSubtitle(event) {
      this.currentTime = event.target.currentTime;
    },
    isSubtitleVisible(subtitle) {
      const startTime = this.parseTimestamp(subtitle.timestamp);
      const endTime = startTime + 2; // Display subtitle for 2 seconds
      return this.currentTime >= startTime && this.currentTime <= endTime;
    },
    parseTimestamp(timestamp) {
      // Your code to parse the timestamp
      return Date.parse(timestamp);
    },
    playWithSubtitle(subtitle) {
      const startTime = this.parseTimestamp(subtitle.timestamp);
      this.$refs.videoPlayer.currentTime = startTime / 1000; // Convert milliseconds to seconds
      this.$refs.videoPlayer.play();
    }
  }
};
</script>

<style scoped>
/* Your component styles here */
</style>
