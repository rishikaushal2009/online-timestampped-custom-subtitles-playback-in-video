<template>
  <div>
    <h2>Upload Video</h2>
    <input type="file" @change="handleFileUpload" accept="video/*" />
    <button @click="uploadVideo" :disabled="!selectedFile">Upload</button>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <p v-else-if="successMessage" class="success">{{ successMessage }}</p>
    <SubtitleForm v-if="videoId" :videoId="videoId" />
    <VideoPlayer v-if="videoId" :videoId="videoId" :videoUrl="videoUrl" :subtitlesUrl="subtitlesUrl" />
  </div>
</template>

<script>
import axios from 'axios';
import SubtitleForm from './SubtitleForm.vue';
import VideoPlayer from './VideoPlayer.vue';

export default {
  data() {
    return {
      selectedFile: null,
      errorMessage: '',
      successMessage: '',
      videoId: null,
      videoUrl: '/api/video',
      subtitlesUrl: '/api/subtitles'
    };
  },
  components: {
    SubtitleForm,
    VideoPlayer
  },
  methods: {
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },
    uploadVideo() {
      if (!this.selectedFile) {
        this.errorMessage = 'Please select a video file.';
        return;
      }
      const formData = new FormData();
      formData.append('video', this.selectedFile);
      axios
        .post('http://127.0.0.1:5000/api/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(response => {
          this.successMessage = 'Video uploaded successfully!';
          this.videoId = response.data.videoId;
          this.videoUrl = `${this.selectedFile.name}`;
          this.subtitlesUrl = `/api/subtitles/${this.videoId}`;
          this.selectedFile = null;
        })
        .catch(error => {
          this.errorMessage = 'Error uploading video: ' + error.message;
        });
    }
  }
};
</script>

<style scoped>
.error {
  color: red;
}

.success {
  color: green;
}
</style>
