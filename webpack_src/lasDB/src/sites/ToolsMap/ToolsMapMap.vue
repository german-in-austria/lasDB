<template>
  <div class="tools-map-map fill-height white elevation-2">
    <l-map ref="map" class="lmap" :zoom.sync="zoom" :center.sync="center" v-if="center">
      <l-control-layers position="topright"></l-control-layers>
      <l-control position="bottomleft">
        <v-btn @click="setView(home, 6)" small fab class="ml-0 mb-3 mr-2"><v-icon>mdi-home</v-icon></v-btn>
        <v-btn @click="setView(latLng(mapData.locations.obj[mapData.data.selected].lat_new, mapData.locations.obj[mapData.data.selected].lon_new), 12)" small fab class="ml-0 mb-3 mr-2" :disabled="!(mapData.data.selected > 0 && mapData.locations.obj[mapData.data.selected].lat_new && mapData.locations.obj[mapData.data.selected].lon_new)"><v-icon>mdi-magnify-scan</v-icon></v-btn>
        <v-btn @click="showCross = !showCross" small fab :class="'ml-0 mb-3 mr-2' + (showCross ? ' blue' : '')" :dark="showCross"><v-icon>mdi-crosshairs</v-icon></v-btn>
        <v-card>
          <v-card-text class="px-2 py-1">
            <v-icon @click="getCoordinats" small>mdi-pencil</v-icon>
            {{ center.lat }},{{ center.lng }},{{ zoom }}
            <a :href="'https://osmaps.ordnancesurvey.co.uk/' + center.lat + ',' + center.lng + ',' + zoom" target="_blank" class="ml-2">OS Maps</a>
            <a :href="'https://www.google.de/maps/@' + center.lat + ',' + center.lng + ',' + zoom + 'z'" target="_blank" class="ml-2">Google Maps</a>
          </v-card-text>
        </v-card>
      </l-control>
      <l-tile-layer
        v-for="tileProvider in tileSets"
        :key="tileProvider.name"
        :name="tileProvider.name"
        :visible="tileProvider.visible"
        :url="tileProvider.url"
        :subdomains="tileProvider.subdomains"
        :attribution="tileProvider.attribution"
        layer-type="base"
      />
      <template v-if="!dotRefresh">
        <l-circle-marker
          :lat-lng="latLng(dot.lat_new, dot.lon_new)"
          :radius="mapData.options.map.dotSize"
          :stroke="mapData.data.selected === dot.id"
          :weight="4"
          :fillColor="dotColor(dot)"
          :fillOpacity="0.75"
          @click="mapData.data.selected = dot.id"
          v-for="(dot, dKey) in dots"
          :key="'lmcd' + dKey"
        >
          <l-tooltip v-if="mapData.options.map.showTooltip">
            <b>{{ dot.name }}</b> (id: {{ dot.id }})<br>
            <template v-if="dot.belongs_to">
              bt: {{ mapData.locations.obj[dot.belongs_to] ? mapData.locations.obj[dot.belongs_to].name : '' }} ({{ dot.belongs_to }})<br>
            </template>
            infs: {{ dot.informants.map(i => i.las_num).join(', ') }}
          </l-tooltip>
        </l-circle-marker>
      </template>
      <l-control-scale position="bottomright" :imperial="false" :metric="true"></l-control-scale>
    </l-map>
    <template v-if="showCross">
      <div class="cross cross-x blue"></div>
      <div class="cross cross-y blue"></div>
    </template>
  </div>
</template>

<script>
// https://vue2-leaflet.netlify.app/components/
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
import { LMap, LTileLayer, LControl, LControlLayers, LCircleMarker, LTooltip, LControlScale } from 'vue2-leaflet'

