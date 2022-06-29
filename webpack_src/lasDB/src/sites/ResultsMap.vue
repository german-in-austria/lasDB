<template>
  <v-layout fill-height>
    <v-flex class="xs12 md8 px-2">
      <l-map ref="map" class="lmap" :zoom.sync="map.zoom" :center.sync="map.center" v-if="map.center">
        <l-control-layers position="topright"></l-control-layers>
        <l-control position="bottomleft">
          <v-btn @click="setView(map.home, 6)" small fab class="ml-0 mb-3 mr-2"><v-icon>mdi-home</v-icon></v-btn>
        </l-control>
        <l-control position="bottomright">
          <v-card class="legend" v-if="selectedMap && mapObj && !mapLoading && mapData">
            <v-card-text class="py-1 px-2">
              <h3 v-if="mapObj.legend_title" class="mb-1">{{ mapObj.legend_title }}</h3>
              <ul
                class="legend-list"
                :style="'columns:' + Math.ceil(mapData.vg.length / 35) + ';-webkit-columns:' + Math.ceil(mapData.vg.length / 35) + ';-moz-columns:' + Math.ceil(mapData.vg.length / 35) + ';'"
                v-if="selectedMap > 0"
              >
                <template v-for="(vg, aKey) in mapData.vg">
                  <li :key="aKey" :class="vg.variantgroup.variants.length < 1 ? 'no-variants' : ''" :title="'variants: ' + (vg.variantgroup.variants.length)">
                    <span class="leg-col-circle" :style="'background-color:' + vg.preset_color"/>
                    {{ vg.variantgroup.legendText || vg.variantgroup.name }}
                  </li>
                </template>
              </ul>
              <ul
                class="legend-list"
                :style="'columns:' + Math.ceil(mapData.v.length / 35) + ';-webkit-columns:' + Math.ceil(mapData.v.length / 35) + ';-moz-columns:' + Math.ceil(mapData.v.length / 35) + ';'"
                v-if="selectedMap === -1"
              >
                <template v-for="(v, aKey) in mapData.v">
                  <li :key="aKey" :class="v.length < 1 ? 'no-variants' : ''" :title="'datas: ' + (v.data.length)">
                    <span class="leg-col-circle" :style="'background-color:' + v.preset_color"/>
                    {{ v.variant }}
                  </li>
                </template>
              </ul>
            </v-card-text>
          </v-card>
        </l-control>
        <l-tile-layer
          v-for="tileProvider in map.tileSets"
          :key="tileProvider.name"
          :name="tileProvider.name"
          :visible="tileProvider.visible"
          :url="tileProvider.url"
          :subdomains="tileProvider.subdomains"
          :attribution="tileProvider.attribution"
          layer-type="base"
        />
        <template v-for="(point, dg) in points">
          <l-marker :lat-lng="point.p" v-if="map.show === 'icon'" :key="'m' + dg">
            <l-icon
              :icon-size="[map.radius * 2 / map.kmPerPixel, map.radius * 2 / map.kmPerPixel]"
              :icon-url="torte(24, 1, '#000', point.c, point.l, true)"
              shadowUrl="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
            />
            <l-popup>
              <h4 class="mb-1">{{ point.lName }}</h4>
              <ul class="legend-list">
                <li v-for="(l, aKey) in point.l" :key="aKey">
                  <span class="leg-col-circle" :style="'background-color:' + l.c"/>
                  {{ selectedMap > 0 ? mapData.vg.filter(v => v.id === l.id)[0].variantgroup.name : mapData.v.filter(v => v.id === l.id)[0].variant }} - {{ l.v }}
                </li>
              </ul>
            </l-popup>
          </l-marker>
          <l-circle :lat-lng="point.p" :radius="map.radius * 1000" :weight="2" :color="point.c" :fillColor="point.c" :key="'c' + dg"
            :fillOpacity="map.circleOpacity / 100"
            :stroke="map.circleStroke"
            v-if="map.show === 'circle'"
          >
            <l-popup>
              <h4 class="mb-1">{{ point.lName }}</h4>
              <ul class="legend-list">
                <li v-for="(l, aKey) in point.l" :key="aKey">
                  <span class="leg-col-circle" :style="'background-color:' + l.c"/>
                  {{ selectedMap > 0 ? mapData.vg.filter(v => v.id === l.id)[0].variantgroup.name : mapData.v.filter(v => v.id === l.id)[0].variant }} - {{ l.v }}
                </li>
              </ul>
            </l-popup>
          </l-circle>
        </template>
      </l-map>
    </v-flex>
    <v-flex class="xs12 md4 px-2 z-i-1000">
      <v-autocomplete
        v-model="selectedMap"
        :items="maps"
        item-text="name"
        item-value="id"
        label="Map"
        hide-details
        dense
        :loading="loading || mapLoading"
        v-if="!individual"
      />
      <template v-if="selectedMap === -1">
        <v-autocomplete
          v-model="selectedVariable"
          :items="variables.list"
          item-text="variable"
          item-value="id"
          label="Variables"
          hide-details
          dense
          :loading="loading || mapLoading"
          class="mt-2"
        />
        <template v-if="selectedVariable && variables.byId[selectedVariable]">
          <b v-if="variables.byId[selectedVariable].in_question" class="mt-2 fx-txt">{{ variables.byId[selectedVariable].in_question }}</b>
          <p v-if="variables.byId[selectedVariable].comment" class="mt-2 fx-txt">{{ variables.byId[selectedVariable].comment }}</p>
          <v-autocomplete
            v-model="selectedVariants"
            :items="variants.list"
            item-text="variant"
            item-value="id"
            label="Variants"
            hide-details
            dense
            multiple
            :loading="loading || mapLoading"
            @blur="loadVariantsMap"
            class="mt-2"
            v-if="variants.list"
          />
        </template>
      </template>
      <template v-if="selectedMap && mapObj && !mapLoading">
        <div class="mt-3">
          <h2 v-if="mapObj.title">{{ mapObj.title + (mapObj.public ? ' - Private' : ' - Public') }}</h2>
          <h2 v-else-if="!mapObj.public">Private</h2>
          <p v-if="mapObj.description" class="mt-2 fx-txt">{{ mapObj.description }}</p>
          <p v-if="mapObj.comment" class="mt-2 fx-txt">{{ mapObj.comment }}</p>
          <p class="mt-2" v-if="mapData">
            <b>Locations:</b> {{ Object.keys(mapData.locations).length }}<br>
            <b>Districts:</b> {{ Object.keys(mapData.districts).length }}<br>
          </p>
          <hr>
        </div>
        <template v-if="!mapLoading">
          <v-select v-model="map.markerSource" @change="map.show = map.markerSource === 'locations' ? 'circle' : map.show" :items="['districts', 'locations']" label="Marker Source" hide-details dense class="mt-2"></v-select>
          <v-select v-model="map.show" :items="['icon', 'circle']" label="Marker" hide-details dense class="mt-2"></v-select>
          <v-slider v-model="map.radius" min="1" max="50" label="Radius" hide-details dense thumb-label class="mt-3">
            <template v-slot:append>
              <v-text-field v-model="map.radius" class="mt-0 pt-0 fx-tf" hide-details single-line type="number" style="width: 60px"></v-text-field><span class="mt-2"> km</span>
            </template>
          </v-slider>
          <template v-if="map.show === 'circle'">
            <v-slider v-model="map.circleOpacity" min="10" max="100" label="Opacity" hide-details dense thumb-label class="mt-3">
              <template v-slot:append>
                <v-text-field v-model="map.circleOpacity" class="mt-0 pt-0 fx-tf" hide-details single-line type="number" style="width: 60px"></v-text-field><span class="mt-2"> %</span>
              </template>
            </v-slider>
            <v-checkbox v-model="map.circleStroke" class="mt-2" label="Stroke" hide-details></v-checkbox>
          </template>
          <div class="mt-2" v-if="selectedMap > 0 && maps && mapObj">
            <v-btn @click="selectedMap = maps[maps.indexOf(mapObj) - 1].id" :disabled="maps.indexOf(mapObj) < 1">prior map</v-btn>
            <v-btn @click="selectedMap = maps[maps.indexOf(mapObj) + 1].id" :disabled="maps.indexOf(mapObj) > maps.length - 2">next map</v-btn>
          </div>
        </template>
      </template>
      <v-alert type="info" v-else>
        Loading Map ... please stand by
      </v-alert>
    </v-flex>
    <v-dialog v-model="loading" persistent width="300">
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
// https://vue2-leaflet.netlify.app/components/
// https://leafletjs.com/reference-1.7.1.html
import _ from 'lodash'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
import { LMap, LTileLayer, LControl, LControlLayers, LCircleMarker, LTooltip, LControlScale, LIcon, LMarker, LCircle, LPopup } from 'vue2-leaflet'

