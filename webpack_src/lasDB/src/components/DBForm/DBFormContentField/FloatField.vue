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
      type="number"
      step="0.01"
    ></v-text-field>
  </div>
</template>

<script>
export default {
  name: 'FloatField',
  props: ['tabledata', 'field', 'edit', 'values', 'fieldTitle', 'orgField', 'needValue', 'value'],
  data () {
    return {
    }
  },
  mounted () {
  },
  computed: {
    error () {
      return !(!this.needValue || (typeof this.values[this.field.field_name].val === 'number'))
    }
  },
  methods: {
  },
  watch: {
    value (nVal) {
      if (typeof nVal === 'string') {
        if (nVal.trim().length > 0) {
          this.values[this.field.field_name].val = parseFloat(nVal)
        } else {
          this.values[this.field.field_name].val = null
        }
      }
    }
  }
}
</script>

<style scoped>
</style>
