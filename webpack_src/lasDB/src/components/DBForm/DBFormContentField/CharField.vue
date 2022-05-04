<template>
  <div>
    <v-text-field
      :color="edit ? 'primary' : 'grey darken-3'"
      :label="fieldTitle + (needValue ? ' *' : '')"
      v-model="values[field.field_name].val"
      :title="
        'field_name: ' + field.field_name + '\n' +
        'internal_type: ' + orgField.internal_type + '\n'
      "
      placeholder="empty"
      :readonly="!edit"
      :error="error"
      counter
    ></v-text-field>
  </div>
</template>

<script>
export default {
  name: 'CharField',
  props: ['tabledata', 'field', 'edit', 'values', 'fieldTitle', 'orgField', 'needValue', 'value'],
  data () {
    return {
    }
  },
  mounted () {
  },
  computed: {
    error () {
      return !(!this.needValue || (typeof this.values[this.field.field_name].val === 'string' && this.values[this.field.field_name].val.length > 0))
    }
  },
  methods: {
  },
  watch: {
    value (nVal) {
      if (typeof nVal === 'string') {
        if (nVal.trim().length === 0) {
          this.values[this.field.field_name].val = null
        }
      }
    }
  }
}
</script>

<style scoped>
</style>
