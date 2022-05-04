<template>
  <div>
    <v-checkbox
      :color="edit ? 'primary' : 'grey darken-3'"
      :label="fieldTitle + (needValue ? ' *' : '')"
      v-model="values[field.field_name].val"
      :title="
        'field_name: ' + field.field_name + '\n' +
        'internal_type: ' + orgField.internal_type + '\n'
      "
      :readonly="!edit"
      :error="error"
    ></v-checkbox>
  </div>
</template>

<script>
export default {
  name: 'BooleanField',
  props: ['tabledata', 'field', 'edit', 'values', 'fieldTitle', 'orgField', 'needValue', 'value'],
  data () {
    return {
    }
  },
  mounted () {
  },
  computed: {
    error () {
      return !(!this.needValue || (this.values[this.field.field_name].val === true || this.values[this.field.field_name].val === false))
    }
  },
  methods: {
  }
}
</script>

<style scoped>
</style>
