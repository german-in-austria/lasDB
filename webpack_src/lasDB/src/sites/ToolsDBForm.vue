<template>
  <v-layout column fill-height>
    <div>
      <v-select
        v-model="selTable"
        :items="tables"
        item-value="name"
        item-text="title"
        label="Table"
        :loading="!fReady"
        mt-0 />
    </div>
    <DBForm :table="selTable" :user="user" :options="options" :csrf="csrf" v-if="fReady && selTable" />
  </v-layout>
</template>

<script>
import DBForm from '../components/DBForm.vue'

export default {
  name: 'ToolsDBForm',
  props: ['user', 'options', 'csrf', 'tabledata'],
  data () {
    return {
      selTable: null,
      tables: [],
      fReady: false
    }
  },
  mounted () {
    this.getTables()
  },
  watch: {
    selTable () {
      this.fReady = false
      this.$nextTick(() => {
        this.fReady = true
      })
    }
  },
  methods: {
    getTables () {
      this.fReady = false
      this.$http
        .post('/form/', { get: 'getTables' }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
        .then((response) => {
          this.tables = response.data
          this.fReady = true
        })
        .catch((err) => {
          console.log(err)
          this.fReady = true
        })
    }
  },
  components: {
    DBForm
  }
}
</script>

<style scoped>
</style>
