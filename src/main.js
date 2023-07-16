/*import { createApp } from 'vue';
import App from './App.vue';

const app = createApp(App);

const eventBus = {
  $on: (event, callback) => {
    app.config.globalProperties.$emitter.on(event, callback);
  },
  $off: (event, callback) => {
    app.config.globalProperties.$emitter.off(event, callback);
  },
  $emit: (event, ...args) => {
    app.config.globalProperties.$emitter.emit(event, ...args);
  }
};

app.config.globalProperties.$eventBus = eventBus;

app.mount('#app');
*/

import { createApp } from 'vue';
import App from './App.vue';

const app = createApp(App);

const eventBus = {
  emit(event, ...args) {
    this[event]?.forEach(fn => fn(...args));
  },
  on(event, fn) {
    if (!this[event]) {
      this[event] = [];
    }
    this[event].push(fn);
  },
  off(event, fn) {
    if (!this[event]) {
      return;
    }
    const index = this[event].indexOf(fn);
    if (index !== -1) {
      this[event].splice(index, 1);
    }
  }
};

app.provide('$eventBus', eventBus);

app.mount('#app');





