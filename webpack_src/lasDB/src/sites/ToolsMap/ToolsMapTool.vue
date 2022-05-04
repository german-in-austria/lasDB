<template>
  <div>
    <v-tabs v-model="tab" background-color="deep-purple accent-4" dark>
      <v-tabs-slider></v-tabs-slider>
      <v-tab href="#overview"><v-icon>mdi-eye</v-icon></v-tab>
      <v-tab href="#edit"><v-icon>mdi-pencil</v-icon></v-tab>
      <v-tab href="#search"><v-icon>mdi-map-search</v-icon></v-tab>
      <v-tab href="#off"><v-icon>mdi-eye-off</v-icon></v-tab>
      <v-btn @click="mapData.toolVue.saveData" icon class="ml-auto" :disabled="mapData.toolVue.saving || !changedTowns"><v-icon>mdi-cloud-upload</v-icon></v-btn>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item value="overview">
        <ToolsMapToolOverview :aObj="aObj" :mapData="mapData" />
      </v-tab-item>
      <v-tab-item value="edit">
        <ToolsMapToolEdit :aObj="aObj" :mapData="mapData" :user="user" :options="options" :csrf="csrf" />
      </v-tab-item>
      <v-tab-item value="search">
        <ToolsMapToolSearch :aObj="aObj" :mapData="mapData" :user="user" :options="options" :csrf="csrf" />
      </v-tab-item>
      <v-tab-item value="off"></v-tab-item>
    </v-tabs-items>
  </div>
</template>

<script>
import ToolsMapToolOverview from './ToolsMapToolOverview.vue'
import ToolsMapToolEdit from './ToolsMapToolEdit.vue'
import ToolsMapToolSearch from './ToolsMapToolSearch.vue'

export default {
  name: 'ToolsMapTool',
  props: ['user', 'options', 'csrf', 'aObj', 'mapData'],
  data () {
    return {
      tab: null
    }
  },
  mounted () {
  },
  watch: {
  },
  methods: {
  },
  computed: {
    changedTowns () {
      return this.mapData.locations.list.filter(aTown => aTown.changed).length > 0
    }
  },
  components: {
    ToolsMapToolOverview,
    ToolsMapToolEdit,
    ToolsMapToolSearch
  }
}
</script>

<style scoped>
</style>
