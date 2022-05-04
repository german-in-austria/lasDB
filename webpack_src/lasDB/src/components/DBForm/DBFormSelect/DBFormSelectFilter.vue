<template>
  <div class="db-filter">
    <template v-for="field in fields">
      <DBFormSelectFilterForeignKey v-if="field.internal_type === 'ForeignKey'" :onlyRelated="true" @filterIt="filterIt" :tabledata="tabledata" :field="field" :options="options" :csrf="csrf" :key="'dbf-' + field.field_name" />
      <div :key="'dbf-' + field.field_name" v-else>
        <b>{{ field.field_name }}</b> - Unknown Type: <b>{{ field.internal_type }}</b>
      </div>
    </template>
  </div>
</template>

<script>
import DBFormSelectFilterForeignKey from './DBFormSelectFilterForeignKey'

export default {
  name: 'DBFormSelectFilter',
  props: ['tabledata', 'options', 'csrf'],
  data () {
    return {
    }
  },
  mounted () {
  },
  methods: {
    filterIt (val) {
      this.$emit('filterIt', val)
    }
  },
  computed: {
    fields () {
      let aFields = []
      this.tabledata.data.model.fields.forEach(f => {
        if (this.tabledata.data.model.filter_fields.indexOf(f.field_name) > -1) {
          aFields.push(f)
        }
      })
      console.log(aFields)
      return aFields
    }
  },
  watch: {
  },
  components: {
    DBFormSelectFilterForeignKey
  }
}
</script>

<style scoped>
</style>
