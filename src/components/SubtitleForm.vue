<template>
    <div>
      <h2>Add Subtitles</h2>
      <div v-for="(subtitle, index) in subtitles" :key="index">
        <input type="text" v-model="subtitle.text" placeholder="Subtitle text" />
        <input type="text" v-model="subtitle.timestamp" placeholder="Timestamp (e.g., 00:00:10)" />
        <button @click="removeSubtitle(index)">Remove</button>
      </div>
      <button @click="addSubtitle">Add Subtitle</button>
      <button @click="saveSubtitles" :disabled="subtitles.length === 0">Save Subtitles</button>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <p v-else-if="successMessage" class="success">{{ successMessage }}</p>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        subtitles: [],
        errorMessage: '',
        successMessage: ''
      };
    },
    methods: {
      addSubtitle() {
        this.subtitles.push({ text: '', timestamp: '' });
      },
      removeSubtitle(index) {
        this.subtitles.splice(index, 1);
      },
      saveSubtitles() {
        if (this.subtitles.length === 0) {
          this.errorMessage = 'No subtitles to save.';
          return;
        }
        const subtitleData = {
          subtitles: this.subtitles
        };
        axios
          .post('/api/subtitles', subtitleData)
          .then(() => {
            this.successMessage = 'Subtitles saved successfully!';
            this.subtitles = [];
          })
          .catch(error => {
            this.errorMessage = 'Error saving subtitles: ' + error.message;
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
  