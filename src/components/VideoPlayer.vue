<template>
  <div>
    <h2>Video Player</h2>
    <!--video ref="videoPlayer" :src="videoSource" @timeupdate="updateSubtitle" controls></video-->
    <video ref="videoPlayer" :src="videoSource"  autoplay="autoplay" controls="controls"></video>
    <!--
    <div v-if="displayedSubtitles.length > 0">
      <p v-for="(subtitle, index) in displayedSubtitles" :key="index">
        {{ subtitle.text }}
      </p>
    </div>
  -->
  </div>
</template>

<script>
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
  data() {
    return {
      //subtitles: [],
      //currentTime: 0,
      videoSource: ''
    };
  },
/*
  computed: {
    displayedSubtitles() {
      return this.subtitles.filter(subtitle => this.isSubtitleVisible(subtitle));
    }
  },
  */
  mounted() {
    //this.loadSubtitles();
    this.fetchVideoSource();
    //this.videoUrl
  },

  methods: {
   /* 
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
      const endTime = startTime + 2; // Display subtitle for 2 seconds
      return this.currentTime >= startTime && this.currentTime <= endTime;
    },
    parseTimestamp(timestamp) {
      // Split the timestamp into hours, minutes, and seconds
      const [hours, minutes, seconds] = timestamp.split(':');

      // Calculate the total milliseconds from hours, minutes, and seconds
      const milliseconds = ((Number(hours) * 60 + Number(minutes)) * 60 + Number(seconds)) * 1000;

      return milliseconds;
    },
    */
    fetchVideoSource() {
  // Make an AJAX request to your Flask server to get the video source URL
  // Replace '/video/filename.mp4' with the appropriate URL to your Flask route
  console.log(decodeURIComponent(this.videoUrl));
  const abc = decodeURIComponent(this.videoUrl);
  axios
    .get('http://127.0.0.1:5000/api/uploads/' + abc, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
    })
    .then(response => {
      this.videoSource = response.data.videoSource; // Update videoSource with the received URL from the server
      //console.log(this.videoSource);
    })
    .catch(error => {
      console.error('Error fetching video source:', error);
    });
}

   
  }

};
</script>

<style scoped>
/* Your component styles here */
</style>

