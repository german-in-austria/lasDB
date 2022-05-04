<template>
  <div class="h-100">
    <DBForm table="lex_variantgroup_types" form="lex_variantgroup_types" :user="user" :options="options" :csrf="csrf" />
  </div>
</template>

<script>
import DBForm from '../components/DBForm.vue'

export default {
  name: 'EditVariantgroupTypes',
  props: ['user', 'options', 'csrf'],
  data () {
    return {
    }
  },
  components: {
    DBForm
  }
}
</script>

<style scoped>
</style>
