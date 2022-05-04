<template>
  <div>
    <v-select
      :color="edit ? 'primary' : 'grey darken-3'"
      :label="fieldTitle + (needValue ? ' *' : '')"
      v-model="values[field.field_name].val"
      :items="selectableItems"
      item-value="0"
      item-text="1"
      :title="
        'field_name: ' + field.field_name + '\n' +
        'internal_type: ' + orgField.internal_type + '\n'
      "
      placeholder="empty"
      :readonly="!edit"
      :error="error"
    ></v-select>
  </div>
</template>

<script>
export default {
  name: 'FxChoices',
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
    },
    selectableItems () {
      let addChoices = []
      if (this.values[this.field.field_name].val && this.orgField.choices.indexOf(this.values[this.field.field_name].val) < 1) {
        addChoices.push([this.values[this.field.field_name].val, this.values[this.field.field_name].val + ' (value not available)'])
      }
      return [[null, 'empty'], ...this.orgField.choices, ...addChoices]
    }
  },
  methods: {
  }
}
</script>

<style scoped>
</style>
