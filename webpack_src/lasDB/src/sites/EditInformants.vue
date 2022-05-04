<template>
  <div class="h-100">
    <DBForm table="informant" form="informant" :user="user" :options="options" :csrf="csrf" />
  </div>
</template>

<script>
import DBForm from '../components/DBForm.vue'

export default {
  name: 'EditInformants',
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
