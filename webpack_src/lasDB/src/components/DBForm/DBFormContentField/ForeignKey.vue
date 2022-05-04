<template>
  <div>
    <v-autocomplete
      :color="edit ? 'primary' : 'grey darken-3'"
      :label="fieldTitle + (needValue ? ' *' : '')"
      v-model="values[field.field_name].val"
      :items="fKeyList"
      item-value="val"
      item-text="str"
      :search-input.sync="search"
      cache-items
      :title="
        'field_name: ' + field.field_name + '\n' +
        'internal_type: ' + orgField.internal_type + '\n'
      "
      placeholder="empty"
      :hint="countAll === 0 || countAll > 0 ? countAll + ' Entries' : ''"
      :persistent-hint="countAll === 0 || countAll > 0"
      :readonly="!edit"
      :error="error"
      :loading="loading"
      v-if="!update"
    >
      <template slot="append-outer" v-if="edit && (orgField.related_db_table_count <= maxCount || (!orgField.related_search_fields || orgField.related_search_fields.length < 1))">
        <v-btn @click="getFkData" icon small :disabled="loading">
          <v-icon>mdi-reload</v-icon>
        </v-btn>
      </template>
    </v-autocomplete>
  </div>
</template>

<script>
import AllgemeineFunktionen from '@/functions/Allgemein'

export default {
  name: 'ForeignKey',
  props: ['tabledata', 'field', 'edit', 'values', 'fieldTitle', 'orgField', 'needValue', 'value', 'filter', 'csrf'],
  data () {
    return {
      fkData: {},
      loading: false,
      search: null,
      searchNext: null,
      maxCount: 50,
      update: false,
      nextSelect: null,
      getAgain: false
    }
  },
  mounted () {
    if (this.edit && (this.orgField.related_db_table_count <= this.maxCount || (!this.orgField.related_search_fields || this.orgField.related_search_fields.length < 1))) {
      this.getFkData()
    }
  },
  methods: {
    getFkData (searchString) {
      if (this.loading) {
        if (searchString) {
          this.searchNext = searchString
        } else {
          this.getAgain = true
        }
      } else {
        this.loading = true
        let pData = {
          get: 'getRelatedDbTable',
          getRelatedDbTable: this.orgField.related_model
        }
        if (this.filter) {
          pData.filter = this.filter
        }
        if (searchString) {
          pData.searchString = searchString
        }
        this.$http
          .post('/form/', pData, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
          .then((response) => {
            console.log(this.fieldTitle, response.data)
            this.fkData = response.data
            this.loading = false
            if (this.searchNext) {
              this.getFkData(this.searchNext)
              this.searchNext = null
            } else if (this.getAgain) {
              this.getFkData()
              this.getAgain = false
            } else if (this.filter) {
              this.update = true
            }
            if (this.nextSelect) {
              this.selectByVal(this.nextSelect)
            }
          })
          .catch((err) => {
            console.log(err)
            this.loading = false
          })
      }
    },
    selectByVal (sVal) {
      let nSel = this.fKeyList.filter(d => d.val === sVal)
      if (nSel.length > 0) {
        this.values[this.field.field_name].val = nSel[0].val
        this.nextSelect = null
      } else {
        this.nextSelect = this.nextSelect !== sVal ? sVal : null
      }
    }
  },
  computed: {
    countAll () {
      return this.filter ? (this.fkData && this.fkData.count ? this.fkData.count : null) : (this.fkData && this.fkData.countall ? this.fkData.countall : null)
    },
    fKeyList () {
      let fkList = [{val: null, str: 'empty'}]
      if (this.fkData && this.fkData.all) {
        fkList = [...fkList, ...this.fkData.all]
      }
      if (this.values[this.field.field_name].val && !AllgemeineFunktionen.getFirstObjectOfValueInPropertyOfArray(fkList, 'val', this.values[this.field.field_name].val)) {
        fkList.push({val: this.values[this.field.field_name].val, str: this.values[this.field.field_name].str})
      }
      return fkList
    },
    error () {
      return !(!this.needValue || (typeof this.values[this.field.field_name].val === 'number' && this.values[this.field.field_name].val > 0))
    }
  },
  watch: {
    search (nVal) {
      if (this.edit && this.orgField.related_search_fields && this.orgField.related_search_fields.length > 0 && this.orgField.related_db_table_count > this.maxCount && nVal && nVal.length > 1) {
        nVal && nVal !== this.values[this.field.field_name].nVal && this.getFkData(nVal)
      }
    },
    edit (nVal) {
      if (this.edit && (this.orgField.related_db_table_count <= this.maxCount || (!this.orgField.related_search_fields || this.orgField.related_search_fields.length < 1))) {
        this.getFkData()
      }
    },
    filter (nVal) {
      this.getFkData()
    },
    update (nVal) {
      if (nVal) {
        this.$nextTick(() => {
          this.update = false
        })
      }
    }
  }
}
</script>

<style scoped>
</style>
