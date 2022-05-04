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
      :hint="'Unknowen Type: ' + orgField.internal_type"
      persistent-hint
    ></v-text-field>
  </div>
</template>

<script>
export default {
  name: 'UnknowenField',
  props: ['tabledata', 'field', 'edit', 'values', 'fieldTitle', 'orgField', 'needValue', 'value'],
  data () {
    return {
    }
  },
  mounted () {
  },
  computed: {
    error () {
      return !(!this.needValue || (this.values[this.field.field_name].val !== null))
    }
  },
  methods: {
  }
}
</script>

<style scoped>
</style>
