<template>
  <div>
    <h1>My Video Application</h1>
    <VideoUploader />
    <SubtitleForm />
    <VideoPlayer :videoUrl="videoUrl" :subtitlesUrl="subtitlesUrl" />
  </div>
</template>

<script>
import VideoUploader from './components/VideoUploader.vue';
import SubtitleForm from './components/SubtitleForm.vue';
import VideoPlayer from './components/VideoPlayer.vue';

export default {
  components: {
    VideoUploader,
    SubtitleForm,
    VideoPlayer
  },
  data() {
    return {
      videoUrl: '/api/video', // Replace with the correct URL for your video API
      subtitlesUrl: '/api/subtitles' // Replace with the correct URL for your subtitles API
    };
  }
};
</script>

<style>
/* Add your custom CSS styles here */
</style>
















