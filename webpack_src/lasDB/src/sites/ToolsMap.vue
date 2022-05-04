<template>
  <v-layout fill-height :class="mapData.options.view.horizontal ? 'horizontal-div' : ''">
    <v-flex :class="'xs12' + (mapData.options.view.horizontal ? ' md4' : ' md6')" px-2>
      <ToolsMapMap :mapData="mapData" :user="user" :options="options" :csrf="csrf" v-if="!refresh" />
    </v-flex>
    <v-flex :class="'xs12' + (mapData.options.view.horizontal ? ' md8' : ' md6')" px-2>
      <ToolsMapData :mapData="mapData" :user="user" :options="options" :csrf="csrf" />
    </v-flex>
    <v-dialog v-model="mapData.loading" persistent width="300">
      <v-card color="primary" dark>
        <v-card-text>
          Loading ... please stand by
          <v-progress-linear indeterminate color="white" class="mb-0" />
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-layout>
</template>

<script>
import ToolsMapMap from './ToolsMap/ToolsMapMap.vue'
import ToolsMapData from './ToolsMap/ToolsMapData.vue'

export default {
  name: 'ToolsMap',
  props: ['user', 'options', 'csrf'],
  data () {
    return {
      mapData: {
        map: null,
        mapVue: null,
        toolVue: null,
        locations: {
          list: [],
          obj: {},
          treeBase: {
            childs: [],
            unknownChilds: []
          }
        },
        locationTypes: {
          list: [],
          obj: {}
        },
        options: {
          map: {
            dotType: 'controlled',
            dotSize: 5,
            dotFilter: null,
            showTooltip: true
          },
          view: {
            horizontal: false,
            listshortinfo: false
          }
        },
        data: {
          selected: null
        },
        saving: false,
        loading: false
      },
      refresh: false
    }
  },
  mounted () {
    this.mapData.toolVue = this
  },
  methods: {
    saveData () {
      let aChangedTowns = this.mapData.locations.list.filter(aTown => aTown.changed)
      console.log('saveData', aChangedTowns, this.mapData.saving)
      if (!this.mapData.saving) {
        if (aChangedTowns.length < 1) {
          alert('Keine Änderungen!')
        } else if (confirm('Wirklich ' + aChangedTowns.length + ' Datensätze aktuallisieren?')) {
          this.mapData.saving = true
          this.$http
            .post('/tools/map/', { set: 'setLocations', locations: JSON.stringify(aChangedTowns) }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
            .then((response) => {
              console.log('setLocations', response.data)
              if (response.data.saved) {
                aChangedTowns.forEach(aTown => {
                  this.$delete(aTown, 'changed')
                })
              }
              console.log('mapData', this.mapData)
              this.mapData.saving = false
            })
            .catch((err) => {
              console.log(err)
              this.mapData.saving = false
            })
        }
      }
    }
  },
  watch: {
    'mapData.options.view.horizontal' () {
      this.refresh = true
    },
    refresh (nVal) {
      if (nVal) {
        this.$nextTick(() => { this.refresh = false })
      }
    }
  },
  components: {
    ToolsMapMap,
    ToolsMapData
  }
}
</script>

<style scoped>
.v-dialog__content.v-dialog__content--active {
  z-index: 9999!important;
}
</style>
