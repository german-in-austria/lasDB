<template>
  <div>
    <v-textarea
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
      auto-grow
      counter
    ></v-textarea>
  </div>
</template>

<script>
export default {
  name: 'TextField',
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
