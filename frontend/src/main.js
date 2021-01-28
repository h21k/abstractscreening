/*
import Vue from 'vue'
import App from './App.vue'
Vue.config.productionTip = false
new Vue({
  render: h => h(App),
}).$mount('#app')
*/
// frontend/src/main.js
import "bootstrap/dist/css/bootstrap.css";
import BootstrapVue from "bootstrap-vue";
import Vue from "vue";
import App from "./App.vue";
import router from "./router";

import firebase from "./firebaseInit";
const db = firebase.firestore()

Vue.use(BootstrapVue);

Vue.config.productionTip = false;
new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
