<template>
  <div class="db-filter-fk">
    <v-autocomplete
      v-model="value"
      :items="fKeyList"
      item-value="val"
      item-text="str"
      :search-input.sync="search"
      cache-items
      :label="'Filter: ' + field.field_name"
      :title="
        'field_name: ' + field.field_name + '\n' +
        'internal_type: ' + field.internal_type + '\n'
      "
      :loading="loading"
    >
      <template slot="append-outer" v-if="availableElementCount <= maxCount || (!field.related_search_fields || field.related_search_fields.length < 1)">
        <v-btn @click="getFkData" icon small :disabled="loading">
          <v-icon >mdi-reload</v-icon>
        </v-btn>
      </template>
    </v-autocomplete>
  </div>
</template>

<script>
// import AllgemeineFunktionen from '@/functions/Allgemein'

export default {
  name: 'DBFormSelectFilterForeignKey',
  props: ['tabledata', 'field', 'onlyRelated', 'options', 'csrf'],
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
    console.log(this.field)
    if (this.availableElementCount <= this.maxCount || (!this.field.related_search_fields || this.field.related_search_fields.length < 1)) {
      this.getFkData()
    }
  },
  methods: {
    getFkData (searchString) {
      if (this.loading) {
        this.searchNext = searchString
      } else {
        this.loading = true
        let pData = { getRelatedDbTable: this.field.related_model }
        if (searchString) {
          pData.searchString = searchString
        }
        if (this.onlyRelated) {
          pData.getRelatedField = this.field.field_name
          pData.getRelatedName = this.field.related_name
          pData.onlyRelated = this.onlyRelated
        }
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
      let fkList = [{val: null, str: 'all'}, {val: -1, str: 'empty'}]
      if (this.fkData && this.fkData.all) {
        fkList = [...fkList, ...this.fkData.all]
      }
      return fkList
    },
    availableElementCount () {
      return this.onlyRelated ? this.field.related_db_table_count_related : this.field.related_db_table_count
    }
  },
  watch: {
    search (nVal) {
      if (this.field.related_search_fields && this.field.related_search_fields.length > 0 && this.availableElementCount > this.maxCount && nVal && nVal.length > 1 && !(nVal === 'all' && !this.value) && !(nVal === 'empty' && this.value === -1)) {
        console.log('getFkData')
        nVal && this.getFkData(nVal)
      }
    },
    value (nVal) {
      this.$emit('filterIt', { field: this.field.field_name, val: nVal })
    }
  }
}
</script>

<style scoped>
.db-filter-fk {
  padding-right: 2px;
}
</style>
