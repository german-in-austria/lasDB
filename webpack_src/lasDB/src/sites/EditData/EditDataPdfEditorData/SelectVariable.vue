<template>
  <div class="select-variable">
    <v-autocomplete
      v-model="value"
      :items="fKeyList"
      label="select variable"
      item-value="val"
      item-text="str"
      :search-input.sync="search"
      cache-items
      :loading="loading"
    >
      <template slot="append-outer">
        <v-btn @click="$emit('select', value)" color="primary" small :disabled="loading || value < 1">
          select
        </v-btn>
      </template>
    </v-autocomplete>
  </div>
</template>

<script>
// import AllgemeineFunktionen from '@/functions/Allgemein'

export default {
  name: 'SelectVariable',
  props: ['options', 'csrf'],
  data () {
    return {
      fkData: {},
      loading: false,
      value: null,
      search: null,
      searchNext: null,
      maxCount: 100
    }
  },
  mounted () {
  },
  methods: {
    getFkData (searchString) {
      if (this.loading) {
        this.searchNext = searchString
      } else {
        this.loading = true
        let pData = { getRelatedDbTable: 'lex_variable' }
        pData.searchString = searchString
        pData.get = 'getRelatedDbTable'
        this.$http
          .post('/form/', pData, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
          .then((response) => {
            console.log(response.data)
            this.fkData = response.data
            this.loading = false
            if (this.searchNext) {
              this.getFkData(this.searchNext)
              this.searchNext = null
            }
          })
          .catch((err) => {
            console.log(err)
            this.loading = false
          })
      }
    }
  },
  computed: {
    fKeyList () {
      let fkList = [{val: -1, str: 'None'}]
      if (this.fkData && this.fkData.all) {
        fkList = [...fkList, ...this.fkData.all]
      }
      return fkList
    }
  },
  watch: {
    search (nVal) {
      if (nVal && nVal.length > 1 && !(nVal === 'empty' && this.value === -1)) {
        nVal && this.getFkData(nVal)
      }
    }
  }
}
</script>

<style scoped>
</style>
