<template>
    <div>
      <h2>Upload Video</h2>
      <input type="file" @change="handleFileUpload" accept="video/*" />
      <button @click="uploadVideo" :disabled="!selectedFile">Upload</button>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <p v-else-if="successMessage" class="success">{{ successMessage }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        selectedFile: null,
        errorMessage: '',
        successMessage: ''
      };
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
          .post('/api/upload', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
          .then(() => {
            this.successMessage = 'Video uploaded successfully!';
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
  