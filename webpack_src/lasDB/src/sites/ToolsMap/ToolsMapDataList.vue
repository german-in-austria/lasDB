<template>
  <div>
    <div class="location" v-if="aObj.id">
      <button @click="toggleLocationOpen" :class="'location-btn layout' + (locationOpen ? ' open' : '') + (mapData.data.selected === aObj.id ? ' selected' : '')">
        <div>{{ aObj.name }}
          <i v-if="aObj.childs || aObj.unknownChilds">({{ (aObj.childs ? aObj.childs.filter(aT => aT.controlled).length : 0) + (aObj.unknownChilds ? aObj.unknownChilds.filter(aT => aT.controlled).length : 0) }} /
            {{ (aObj.childs ? aObj.childs.filter(aT => aT.geodata || (aT.lat_new && aT.lon_new)).length : 0) + (aObj.unknownChilds ? aObj.unknownChilds.filter(aT => aT.geodata || (aT.lat_new && aT.lon_new)).length : 0) }} /
            {{ (aObj.childs ? aObj.childs.length : 0) + (aObj.unknownChilds ? aObj.unknownChilds.length : 0) }})</i>
        </div>
        <v-spacer />
        <div class="mr-3" v-if="aObj.informants && aObj.informants.length > 0">[{{ aObj.informants.map(i => i.las_num).join(', ') }}]</div>
        <v-icon
          :title="'Type: ' + mapData.locationTypes.obj[aObj.type].name"
          :color="aObj.controlled ? 'green darken-1' : (aObj.geodata || (aObj.lat_new && aObj.lon_new) ? 'blue darken-1' : '')"
          v-if="aObj.type && mapData.locationTypes.obj[aObj.type]"
        >
          {{ typesIcons[aObj.type] ? typesIcons[aObj.type] : 'mdi-crosshairs-question' }}
        </v-icon>
        <v-icon title="Type: Not set or wrong!" v-else>mdi-crosshairs-question</v-icon>
      </button>
      <div class="location-open" v-if="locationOpen">
        <v-layout row wrap class="location-info mx-2 mt-2">
          <v-flex xs12 md3 v-if="!mapData.options.view.listshortinfo"><b>id:</b> {{ aObj.id }}</v-flex>
          <v-flex :class="'xs12' + (mapData.options.view.listshortinfo ? 'md6' : ' md3')"><b>grid_org:</b> {{ aObj.grid_org }}</v-flex>
          <v-flex xs12 md3><b>type:</b> {{ aObj.type && mapData.locationTypes.obj[aObj.type] ? mapData.locationTypes.obj[aObj.type].name + ' (' + aObj.type + ')' : aObj.type }}</v-flex>
          <v-flex xs12 md3><b>controlled:</b> {{ aObj.controlled }}</v-flex>
          <v-flex xs12 md6 v-if="!mapData.options.view.listshortinfo"><b>osm_id:</b> {{ aObj.osm_id }}</v-flex>
          <v-flex xs12 md6 v-if="!mapData.options.view.listshortinfo"><b>osm_type:</b> {{ aObj.osm_type }}</v-flex>
          <v-flex xs12 md6><b>lat_new:</b> {{ aObj.lat_new }}</v-flex>
          <v-flex xs12 md6><b>lon_new:</b> {{ aObj.lon_new }}</v-flex>
          <v-flex xs12 md6 v-if="!mapData.options.view.listshortinfo"><b>lat_imp:</b> {{ aObj.lat_imp }}</v-flex>
          <v-flex xs12 md6 v-if="!mapData.options.view.listshortinfo"><b>lon_imp:</b> {{ aObj.lon_imp }}</v-flex>
          <v-flex xs12>
            <b>comment:</b><br>
            <div class="location-comment" v-if="aObj.comment">{{ aObj.comment.trim() }}</div>
          </v-flex>
          <v-flex xs12 md6 v-if="!mapData.options.view.listshortinfo"><b>informants (las_num):</b> {{ aObj.informants.map(i => i.las_num).join(', ') }}</v-flex>

        </v-layout>
        <div v-if="aObj.childs && aObj.childs.length > 0">
          <button @click="childOpen = !childOpen" :class="'childs-btn layout' + (childOpen ? ' open' : '')">
            <div><b>Childs</b> ({{ aObj.childs.filter(aT => aT.controlled).length }} / {{ aObj.childs.filter(aT => aT.geodata || (aT.lat_new && aT.lon_new)).length }} / {{ aObj.childs.length }})</div>
            <v-spacer />
            <v-icon>{{ childOpen ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
          </button>
          <div class="childs-open" v-if="childOpen">
            <div v-for="aChild in aObj.childs" :key="'mc-' + aChild.id">
              <ToolsMapDataList :aObj="aChild" :mapData="mapData" @scrollTo="scrollTo" />
            </div>
          </div>
        </div>
        <div v-if="aObj.unknownChilds && aObj.unknownChilds.length > 0">
          <button @click="unknownOpen = !unknownOpen" :class="'unknown-childs-btn layout' + (unknownOpen ? ' open' : '')">
            <div><b>Unknown</b> ({{ aObj.unknownChilds.filter(aT => aT.controlled).length }} / {{ aObj.unknownChilds.filter(aT => aT.geodata || (aT.lat_new && aT.lon_new)).length }} / {{ aObj.unknownChilds.length }})</div>
            <v-spacer />
            <v-icon>{{ unknownOpen ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
          </button>
          <div class="unknown-childs-open" v-if="unknownOpen">
            <div v-for="aChild in aObj.unknownChilds" :key="'muc-' + aChild.id">
              <ToolsMapDataList :aObj="aChild" :mapData="mapData" @scrollTo="scrollTo" />
            </div>
          </div>
        </div>
      </div>
    </div>
    <div style="margin-top: -1px;" v-else>
      <ToolsMapDataList :aObj="aChild" :mapData="mapData" v-for="aChild in aObj.childs" :key="'mc-' + aChild.id" @scrollTo="scrollTo" />
      <div v-if="aObj.unknownChilds && aObj.unknownChilds.length > 0">
        <button @click="unknownOpen = !unknownOpen" :class="'unknown-childs-btn layout' + (unknownOpen ? ' open' : '')">
          <div><b>Unknown</b> ({{ aObj.unknownChilds.filter(aT => aT.controlled).length }} / {{ aObj.unknownChilds.filter(aT => aT.geodata || (aT.lat_new && aT.lon_new)).length }} / {{ aObj.unknownChilds.length }})</div>
          <v-spacer />
          <v-icon>{{ unknownOpen ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
        </button>
        <div class="unknown-childs-open" v-if="unknownOpen">
          <div v-for="aChild in aObj.unknownChilds" :key="'muc-' + aChild.id">
            <ToolsMapDataList :aObj="aChild" :mapData="mapData" @scrollTo="scrollTo" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ToolsMapDataList',
  props: ['aObj', 'mapData'],
  data () {
    return {
      locationOpen: false,
      childOpen: false,
      unknownOpen: false,
      typesIcons: {
        1: 'mdi-map',
        2: 'mdi-city',
        3: 'mdi-help-circle'
      }
    }
  },
  mounted () {
    this.checkChildrenSelected()
  },
  methods: {
    toggleLocationOpen () {
      if (!this.locationOpen) {
        this.mapData.data.selected = this.aObj.id
      }
      this.locationOpen = !this.locationOpen
    },
    openParent (type) {
      this.locationOpen = true
      if (type === 'childs') {
        this.childOpen = true
      }
      if (type === 'unknown') {
        this.unknownOpen = true
      }
    },
    checkChildrenSelected () {
      if (this.mapData.data.selected > 0) {
        if (this.aObj.childs && !this.childOpen && !this.locationOpen) {
          this.aObj.childs.map(cObj => {
            if (cObj.id === this.mapData.data.selected) {
              this.locationOpen = true
              this.childOpen = true
              return true
            }
          })
        }
        if (this.aObj.unknownChilds && !this.unknownOpen && !this.locationOpen) {
          this.aObj.unknownChilds.map(cObj => {
            if (cObj.id === this.mapData.data.selected) {
              this.locationOpen = true
              this.unknownOpen = true
              return true
            }
          })
        }
      }
      if (this.aObj.id === this.mapData.data.selected) {
        this.locationOpen = true
        this.$nextTick(() => {
          this.$emit('scrollTo', this.$el.offsetTop)
        })
      }
    },
    scrollTo (pos) {
      this.$emit('scrollTo', pos)
    }
  },
  computed: {
  },
  watch: {
    'mapData.data.selected' (nVal) {
      this.checkChildrenSelected()
    }
  },
  components: {
  }
}
</script>

<style scoped>
.location-info {
  font-size: 1.1rem;
}
.location-btn, .unknown-childs-btn, .childs-btn {
  width: 100%;
  text-align: left;
  padding: 0.5rem;
  border-top: 1px solid #ddd;
  font-size: 1.2rem;
}
.location-btn.selected, .unknown-childs-btn.selected, .childs-btn.selected {
  background: #88b5dc!important;
}
.location-btn:hover, .unknown-childs-btn:hover, .childs-btn:hover, .location-btn:focus, .unknown-childs-btn:focus, .childs-btn:focus {
  background: #eee;
}
.location > div > div > .unknown-childs-btn, .location > div > div > .childs-btn {
  border-top: none;
}
.childs-open, .unknown-childs-open {
  margin-left: 2rem;
  border-left: 1px solid #999;
}
.location-open {
  margin-left: 1rem;
}
.location-comment {
  display: block;
  white-space: pre-line;
  padding: 0.5rem 1rem;
  background: #f8f8f8;
}
</style>
