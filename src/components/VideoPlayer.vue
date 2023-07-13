<template>
    <div>
      <h2>Video Player</h2>
      <video ref="videoPlayer" :src="videoUrl" @timeupdate="updateSubtitle" controls></video>
      <div v-if="subtitles.length > 0">
        <p v-for="(subtitle, index) in subtitles" :key="index" v-if="isSubtitleVisible(subtitle)">
          {{ subtitle.text }}
        </p>
      </div>
    </div>
  </template>
  
  <script>
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
    mounted() {
      this.loadSubtitles();
    },
    methods: {
      loadSubtitles() {
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
        const endTime = this.parseTimestamp(subtitle.timestamp) + 2; // Display subtitle for 2 seconds
        return this.currentTime >= startTime && this.currentTime <= endTime;
      },
      parseTimestamp(timestamp) {
        const parts = timestamp.split(':');
        const hours = parseInt(parts[0]);
        const minutes = parseInt(parts[1]);
        const seconds = parseInt(parts[2]);
        return hours * 3600 + minutes * 60 + seconds;
      }
    }
  };
  </script>
  