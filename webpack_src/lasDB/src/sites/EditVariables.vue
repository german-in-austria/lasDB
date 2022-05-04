<template>
  <div class="h-100">
    <DBForm table="lex_variable" form="lex_variable" :user="user" :options="options" :csrf="csrf" />
  </div>
</template>

<script>
import DBForm from '../components/DBForm.vue'

export default {
  name: 'EditVariables',
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