export default {
  name: 'ToolsMapMap',
  props: ['user', 'options', 'csrf', 'mapData'],
  data () {
    return {
      map: null,
      home: L.latLng(58.03718871323224, -4.514169463663858),
      center: null,
      zoom: 6,
      dotRefresh: false,
      showCross: false,
      tileSets: [
        {
          name: 'OpenStreetMap',
          visible: true,
          url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        },
        {
          name: 'Humanitarian Open Tiles',
          visible: false,
          url: 'http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
          attribution: 'Humanitarian Open Tiles'
        },
        // {
        //   name: 'NLS',
        //   visible: false,
        //   url: 'https://nls-{s}.tileserver.com/nls/{z}/{x}/{y}.jpg',
        //   attribution: '<a href="https://maps.nls.uk/projects/api/">National Library of Scotland Historic Maps</a>',
        //   subdomains: '0123'
        // },
        {
          name: 'Stamen.TonerBackground',
          visible: false,
          url: 'https://stamen-tiles-{s}.a.ssl.fastly.net/toner-background/{z}/{x}/{y}{r}.png',
          attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
          subdomains: 'abcd'
        },
        {
          name: 'Minimal Ländergrenzen (hell)',
          visible: false,
          url: 'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',
          attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ'
        },
        {
          name: 'Minimal Ländergrenzen (dunkel)',
          visible: false,
          url: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
          subdomains: 'abcd'
        },
        {
          name: 'Leer',
          visible: false,
          url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}',
          attribution: 'Tiles &copy; Esri &mdash; Source: Esri'
        }
      ]
    }
  },
  mounted () {
    this.center = this.home
    // console.log(this.mapData)
    // console.log('locations', this.locations)
    // console.log('dots', this.dots)
    // console.log('dotsInformants', this.dotsInformants)
    this.$nextTick(() => {
      this.map = this.$refs.map.mapObject
      this.mapData.map = this.$refs.map.mapObject
      this.mapData.mapVue = this
      console.log('mapObject', this.map)
    })
  },
  methods: {
    latLng: L.latLng,
    setView (latLon, zoom) {
      this.map.setView(latLon, zoom || this.zoom)
    },
    dotColor (aDot) {
      if (this.mapData.options.map.dotType === 'controlled') {
        return aDot.controlled ? 'green' : 'red'
      }
      if (this.mapData.options.map.dotType === 'informants') {
        if (aDot.informants.length > 0) {
          let aInfs = aDot.informants.filter(aI => aI.las_num && aI.las_num.length > 0)
          if (aInfs.length > 0) {
            let aCol = this.dotsInformants.obj[aInfs[0].las_num]
            if (aCol) {
              return aCol.color
            }
          }
        }
        return 'red'
      }
      return this.mapData.options.map.dotType
    },
    getCoordinats () {
      let aTxt = prompt('Enter coordinats or url.')
      if (aTxt) {
        let aMatch = aTxt.match(/([0-9.-]+,[0-9.-]+,[0-9]+)/g)
        if (aMatch && aMatch[0]) {
          let aCoords = aMatch[0].split(',')
          console.log('getCoordinats', aTxt, aMatch, aCoords)
          if (aCoords && aCoords.length === 3) {
            this.setView(this.latLng(aCoords[0], aCoords[1]), aCoords[2])
          } else {
            alert('Coordinats not found!')
          }
        } else {
          console.log('getCoordinats', aTxt, aMatch)
          alert('Coordinats not found!')
        }
      }
    }
  },
  computed: {
    locations () {
      return this.mapData.locations.list.filter(aT => aT.geodata || (aT.lat_new && aT.lon_new))
    },
    dots () {
      if (!this.mapData.options.map.dotType || this.mapData.options.map.dotType === 'None') {
        return []
      }
      let aDots = this.locations.filter(aT => {
        if (this.mapData.options.map.dotFilter > 0) {
          return aT.lat_new && aT.lon_new && aT.belongs_to === this.mapData.options.map.dotFilter
        } else {
          return aT.lat_new && aT.lon_new
        }
      })
      return aDots
    },
    dotsInformants () {
      let infList = { list: [], obj: {} }
      this.dots.forEach(aDot => {
        aDot.informants.forEach(aInf => {
          if (aInf && aInf.las_num && infList.list.indexOf(aInf.las_num) < 0) {
            infList.obj[aInf.las_num] = { color: 'red' }
            infList.list.push(aInf.las_num)
          }
        })
      })
      infList.list.sort()
      infList.list.sort((a, b) => {
        let aN = parseInt(a.replace(/[a-zA-Z]+/g, ''))
        let bN = parseInt(b.replace(/[a-zA-Z]+/g, ''))
        return aN < bN ? -1 : (aN > bN ? 1 : 0)
      })
      let aLen = infList.list.length
      infList.list.forEach(aInf => {
        let aIndex = infList.list.indexOf(aInf)
        if (aIndex > 0) {
          let aColor = parseInt(255 / aLen * aIndex)
          infList.obj[aInf].color = 'rgb(0,' + aColor + ',' + (255 - aColor) + ')'
        }
      })
      return infList
    }
  },
  watch: {
    'mapData.options.map.showTooltip': function (nVal) {
      this.dotRefresh = true
    },
    dotRefresh (nVal) {
      if (nVal) {
        this.$nextTick(() => { this.dotRefresh = false })
      }
    }
  },
  components: {
    LMap,
    LTileLayer,
    LControl,
    LControlLayers,
    LCircleMarker,
    LTooltip,
    LControlScale
  }
}
</script>

<style scoped>
.tools-map-map {
  position: relative;
}
.map-select {
  position: absolute;
  left: 16px;
  bottom: 16px;
  z-index: 10000;
}
.v-menu {
  z-index: 10000;
}
.lmap {
  width: 100%;
  height: 100%;
}
.cross {
  position: absolute;
  z-index: 1000;
  pointer-events: none;
}
.cross-x {
  top: 0;
  left: 50%;
  width: 2px;
  height: 100%;
  margin-left: -1px;
}
.cross-y {
  top: 50%;
  left: 0;
  width: 100%;
  height: 2px;
  margin-top: -1px;
}
</style>
