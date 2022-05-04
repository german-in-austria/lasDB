<template>
  <div class="field pr-4" :style="'width:' + aWidth + '%'" v-if="field.show">
    <AutoField             v-if="orgField.internal_type === 'AutoField'"      :csrf="csrf" :tabledata="tabledata" :field="field" :edit="edit" :values="values" :value="values[field.field_name].val" :fieldTitle="fieldTitle" :orgField="orgField" ref="field" :needValue="needValue" />
    <FxChoices        v-else-if="orgField.choices"                            :csrf="csrf" :tabledata="tabledata" :field="field" :edit="edit" :values="values" :value="values[field.field_name].val" :fieldTitle="fieldTitle" :orgField="orgField" ref="field" :needValue="needValue" />
    <ForeignKey       v-else-if="orgField.internal_type === 'ForeignKey'"     :csrf="csrf" :tabledata="tabledata" :field="field" :edit="edit" :values="values" :value="values[field.field_name].val" :fieldTitle="fieldTitle" :orgField="orgField" ref="field" :needValue="needValue" />
    <BooleanField     v-else-if="orgField.internal_type === 'BooleanField'"   :csrf="csrf" :tabledata="tabledata" :field="field" :edit="edit" :values="values" :value="values[field.field_name].val" :fieldTitle="fieldTitle" :orgField="orgField" ref="field" :needValue="needValue" />
    <TextField        v-else-if="orgField.internal_type === 'TextField'"      :csrf="csrf" :tabledata="tabledata" :field="field" :edit="edit" :values="values" :value="values[field.field_name].val" :fieldTitle="fieldTitle" :orgField="orgField" ref="field" :needValue="needValue" />
    <CharField        v-else-if="orgField.internal_type === 'CharField'"      :csrf="csrf" :tabledata="tabledata" :field="field" :edit="edit" :values="values" :value="values[field.field_name].val" :fieldTitle="fieldTitle" :orgField="orgField" ref="field" :needValue="needValue" />
    <IntegerField     v-else-if="orgField.internal_type === 'IntegerField'"   :csrf="csrf" :tabledata="tabledata" :field="field" :edit="edit" :values="values" :value="values[field.field_name].val" :fieldTitle="fieldTitle" :orgField="orgField" ref="field" :needValue="needValue" />
    <FloatField       v-else-if="orgField.internal_type === 'FloatField'"     :csrf="csrf" :tabledata="tabledata" :field="field" :edit="edit" :values="values" :value="values[field.field_name].val" :fieldTitle="fieldTitle" :orgField="orgField" ref="field" :needValue="needValue" />
    <UnknowenField    v-else                                                  :csrf="csrf" :tabledata="tabledata" :field="field" :edit="edit" :values="values" :value="values[field.field_name].val" :fieldTitle="fieldTitle" :orgField="orgField" ref="field" :needValue="needValue" />
  </div>
</template>

<script>
import AllgemeineFunktionen from '@/functions/Allgemein'
const reqFieldComponent = require.context('./DBFormContentField/', false, /\.vue$/i)
const fieldComponents = {}
reqFieldComponent.keys().forEach(fileName => {
  fieldComponents[fileName.split('/').pop().replace(/\.\w+$/, '')] = reqFieldComponent(fileName).default || reqFieldComponent(fileName)
})

export default {
  name: 'DBFormContentField',
  props: ['tabledata', 'field', 'edit', 'values', 'csrf'],
  data () {
    return {
    }
  },
  mounted () {
    // console.log(this.tabledata.data)
    // console.log(this.values)
    // console.log(this.field)
    this.values[this.field.field_name].fieldVue = this.$refs.field
  },
  computed: {
    aWidth () {
      return this.field.width || 100
    },
    orgField () {
      return AllgemeineFunktionen.getFirstObjectOfValueInPropertyOfArray(this.tabledata.data.model.fields, 'field_name', this.field.field_name)
    },
    fieldTitle () {
      return this.field.verbose_name ? this.field.verbose_name : (this.orgField.verbose_name ? this.orgField.verbose_name : this.field.field_name)
    },
    needValue () {
      return !(this.orgField.null && this.orgField.blank)
    }
  },
  methods: {
  },
  components: {
    ...fieldComponents
  }
}
</script>

<style scoped>
.field {
  width: 100%;
  min-width: 300px;
  max-width: 100%;
}
</style>