export default {
  name: 'ResultsMap',
  props: ['user', 'options', 'csrf', 'query'],
  data () {
    return {
      loading: false,
      mapLoading: false,
      newQuery: true,
      reSetQuery: false,
      variantsQuery: false,
      selectedMap: null,
      mapsRaw: null,
      mapData: null,
      locations: {
        list: [],
        byId: {}
      },
      variables: {
        list: [],
        byId: {}
      },
      selectedVariable: null,
      variants: {
        list: [],
        byId: {}
      },
      selectedVariants: null,
      map: {
        map: null,
        home: L.latLng(58.03718871323224, -4.514169463663858),
        center: null,
        kmPerPixel: null,
        zoom: 6,
        markerSource: 'districts',
        show: 'icon',
        radius: 12,
        circleOpacity: 20,
        circleStroke: true,
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
          {
            name: 'NLS',
            visible: false,
            url: 'https://nls-{s}.tileserver.com/nls/{z}/{x}/{y}.jpg',
            attribution: '<a href="https://maps.nls.uk/projects/api/">National Library of Scotland Historic Maps</a>',
            subdomains: '0123'
          },
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
      },
      dev: (process.env.NODE_ENV === 'development')
    }
  },
  mounted () {
    this.selectedMap = this.individual ? -1 : null
    this.loadMaps()
    this.map.center = this.map.home
    this.$nextTick(() => {
      this.map.map = this.$refs.map.mapObject
      this.updateKmPerPixel()
      // console.log('mapObject', this.map.map)
    })
    this.getQuery()
  },
  methods: {
    getQuery () {
      if (this.query && this.newQuery && !(this.loading || this.mapLoading)) {
        console.log('getQuery', this.query)
        this.selectedMap = this.query.smid && (this.maps.filter(m => m.id === parseInt(this.query.smid)).length > 0) ? parseInt(this.query.smid) : null
        this.map.markerSource = this.query.mms || this.map.markerSource
        this.map.show = this.query.ms || this.map.show
        this.map.radius = this.query.mr || this.map.radius
        this.map.circleOpacity = this.query.mco ? parseInt(this.query.mco) : this.map.circleOpacity
        this.map.circleStroke = typeof this.query.mcs === 'boolean' ? this.query.mcs : this.map.circleStroke
        this.selectedVariable = this.query.svb > 0 ? parseInt(this.query.svb) : this.selectedVariable
        this.selectedVariants = this.query.svt && Array.isArray(this.query.svt) ? this.query.svt.map(w => parseInt(w)) : this.selectedVariants
        if (this.selectedVariants && this.selectedVariants.length > 0) {
          this.variantsQuery = true
        }
        this.newQuery = false
      }
    },
    setQuery () {
      if (!(this.loading || this.mapLoading)) {
        console.log('setQuery', this.selectedMap, this.selectedVariable, this.selectedVariants)
        this.$router.push({
          path: this.$route.path,
          query: {
            smid: this.selectedMap,
            mms: this.map.markerSource,
            ms: this.map.show,
            mr: this.map.radius,
            mco: this.map.circleOpacity,
            mcs: this.map.circleStroke,
            svb: this.selectedVariable,
            svt: this.selectedVariants
          }
        })
        this.reSetQuery = false
      } else {
        this.reSetQuery = true
      }
    },
    latLng: L.latLng,
    setView (latLon, zoom) {
      this.map.map.setView(latLon, zoom || this.zoom)
    },
    torte (size, border, borderColor, color, data, encoded) {
      let hSize = size * 0.5
      let ihSize = (size - border * 2) * 0.5
      let out = ''
      out += '<circle cx="' + hSize + '" cy="' + hSize + '" r="' + hSize + '" fill="' + borderColor + '" />'
      out += '<circle cx="' + hSize + '" cy="' + hSize + '" r="' + ihSize + '" fill="' + color + '" />'
      function describeArc (x, y, radius, startAngle, endAngle) {
        function polarToCartesian (centerX, centerY, radius, angleInDegrees) {
          var angleInRadians = (angleInDegrees - 90) * Math.PI / 180.0
          return {x: centerX + (radius * Math.cos(angleInRadians)), y: centerY + (radius * Math.sin(angleInRadians))}
        }
        var start = polarToCartesian(x, y, radius, endAngle)
        var end = polarToCartesian(x, y, radius, startAngle)
        var arcSweep = endAngle - startAngle <= 180 ? '0' : '1'
        var d = ['M', start.x, start.y, 'A', radius, radius, 0, arcSweep, 0, end.x, end.y, 'L', x, y, 'L', start.x, start.y].join(' ')
        return d
      }
      let max = data.reduce((a, b) => a + (b.v || 0), 0)
      let angMulti = 360 / max
      let lAng = 0
      data.forEach(el => {
        let nAng = lAng + el.v * angMulti
        // console.log(el.c)
        out += '<path d="' + describeArc(hSize, hSize, ihSize, lAng, nAng) + '" stroke-width="0" fill="' + (el.c || '#f00') + '" />'
        lAng = nAng
      })
      out = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1"  width="' + size + '" height="' + size + '" viewBox="0 0 ' + size + ' ' + size + '">' + out + '</svg>'
      return encoded ? 'data:image/svg+xml;base64,' + window.btoa(unescape(encodeURIComponent(out))) : out
    },
    updateKmPerPixel () {
      var centerLatLng = this.map.home // get map center
      var pointC = this.map.map.latLngToContainerPoint(centerLatLng) // convert to containerpoint (pixels)
      var pointX = [pointC.x + 1, pointC.y] // add one pixel to x
      // var pointY = [pointC.x, pointC.y + 1] // add one pixel to y
      var latLngC = this.map.map.containerPointToLatLng(pointC)
      var latLngX = this.map.map.containerPointToLatLng(pointX)
      // var latLngY = this.map.map.containerPointToLatLng(pointY)
      var distanceX = latLngC.distanceTo(latLngX) // calculate distance between c and x (latitude)
      // var distanceY = latLngC.distanceTo(latLngY) // calculate distance between c and y (longitude)
      // console.log(distanceX, distanceY)
      this.map.kmPerPixel = distanceX / 1000
    },
    loadMaps () {
      if (!this.loading) {
        this.loading = true
        this.$http
          .post('/maps/', {
            get: 'maps'
          }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
          .then((response) => {
            this.mapsRaw = null
            this.$nextTick(() => {
              console.log('loadMaps', response.data)
              this.mapsRaw = response.data.maps
              console.log(response.data.maps)
              this.locations = {
                list: [],
                byId: {}
              }
              this.locations.list = response.data.locations
              this.locations.list.forEach(l => {
                this.locations.byId[l.id] = l
              })
              this.variables = {
                list: [],
                byId: {}
              }
              this.variables.list = response.data.variables
              this.variables.list.forEach(v => {
                this.variables.byId[v.id] = v
              })
              // console.log('locations', this.locations)
              // if (!this.selectedMap && this.dev && this.maps && this.maps[0] && this.maps[0].id) {
              //   this.selectedMap = this.maps[1].id
              // }
              this.loading = false
              this.getQuery()
              if (this.reSetQuery) {
                this.setQuery()
              }
            })
          })
          .catch((err) => {
            console.log(err)
            this.loading = false
            this.getQuery()
            if (this.reSetQuery) {
              this.setQuery()
            }
          })
      }
    },
    loadMap () {
      if (!this.mapLoading && this.selectedMap > 0) {
        this.mapLoading = true
        this.$http
          .post('/maps/', {
            get: 'map',
            mapId: this.selectedMap
          }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
          .then((response) => {
            this.mapData = null
            this.$nextTick(() => {
              console.log('loadMap', response.data)
              // vg[0].variantgroup.variants[0].data[0].fDist
              let locations = {}
              let districts = {}
              if (response.data.vg) {
                response.data.vg.forEach(vg => {
                  if (vg.variantgroup.variants) {
                    vg.variantgroup.variants.forEach(v => {
                      if (v.data) {
                        v.data.forEach(d => {
                          if (!locations[d.fDist]) {
                            locations[d.fDist] = {
                              id: d.fDist,
                              vg: {}
                            }
                            if (!locations[d.fDist].vg[vg.id]) {
                              locations[d.fDist].vg[vg.id] = {
                                id: vg.id,
                                color: vg.preset_color,
                                count: 0
                              }
                            }
                            locations[d.fDist].vg[vg.id].count += 1
                          }
                          if (this.locations.byId[d.fDist]) {
                            let aLoc = this.locations.byId[d.fDist]
                            let aDistr = 0
                            if (aLoc.belongs_to && this.locations.byId[aLoc.belongs_to]) {
                              aDistr = this.locations.byId[aLoc.belongs_to].id
                            }
                            if (!districts[aDistr]) {
                              districts[aDistr] = {
                                id: aDistr,
                                vg: {},
                                locations: []
                              }
                            }
                            if (!districts[aDistr].vg[vg.id]) {
                              districts[aDistr].vg[vg.id] = {
                                id: vg.id,
                                color: vg.preset_color,
                                count: 0
                              }
                            }
                            districts[aDistr].vg[vg.id].count += 1
                            if (districts[aDistr].locations.indexOf(d.fDist) < 0) {
                              districts[aDistr].locations.push(d.fDist)
                            }
                          } else {
                            alert('Error: location id ' + d.fDist + ' did not exist!')
                          }
                        })
                      }
                    })
                  }
                })
              }
              this.mapData = {
                vg: response.data.vg,
                locations: locations,
                districts: districts
              }
              console.log('mapData', this.mapData)
              this.mapLoading = false
              this.getQuery()
              if (this.reSetQuery) {
                this.setQuery()
              }
            })
          })
          .catch((err) => {
            console.log(err)
            this.mapLoading = false
            this.getQuery()
            if (this.reSetQuery) {
              this.setQuery()
            }
          })
      }
    },
    loadVariants () {
      if (!this.mapLoading && this.selectedVariable > 0) {
        this.mapLoading = true
        if (!this.variantsQuery) {
          this.selectedVariants = null
        }
        this.$http
          .post('/maps/', {
            get: 'variants',
            variableId: this.selectedVariable
          }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
          .then((response) => {
            this.variants = {
              list: [],
              byId: {}
            }
            this.$nextTick(() => {
              console.log('loadVariants', response.data)
              this.variants.list = response.data.variants
              this.variants.list.forEach(v => {
                this.variants.byId[v.id] = v
              })
              this.mapLoading = false
              this.getQuery()
              if (this.reSetQuery) {
                this.setQuery()
              }
              if (this.variantsQuery) {
                this.loadVariantsMap()
                this.variantsQuery = false
              }
              this.loadVariantsMap()
            })
          })
          .catch((err) => {
            console.log(err)
            this.mapLoading = false
            this.getQuery()
            if (this.reSetQuery) {
              this.setQuery()
            }
            if (this.variantsQuery) {
              this.loadVariantsMap()
              this.variantsQuery = false
            }
          })
      }
    },
    random (s) {
      var x = Math.sin(s) * 10000
      return x - Math.floor(x)
    },
    loadVariantsMap: _.debounce(function () {
      if (!this.mapLoading && this.selectedVariable > 0 && this.selectedVariants && this.selectedVariants.length > 0) {
        this.mapLoading = true
        this.$http
          .post('/maps/', {
            get: 'variantsMap',
            variableId: this.selectedVariable,
            variantIds: this.selectedVariants
          }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
          .then((response) => {
            this.$nextTick(() => {
              console.log('loadVariantsMap', response.data)
              let locations = {}
              let districts = {}
              if (response.data.variants) {
                response.data.variants.forEach(v => {
                  let rCol = Math.floor(this.random(v.id) * 16777215).toString(16)
                  while (rCol.length < 6) {
                    rCol = '0' + rCol
                  }
                  v.preset_color = '#' + rCol
                  if (v.data) {
                    v.data.forEach(d => {
                      if (!locations[d.fDist]) {
                        locations[d.fDist] = {
                          id: d.fDist,
                          v: {}
                        }
                        if (!locations[d.fDist].v[v.id]) {
                          locations[d.fDist].v[v.id] = {
                            id: v.id,
                            color: v.preset_color,
                            count: 0
                          }
                        }
                        locations[d.fDist].v[v.id].count += 1
                      }
                      if (this.locations.byId[d.fDist]) {
                        let aLoc = this.locations.byId[d.fDist]
                        let aDistr = 0
                        if (aLoc.belongs_to && this.locations.byId[aLoc.belongs_to]) {
                          aDistr = this.locations.byId[aLoc.belongs_to].id
                        }
                        if (!districts[aDistr]) {
                          districts[aDistr] = {
                            id: aDistr,
                            v: {},
                            locations: []
                          }
                        }
                        if (!districts[aDistr].v[v.id]) {
                          districts[aDistr].v[v.id] = {
                            id: v.id,
                            color: v.preset_color,
                            count: 0
                          }
                        }
                        districts[aDistr].v[v.id].count += 1
                        if (districts[aDistr].locations.indexOf(d.fDist) < 0) {
                          districts[aDistr].locations.push(d.fDist)
                        }
                      } else {
                        alert('Error: location id ' + d.fDist + ' did not exist!')
                      }
                    })
                  }
                })
              }
              this.mapData = {
                v: response.data.variants,
                locations: locations,
                districts: districts
              }
              console.log('mapData', this.mapData)
              this.mapLoading = false
              this.getQuery()
              if (this.reSetQuery) {
                this.setQuery()
              }
            })
          })
          .catch((err) => {
            console.log(err)
            this.mapLoading = false
            this.getQuery()
            if (this.reSetQuery) {
              this.setQuery()
            }
          })
      }
    }, 250)
  },
  computed: {
    maps () {
      if (this.individual) {
        return [
          {
            comment: null,
            description: null,
            id: -1,
            legend_title: null,
            name: 'individual variables',
            title: null,
            public: true
          }
        ]
      } else {
        return this.mapsRaw
      }
    },
    individual () {
      return this.$route.name === 'ResultsExplore'
    },
    points () {
      let aPoints = []
      if (this.mapData && (this.selectedMap < 0 || this.selectedMap > 0)) {
        let aLocations = this.mapData[this.map.markerSource]
        if (aLocations) {
          var locWOcoords = 0
          Object.keys(aLocations).forEach(locId => {
            let aDistr = aLocations[locId]
            let aLoc = this.locations.byId[locId]
            // console.log(aLoc, aDistr)
            let p = [60.5, -4.5]
            if (aLoc) {
              p = [aLoc.lat_new || 60.5, aLoc.lon_new || -4.5]
              if (!aLoc.lat_new || !aLoc.lon_new) {
                let cLocs = this.locations.list.filter(fL => fL.belongs_to === parseInt(locId) && fL.lat_new && fL.lon_new)
                if (cLocs.length > 0) {
                  let aLat = 0
                  let aLon = 0
                  cLocs.forEach(cL => {
                    aLat += cL.lat_new
                    aLon += cL.lon_new
                  })
                  // console.log(aLat, aLon)
                  p = [aLat / cLocs.length, aLon / cLocs.length]
                } else {
                  p = [60, -5 + 0.5 * locWOcoords]
                  locWOcoords += 1
                }
              }
            } else {
              p = [60, -5 + 0.5 * locWOcoords]
              locWOcoords += 1
            }
            let l = []
            let c = '#f0f'
            let mV = 0
            let vType = this.selectedMap > 0 ? 'vg' : 'v'
            Object.keys(aDistr[vType]).forEach(vId => {
              let aVg = aDistr[vType][vId]
              // console.log(aVg)
              l.push({
                v: aVg.count,
                c: aVg.color,
                id: aVg.id
              })
              if (aVg.count > mV) {
                c = aVg.color
                mV = aVg.count
              }
            })
            l.sort((a, b) => a.v - b.v)
            aPoints.push({
              lId: aLoc ? aLoc.id : locId,
              lName: aLoc ? aLoc.name : 'no belongs_to :-(',
              p: p,
              c: c,
              l: l
            })
          })
        }
      }
      // console.log(aPoints)
      return aPoints
    },
    mapObj () {
      if (this.selectedMap && this.maps) {
        let sMap = this.maps.filter(m => m.id === this.selectedMap)
        return sMap && sMap[0] ? sMap[0] : null
      } else {
        return null
      }
    }
  },
  watch: {
    individual () {
      if (this.individual) {
        this.selectedMap = -1
      } else {
        this.selectedMap = null
        this.selectedVariable = null
        this.selectedVariants = null
      }
      this.setQuery()
    },
    'map.zoom' () {
      this.updateKmPerPixel()
    },
    selectedMap () {
      if (this.selectedMap) {
        this.mapData = null
        this.loadMap()
      }
      this.setQuery()
    },
    selectedVariable () {
      if (this.selectedVariable) {
        this.mapData = null
        this.loadVariants()
      }
      this.setQuery()
    },
    'map.markerSource' () {
      this.setQuery()
    },
    'map.show' () {
      this.setQuery()
    },
    'map.radius' () {
      this.setQuery()
    },
    'map.circleOpacity' () {
      this.setQuery()
    },
    'map.circleStroke' () {
      this.setQuery()
    },
    selectedVariants () {
      this.setQuery()
    },
    query () {
      this.newQuery = true
      this.getQuery()
    }
  },
  components: {
    LMap,
    LTileLayer,
    LControl,
    LControlLayers,
    LCircleMarker,
    LTooltip,
    LControlScale,
    LIcon,
    LMarker,
    LCircle,
    LPopup
  }
}
</script>

<style scoped>
.z-i-1000 {
  z-index: 1000;
}
.v-dialog__content.v-dialog__content--active {
  z-index: 9999!important;
}
.v-menu {
  z-index: 10000;
}
.lmap {
  width: 100%;
  height: 100%;
}
.legend {
  font-size: 1.1rem;
  background-color: rgba(255,255,255,0.9);
}
.legend-list {
  list-style: none;
  padding: 0;
}
.legend-list > li {
  padding-right: 0.25rem;
  white-space: nowrap;
}
.legend-list > li.no-variants {
  text-decoration: line-through;
  opacity: 0.33;
}
.leg-col-circle {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  background-color: #999;
  margin-right: 0.25rem;
  border-radius: 100%;
  position: relative;
  top: 0.15rem;
}
.fx-tf >>> input {
  padding: 1px 0;
}
.fx-txt {
  display: block;
  max-height: 9rem;
  max-height: 25vh;
  overflow-y: auto;
}
</style>
