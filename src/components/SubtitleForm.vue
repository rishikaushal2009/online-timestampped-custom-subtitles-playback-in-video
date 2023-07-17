<template>
  <div>
    <h2>Add Subtitles</h2>
    <div v-for="(subtitle, index) in subtitles" :key="index">
      <input type="text" v-model="subtitle.text" placeholder="Subtitle text" />
      <input type="text" v-model="subtitle.timestamp" placeholder="Timestamp (e.g., 00:00:10)" />
      <input type="text" v-model="subtitle.src" placeholder="Subtitle source URL" />
      <input type="text" v-model="subtitle.language" placeholder="Subtitle language" />
      <input type="text" v-model="subtitle.label" placeholder="Subtitle label" />
      <button @click="removeSubtitle(index)">Remove</button>
    </div>
    <button @click="addSubtitle">Add Subtitle</button>
    <button @click="saveSubtitles" :disabled="subtitles.length === 0">Save Subtitles</button>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <p v-else-if="successMessage" class="success">{{ successMessage }}</p>
  </div>
</template>

<script>
import { inject, ref } from 'vue';
import axios from 'axios';

export default {
  props: {
    videoId: {
      type: [String, null],
      required: true
    }
  },
  setup(props) {
    const subtitles = ref([]);
    const errorMessage = ref('');
    const successMessage = ref('');

    const addSubtitle = () => {
      subtitles.value.push({
        text: '',
        timestamp: '',
        src: '',
        language: '',
        label: ''
      });
    };

    const removeSubtitle = (index) => {
      subtitles.value.splice(index, 1);
    };

    const saveSubtitles = () => {
      if (subtitles.value.length === 0) {
        errorMessage.value = 'No subtitles to save.';
        return;
      }

      // Format the subtitles before sending
      const formattedSubtitles = subtitles.value.map(subtitle => {
        return {
          startTime: subtitle.timestamp,
          endTime: subtitle.timestamp + 5, // Display the subtitle for 5 seconds
          text: subtitle.text,
          src: subtitle.src,
          language: subtitle.language,
          label: subtitle.label
        };
      });

      const subtitleData = {
        videoId: props.videoId,
        subtitles: formattedSubtitles
      };

      axios
        .post('http://127.0.0.1:5000/api/subtitles', subtitleData)
        .then(() => {
          successMessage.value = 'Subtitles saved successfully!';
          const eventBus = inject('$eventBus');
          if (eventBus && eventBus.emit) {
            eventBus.emit('subtitles-saved');
          }
          subtitles.value = [];
        })
        .catch(error => {
          errorMessage.value = 'Error saving subtitles: ' + error.message;
        });
    };

    return {
      subtitles,
      errorMessage,
      successMessage,
      addSubtitle,
      removeSubtitle,
      saveSubtitles
    };
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
