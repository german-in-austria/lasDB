<template>
  <div id="app">
    <v-app>
      <v-toolbar app dark color="primary" style="z-index:100000;">
        <v-container d-flex-x-t py-0>
          <v-toolbar-side-icon to="/"><v-icon>home</v-icon></v-toolbar-side-icon>
          <v-toolbar-title class="white--text">lasDB</v-toolbar-title>
          <v-spacer />
          <v-toolbar-items>
            <v-menu right offset-y v-if="user">
              <template v-slot:activator="{ on }">
                <v-btn flat v-on="on" class="not-upper">Edit<v-icon right class="ml-1">arrow_drop_down</v-icon></v-btn>
              </template>
              <v-list>
                <v-list-tile to="/edit/data/"><v-list-tile-title>Data</v-list-tile-title></v-list-tile>
                <v-list-tile to="/edit/informants/"><v-list-tile-title>Informants</v-list-tile-title></v-list-tile>
                <v-list-tile to="/edit/locations/"><v-list-tile-title>Locations</v-list-tile-title></v-list-tile>
                <v-list-tile to="/edit/questions/"><v-list-tile-title>Questions</v-list-tile-title></v-list-tile>
                <v-list-tile to="/edit/variables/"><v-list-tile-title>Variables</v-list-tile-title></v-list-tile>
                <v-list-tile to="/edit/variantgroups/"><v-list-tile-title>Variant Groups</v-list-tile-title></v-list-tile>
                <v-list-tile to="/edit/variantgrouptypes/"><v-list-tile-title>Variant Group Types</v-list-tile-title></v-list-tile>
                <v-list-tile to="/edit/languages/"><v-list-tile-title>Languages</v-list-tile-title></v-list-tile>
                <v-list-tile to="/edit/assignmentvariantgroups/"><v-list-tile-title>Assignment Variant Groups</v-list-tile-title></v-list-tile>
                <v-list-tile to="/edit/mapvariantgroups/"><v-list-tile-title>Map to Variantgroups</v-list-tile-title></v-list-tile>
              </v-list>
            </v-menu>
            <v-btn flat to="/results/map/" class="not-upper">Map</v-btn>
            <v-btn flat to="/results/explore/" class="not-upper">Explore</v-btn>
            <v-menu left offset-y v-if="user">
              <template v-slot:activator="{ on }">
                <v-btn flat v-on="on" class="not-upper" title="DB Tools"><v-icon>build</v-icon></v-btn>
              </template>
              <v-list>
                <v-list-tile to="/tools/diagram/"><v-list-tile-title>Diagram</v-list-tile-title></v-list-tile>
                <v-list-tile to="/tools/dbform/"><v-list-tile-title>DB Form</v-list-tile-title></v-list-tile>
                <v-list-tile to="/tools/map/"><v-list-tile-title>Informants Map</v-list-tile-title></v-list-tile>
              </v-list>
            </v-menu>
          </v-toolbar-items>
          <v-toolbar-title class="white--text text-uppercase" v-if="user">{{ user ? user.name : 'Unbekannt' }}</v-toolbar-title>
          <v-speed-dial v-model="fab" direction="bottom" transition="slide-y-transition" v-if="user">
            <template v-slot:activator>
              <v-toolbar-side-icon v-model="fab" fab small >
                <v-icon class="fontsize-24 d-flex-x">account_circle</v-icon>
                <v-icon class="fontsize-24 d-flex-x">close</v-icon>
              </v-toolbar-side-icon>
            </template>
            <v-btn fab dark small color="red" @click="logout" title="Logout"><v-icon class="fontsize-24">exit_to_app</v-icon></v-btn>
          </v-speed-dial>
          <v-btn flat @click="loginNow = true" class="not-upper" v-if="!user">Login</v-btn>
        </v-container>
      </v-toolbar>
      <v-content>
        <v-container flex h-100>
          <router-view :user="user" :options="options" :csrf="csrf" v-if="user || this.$route.name === 'ResultsMap' || this.$route.name === 'ResultsExplore'" />
        </v-container>
        <DialogLogin :user="user" @updateCSRFToken="updateCSRFToken" :csrf="csrf" v-if="loginNow" />
      </v-content>
    </v-app>
  </div>
</template>

<script>
/* global csrf */
import DialogLogin from './components/DialogLogin.vue'

export default {
  name: 'App',
  data () {
    return {
      csrf: null,
      user: null,
      loginNow: false,
      loading: true,
      fab: false,
      options: {edit: {}}
    }
  },
  mounted () {
    this.csrf = csrf
    this.updateStatus()
  },
  methods: {
    updateStatus () {
      this.loading = true
      this.$http
        .post('/system/', { get: 'status' }, { headers: {'X-CSRFToken': this.csrf}, emulateJSON: true })
        .then((response) => {
          // console.log(response.data)
          this.user = response.data.user
          this.loading = false
        })
        .catch((err) => {
          console.log(err)
          this.loading = false
        })
    },
    updateCSRFToken (nToken) {
      // console.log(this.csrf, '->', nToken)
      this.csrf = nToken
      this.updateStatus()
    },
    logout () {
      this.loading = true
      this.$http
        .post('/system/', { get: 'logout' }, { headers: {'X-CSRFToken': this.csrf}, emulateJSON: true })
        .then((response) => {
          this.updateCSRFToken(response.data.csrf)
          this.loading = false
        })
        .catch((err) => {
          console.log(err)
          this.updateStatus()
          this.loading = false
        })
    }
  },
  components: {
    DialogLogin
  }
}
</script>

<style>
  .container {
    max-width: 1785px!important;
  }
  .text-center {
    text-align: center;
  }
  .h-100 {
    height: 100%;
  }
  .w-25 {
    width: 25%;
  }
  .w-50 {
    width: 50%;
  }
  .w-75 {
    width: 75%;
  }
  .w-100 {
    width: 100%;
  }
  .horizontal-div .hdiv-double .w-25 {
    width: 50%;
  }
  .horizontal-div .hdiv-double .w-50 {
    width: 100%;
  }
  .horizontal-div .hdiv-double .w-75 {
    width: 100%;
  }
  .f-r {
    float: right;
  }
  .v-toolbar__content {
    justify-content: center !important;
  }
  .d-flex-x {
    display: flex !important;
  }
  .d-flex-x-t {
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    height: inherit;
  }
  .p-relative {
    position: relative;
  }
  .not-upper {
    text-transform: none !important;
  }
  .fontsize-24 {
    font-size: 24px!important;
  }
</style>
