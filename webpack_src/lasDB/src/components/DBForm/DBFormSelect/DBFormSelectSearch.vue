<template>
  <div class="db-search">
    <v-text-field
      label="Search"
      v-model="search"
      :loading="loading"
      :title="'Search Fields: ' + tabledata.data.model.search_fields.join(', ')"
    >
      <v-icon @click="search = ''" slot="append" color="grey" v-if="search && search.length > 0">close</v-icon>
    </v-text-field>
  </div>
</template>

<script>
import _ from 'lodash'

export default {
  name: 'DBFormSelectSearch',
  props: ['tabledata', 'options', 'csrf', 'loading'],
  data () {
    return {
      search: ''
    }
  },
  mounted () {
    console.log(this.tabledata)
  },
  methods: {
    startSearch () {
      this.$emit('searchIt', { val: this.search })
    },
    debouncedSearch: _.debounce(function () {
      this.startSearch()
    }, 500)
  },
  computed: {
  },
  watch: {
    search (nVal) {
      if (!nVal || nVal.length < 1) {
        this.startSearch()
      } else {
        this.debouncedSearch()
      }
    }
  }
}
</script>

<style scoped>
</style>
