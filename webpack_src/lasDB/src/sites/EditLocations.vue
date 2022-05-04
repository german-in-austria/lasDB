<template>
  <div class="h-100">
    <DBForm table="location" form="location" :user="user" :options="options" :csrf="csrf" />
  </div>
</template>

<script>
import DBForm from '../components/DBForm.vue'

export default {
  name: 'EditLocations',
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
