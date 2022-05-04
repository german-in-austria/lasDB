<template>
  <v-layout :class="'tools-map-data white elevation-2 fill-height' + (mapData.options.view.horizontal ? '' : ' column')" ref="toolsMapData" :style="{ height: height ? height + 'px' : null }">
    <v-flex :class="mapData.options.view.horizontal ? ' xs12 md6' : 'shrink'">
      <ToolsMapTool :aObj="mapData.locations.treeBase" :mapData="mapData" :user="user" :options="options" :csrf="csrf" v-if="!this.mapData.loading && ready" />
    </v-flex>
    <v-flex :class="'tools-map-data-list' + (mapData.options.view.horizontal ? ' xs12 md6' : ' grow')">
      <ToolsMapDataList :aObj="mapData.locations.treeBase" :mapData="mapData" v-if="!this.mapData.loading && ready" @scrollTo="scrollTo" ref="tmscroll" />
    </v-flex>
  </v-layout>
</template>

<script>
import ToolsMapDataList from './ToolsMapDataList.vue'
import ToolsMapTool from './ToolsMapTool.vue'

export default {
  name: 'ToolsMapData',
  props: ['user', 'options', 'csrf', 'mapData'],
  data () {
    return {
      height: null,
      ready: false
    }
  },
  mounted () {
    this.$nextTick(() => {
      this.height = this.$refs.toolsMapData.clientHeight
    })
    this.getLocations()
  },
  watch: {
  },
  methods: {
    edit (a) {
      console.log('edit', a)
    },
    getLocations () {
      this.mapData.loading = true
      this.$http
        .post('/tools/map/', { get: 'getLocations' }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
        .then((response) => {
          console.log('getLocations', response.data)
          this.mapData.locationTypes.list = response.data.types
          this.mapData.locationTypes.obj = {}
          this.mapData.locationTypes.list.forEach(locType => {
            this.mapData.locationTypes.obj[locType.id] = locType
          })
          this.mapData.locations.list = response.data.locations
          this.mapData.locations.obj = {}
          this.mapData.locations.list.forEach(location => {
            this.mapData.locations.obj[location.id] = location
          })
          this.mapData.locations.treeBase = { childs: [], unknownChilds: [] }
          let aObj = {}
          this.mapData.locations.list.forEach(location => {
            aObj = this.mapData.locations.treeBase
            if (location.belongs_to > 0) {
              aObj = this.mapData.locations.obj[location.belongs_to]
            }
            if (location.type === 3) {
              if (!aObj.unknownChilds) {
                aObj.unknownChilds = []
              }
              aObj = aObj.unknownChilds
            } else {
              if (!aObj.childs) {
                aObj.childs = []
              }
              aObj = aObj.childs
            }
            aObj.push(location)
          })
          this.mapData.loading = false
          this.ready = true
          console.log('mapData', this.mapData)
        })
        .catch((err) => {
          console.log(err)
          this.mapData.loading = false
        })
    },
    scrollTo (pos) {
      // console.log('scrollTo', pos, this.$refs.tmscroll)
      this.$refs.tmscroll.$el.scrollTo(0, (pos - 100 > 0) ? pos - 100 : 0)
    }
  },
  computed: {
    locationTree () {
      let lTree = []
      return lTree
    }
  },
  components: {
    ToolsMapDataList,
    ToolsMapTool
  }
}
</script>

<style scoped>
  .tools-map-data-list {
    position: relative;
    border-top: 1px solid #ddd;
  }
  .horizontal-div .tools-map-data-list {
    border-top: 0;
    border-left: 1px solid #ddd;
  }
  .tools-map-data-list > div {
    overflow: auto;
    position: absolute;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;
  }
</style>
