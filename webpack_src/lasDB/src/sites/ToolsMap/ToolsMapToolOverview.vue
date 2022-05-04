<template>
  <v-card flat class="px-3">
    <v-card-text>
      <div v-for="(counter, cKey) in counters" :key="'c' + cKey">
        <b :title="'Id: ' + counter.type.id">{{ counter.type.name }}:</b>
        <b>{{ counter.sum.toLocaleString() }}</b> locations,
        <b :title="counter.latLon.toLocaleString()">{{ (100 / counter.sum * counter.latLon).toLocaleString(undefined, {minimumFractionDigits: 1, maximumFractionDigits: 1}) }}%</b> with lat/lon,
        <b :title="counter.geodata.toLocaleString()">{{ (100 / counter.sum * counter.geodata).toLocaleString(undefined, {minimumFractionDigits: 1, maximumFractionDigits: 1}) }}%</b> with geodata and
        <b :title="counter.sum.toLocaleString()">{{ (100 / counter.sum * counter.controlled).toLocaleString(undefined, {minimumFractionDigits: 1, maximumFractionDigits: 1}) }}%</b> are controlled.
      </div>
      <div>
        <v-layout flex wrap class="hdiv-double mt-3">
          <div class="pr-3 w-50">
            <v-autocomplete
              label="Selected"
              v-model="mapData.data.selected"
              :items="searchList" item-text="searchText" item-value="data.id"
              clearable
            >
            </v-autocomplete>
          </div>
        </v-layout>
        <h3 class="mb-3">Map</h3>
        <v-layout flex wrap class="hdiv-double">
          <div class="pr-3 w-50">
            <v-select
              label="Dots"
              :items="['controlled', 'red', 'blue', 'green', 'informants', 'None']"
              v-model="mapData.options.map.dotType"
            ></v-select>
          </div>
          <div class="pr-3 w-50">
            <v-slider v-model="mapData.options.map.dotSize" min="2" max="15" label="Dot size" thumb-label></v-slider>
          </div>
          <div class="pr-3 w-50">
            <v-select
              label="Dot Filter"
              :items="[{ name: 'all', id: null }, ...mapData.locations.treeBase.childs.filter(l => l.type === 1 && l.childs && l.childs.length > 0)]" item-text="name" item-value="id"
              v-model="mapData.options.map.dotFilter"
            ></v-select>
          </div>
          <div class="pr-3 w-25">
            <v-checkbox v-model="mapData.options.map.showTooltip" label="show tooltips"></v-checkbox>
          </div>
        </v-layout>
        <h3 class="my-3">Basic</h3>
        <v-layout flex wrap class="hdiv-double">
          <div class="pr-3 w-25">
            <v-checkbox v-model="mapData.options.view.horizontal" label="horizontal division"></v-checkbox>
          </div>
          <div class="pr-3 w-25">
            <v-checkbox v-model="mapData.options.view.listshortinfo" label="less details in the list"></v-checkbox>
          </div>
        </v-layout>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'ToolsMapToolOverview',
  props: ['aObj', 'mapData'],
  data () {
    return {
    }
  },
  mounted () {
    console.log('ToolsMapToolOverview', this.counters)
  },
  watch: {
  },
  methods: {
  },
  computed: {
    searchList () {
      let sL = []
      this.mapData.locations.list.filter(aL => aL.type === 2).forEach(aL => {
        sL.push({ searchText: aL.name + ' (' + (aL.belongs_to && this.mapData.locations.obj[aL.belongs_to] ? this.mapData.locations.obj[aL.belongs_to].name + ', ' : '') + 'id: ' + aL.id + ')', data: aL })
      })
      return sL
    },
    counters () {
      let aCounters = []
      let aCountersObj = {}
      this.mapData.locations.list.forEach(aLoc => {
        if (aLoc.type) {
          if (!aCountersObj[aLoc.type]) {
            aCountersObj[aLoc.type] = { type: this.mapData.locationTypes.obj[aLoc.type], list: [] }
          }
          aCountersObj[aLoc.type].list.push(aLoc)
        } else {
          console.log('Error in aLoc!', aLoc)
        }
      })
      Object.keys(aCountersObj).forEach(aType => {
        aCountersObj[aType].sum = aCountersObj[aType].list.length
        aCountersObj[aType].latLon = aCountersObj[aType].list.filter(aT => aT.lat_new && aT.lon_new).length
        aCountersObj[aType].geodata = aCountersObj[aType].list.filter(aT => aT.geodata).length
        aCountersObj[aType].controlled = aCountersObj[aType].list.filter(aT => aT.controlled).length
        aCounters.push(aCountersObj[aType])
      })
      return aCounters
    }
  },
  components: {
  }
}
</script>

<style scoped>
</style>
