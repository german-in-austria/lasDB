<template>
  <div>
    <v-text-field
      :color="'grey darken-3'"
      :label="fieldTitle + (needValue ? ' *' : '')"
      v-model="values[field.field_name].val"
      :title="
        'field_name: ' + field.field_name + '\n' +
        'internal_type: ' + orgField.internal_type + '\n'
      "
      placeholder="empty"
      readonly
    ></v-text-field>
  </div>
</template>

<script>
export default {
  name: 'AutoField',
  props: ['tabledata', 'field', 'edit', 'values', 'fieldTitle', 'orgField', 'needValue', 'value'],
  data () {
    return {
    }
  },
  mounted () {
  },
  computed: {
    error () {
      return false
    }
  },
  methods: {
  }
}
</script>

<style scoped>
</style>
