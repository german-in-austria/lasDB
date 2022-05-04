<template>
  <div>
    <v-dialog v-model="dialogLogin" persistent max-width="400px">
      <v-card>
        <v-toolbar dark color="primary">
          <v-toolbar-title>Anmelden</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-icon>account_circle</v-icon>
        </v-toolbar>
        <v-card-text>
          <v-form>
            <v-text-field prepend-icon="person" name="username" v-model="loginName" label="Name" ref="username" required></v-text-field>
            <v-text-field prepend-icon="lock" name="password" v-model="loginPassword" label="Passwort" type="password" required></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="login" :disabled="loginReady">Login</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  name: 'DialogLogin',
  props: ['user', 'csrf'],
  data () {
    return {
      dialogLogin: false,
      loginName: '',
      loginPassword: '',
      loading: false
    }
  },
  mounted () {
    this.dialogLogin = !this.user
  },
  methods: {
    login () {
      this.loading = true
      this.$http
        .post('/system/', {
          get: 'login',
          username: this.loginName,
          password: this.loginPassword
        }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
        .then((response) => {
          if (response.data.csrf) {
            this.$emit('updateCSRFToken', response.data.csrf)
          }
          this.loading = false
        })
        .catch((err) => {
          console.log(err)
          this.loading = false
        })
    }
  },
  computed: {
    loginReady () {
      return (this.loginName.length === 0 || this.loginPassword.length === 0 || this.loading)
    }
  },
  watch: {
    user (nVal) {
      this.dialogLogin = !nVal
    },
    dialogLogin (nVal) {
      if (nVal) {
        this.$nextTick(() => this.$refs.username.focus())
      } else {
        this.loginName = ''
        this.loginPassword = ''
      }
    }
  }
}
</script>

<style scoped>
</style>
