// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Vuetify from 'vuetify'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/dist/vuetify.min.css'
import VueResource from 'vue-resource'
import VueSplit from 'vue-split-panel'

Vue.config.productionTip = false
Vue.use(Vuetify, {
  iconfont: 'md'
})
Vue.use(VueResource)
Vue.use(VueSplit)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
