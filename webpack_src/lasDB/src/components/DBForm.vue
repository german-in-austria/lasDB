<template>
  <v-layout row class="dbform-main">
    <v-flex xs12 md2>
      <DBFormSelect ref="dbformselect"
        :tabledata="tableData"
        :user="user"
        :options="options"
        :csrf="csrf"
        :contentID="contentID"
        @loadcontent="loadContent"
        v-if="!loading && tableData.data" />
    </v-flex>
    <v-flex xs12 md10>
      <DBFormContent ref="dbformcontent"
        :tabledata="tableData"
        :user="user"
        :options="options"
        :csrf="csrf"
        :contentID="contentID"
        @contentUpdated="contentUpdated"
        @close="contentID = 0"
        v-if="!loading && tableData.data && contentID"
      >
        <template slot="extraBtns">
          <slot name="extraBtns" />
        </template>
      </DBFormContent>
      <div class="pa-4" v-else>
        <v-btn @click="contentID = -1" color="primary" class="pl-2"><v-icon>mdi-plus</v-icon> New Entrie</v-btn>
      </div>
    </v-flex>
  </v-layout>
</template>

<script>
import DBFormSelect from './DBForm/DBFormSelect.vue'
import DBFormContent from './DBForm/DBFormContent.vue'

export default {
  name: 'DBForm',
  props: ['user', 'options', 'csrf', 'table', 'form'],
  data () {
    return {
      loading: false,
      tableData: { data: null },
      contentID: 0
    }
  },
  mounted () {
    console.log('DBForm mounted ...')
    this.getTable()
  },
  methods: {
    contentUpdated (id, sortFieldValue, oldSortFieldValue) {
      this.$refs.dbformselect.contentUpdated(id, sortFieldValue, oldSortFieldValue, id !== this.contentID)
      if (id > 0) {
        this.loadContent(id)
      }
    },
    loadContent (aId) {
      this.contentID = 0
      this.$nextTick(() => { this.contentID = aId })
    },
    getTable () {
      this.loading = true
      this.$http
        .post('/form/', {
          get: 'getTable',
          getModel: this.table,
          getOptions: this.form ? this.form : ''
        }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
        .then((response) => {
          console.log(response.data)
          this.tableData.data = response.data
          this.loading = false
        })
        .catch((err) => {
          console.log(err)
          this.loading = false
        })
    }
  },
  components: {
    DBFormSelect,
    DBFormContent
  }
}
</script>

<style scoped>
.dbform-main {
  border: 1px solid #ddd;
  height: 100%;
}
</style>
