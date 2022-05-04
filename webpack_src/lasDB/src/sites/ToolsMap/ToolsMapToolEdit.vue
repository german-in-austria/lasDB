<template>
  <v-card flat class="cont px-3 hdiv-double">
    <v-card-text>
      <v-layout row wrap>
        <v-flex class="w-50" pr-3 pb-2>
          <v-autocomplete
            label="Selected"
            v-model="mapData.data.selected"
            :items="searchList" item-text="searchText" item-value="data.id"
            hide-details
            dense
            clearable
          >
          </v-autocomplete>
        </v-flex>
        <template v-if="aLocation">
          <v-flex class="w-25" pr-3 pb-2>
            <v-text-field
              label="id"
              v-model="aLocation.id"
              placeholder="empty"
              hide-details
              dense
              readonly
            ></v-text-field>
          </v-flex>
          <v-flex class="w-25" pr-3 pb-2>
            <v-switch @change="change" dense hide-details v-model="aLocation.controlled" label="Controlled" color="green"></v-switch>
          </v-flex>
          <v-flex xs12 md6 pr-3 pb-2>
            <v-text-field
              label="name"
              v-model="aLocation.name"
              @change="change"
              placeholder="empty"
              hide-details
              dense
            ></v-text-field>
          </v-flex>
          <v-flex class="w-50" pr-3 pb-2>
            <v-autocomplete
              label="belongs_to"
              v-model="aLocation.belongs_to"
              :items="belongsToList" item-text="searchText" item-value="data.id"
              @change="change"
              clearable
              hide-details
              dense
            >
            </v-autocomplete>
          </v-flex>
          <v-flex class="w-25" pr-3 pb-2>
            <v-text-field
              label="grid_org"
              v-model="aLocation.grid_org"
              @change="change"
              placeholder="empty"
              hide-details
              dense
            ></v-text-field>
          </v-flex>
          <v-flex class="w-25" pr-3 pb-2>
            <v-select
              label="Standard"
              :items="mapData.locationTypes.list" item-text="name" item-value="id"
              v-model="aLocation.type" @change="change"
              hide-details
              dense
            ></v-select>
          </v-flex>
          <v-flex class="w-25" pr-3 pb-2>
            <v-text-field
              type="number"
              step="1"
              label="osm_id"
              v-model="aLocation.osm_id"
              @change="change"
              placeholder="empty"
              hide-details
              dense
            ></v-text-field>
          </v-flex>
          <v-flex class="w-25" pr-3 pb-2>
            <v-text-field
              label="osm_type"
              v-model="aLocation.osm_type"
              @change="change"
              placeholder="empty"
              hide-details
              dense
            ></v-text-field>
          </v-flex>
          <v-flex class="w-50" pr-3 pb-2>
            <v-text-field
              type="number"
              step="0.01"
              label="lat_new"
              v-model="aLocation.lat_new"
              @input="changeFx"
              @change="change"
              placeholder="empty"
              prepend-icon="mdi-crosshairs"
              @click:prepend="setLocationByMap('new')"
              hide-details
              dense
            ></v-text-field>
          </v-flex>
          <v-flex class="w-50" pr-3 pb-2>
            <v-text-field
              type="number"
              step="0.01"
              label="lon_new"
              v-model="aLocation.lon_new"
              @input="changeFx"
              @change="change"
              placeholder="empty"
              hide-details
              dense
            ></v-text-field>
          </v-flex>
          <v-flex class="w-50" pr-3 pb-2>
            <v-text-field
              type="number"
              step="0.01"
              label="lat_imp"
              v-model="aLocation.lat_imp"
              @input="changeFx"
              @change="change"
              placeholder="empty"
              prepend-icon="mdi-crosshairs"
              @click:prepend="setLocationByMap('imp')"
              hide-details
              dense
            ></v-text-field>
          </v-flex>
          <v-flex class="w-50" pr-3 pb-2>
            <v-text-field
              type="number"
              step="0.01"
              label="lon_imp"
              v-model="aLocation.lon_imp"
              @input="changeFx"
              @change="change"
              placeholder="empty"
              hide-details
              dense
            ></v-text-field>
          </v-flex>
          <v-flex class="w-100" pr-3 pb-2>
            <v-text-field
              label="Nominatim search"
              v-model="search"
              prepend-icon="mdi-map-search"
              :loading="searching"
              hide-details
              dense
            >
              <template v-slot:append-outer>
                <v-icon :disabled="search.length < 4 || searching" @click="searchNominatim">mdi-magnify</v-icon>
              </template>
            </v-text-field>
          </v-flex>
          <v-flex class="w-100" pr-3 v-if="results.length > 0">
            <v-list two-line>
              <template v-for="(aResult, aKey) in results">
                <v-list-tile @click="centerToCoordinates(aResult.lat, aResult.lon)" :key="'sr-t' + aKey">
                  <v-list-tile-avatar>
                    <img :src="aResult.icon" style="image-rendering: pixelated;" v-if="aResult.icon">
                  </v-list-tile-avatar>
                  <v-list-tile-content>
                    <v-list-tile-title :title="aResult.display_name">{{ aResult.display_name }}</v-list-tile-title>
                    <v-list-tile-sub-title>class: {{ aResult.class }}, type: {{ aResult.type }}, osm_id: {{ aResult.osm_id }}, osm_type: {{ aResult.osm_type }}, lat: {{ aResult.lat }}, lon: {{ aResult.lon }}</v-list-tile-sub-title>
                  </v-list-tile-content>
                  <v-list-tile-action>
                    <div style="font-size:0.8rem;line-height:0.9rem;" class="mx-auto">set</div>
                    <v-btn @click="aLocation.lat_new = aResult.lat;aLocation.lon_new = aResult.lon; aLocation.osm_id = aResult.osm_id; aLocation.osm_type = aResult.osm_type; change();" class="sbtns my-1 mx-auto">new</v-btn>
                    <v-btn @click="aLocation.lat_imp = aResult.lat;aLocation.lon_imp = aResult.lon; change();" class="sbtns mx-auto">imp</v-btn>
                  </v-list-tile-action>
                </v-list-tile>
                <v-divider :key="'sr-d' + aKey" />
              </template>
            </v-list>
          </v-flex>
          <v-flex class="w-100" pr-3 pb-2>
            <v-text-field
              label="informants (las_num)"
              :value="aLocation.informants.map(i => i.las_num).join(', ')"
              placeholder="empty"
              hide-details
              dense
              readonly
            ></v-text-field>
          </v-flex>
          <v-flex class="w-100" pr-3 pb-2>
            <v-textarea
              label="comment"
              v-model="aLocation.comment"
              @change="change"
              placeholder="empty"
              :rows="1"
              hide-details
              dense
              auto-grow
            ></v-textarea>
          </v-flex>
        </template>
      </v-layout>
    </v-card-text>
  </v-card>
</template>

<script>
import _ from 'lodash'

export default {
  name: 'ToolsMapToolEdit',
  props: ['user', 'options', 'csrf', 'aObj', 'mapData'],
  data () {
    return {
      search: '',
      results: [],
      searching: false,
      aLocation: null
    }
  },
  mounted () {
    this.aLocation = this.mapData.data.selected ? _.cloneDeep(this.mapData.locations.obj[this.mapData.data.selected]) : null
    this.search = this.autoSearchText
  },
  methods: {
    centerToCoordinates (lat, lon) {
      console.log('centerToCoordinates', lat, lon, this.mapData.mapVue.latLng(lat, lon))
      this.mapData.mapVue.setView(this.mapData.mapVue.latLng(lat, lon))
    },
    setLocationByMap (t) {
      if (this.mapData.map) {
        console.log('setLocationByMap', t, this.mapData.map.getCenter())
        this.aLocation['lat_' + t] = this.mapData.map.getCenter().lat
        this.aLocation['lon_' + t] = this.mapData.map.getCenter().lng
        this.change()
      }
    },
    searchNominatim () {
      this.results = ''
      if (!this.searching && this.search.length > 3) {
        console.log('searchNominatim', this.search)
        this.searching = true
        this.$http
          .get('https://nominatim.openstreetmap.org/search/?format=json&limit=50&q=' + encodeURIComponent(this.search))
          .then((response) => {
            console.log('searchNominatim - Results:', response.body)
            if (response.body && response.body.length > 0) {
              this.results = response.body
            }
            this.searching = false
          })
          .catch((err) => {
            this.searching = false
            console.log(err)
          })
      }
    },
    changeFx () {
      ['lat_new', 'lon_new', 'lat_imp', 'lon_imp'].forEach(property => {
        this.$set(this.mapData.locations.obj[this.aLocation.id], property, this.aLocation[property] ? parseFloat(this.aLocation[property]) : this.aLocation[property])
      })
      this.debouncedUpdateData()
    },
    change () {
      this.$set(this.aLocation, 'changed', true)
      this.updateData()
    },
    debouncedUpdateData: _.debounce(function () { this.updateData() }, 200),
    updateData () {
      if (this.aLocation && this.aLocation.id && this.aLocation.changed) {
        Object.keys(this.aLocation).forEach(property => {
          let val = typeof this.aLocation[property] === 'string' ? this.aLocation[property].trim() : this.aLocation[property]
          if (val && ['osm_id'].indexOf(property) > -1) {
            val = parseInt(val)
          }
          if (val && ['lat_new', 'lon_new', 'lat_imp', 'lon_imp'].indexOf(property) > -1) {
            val = parseFloat(val)
          }
          this.$set(this.mapData.locations.obj[this.aLocation.id], property, val)
          this.$set(this.aLocation, property, val)
        })
      }
    }
  },
  computed: {
    searchList () {
      return this.mapData.locations.list.filter(aL => aL.type === 2 || aL.type === 1).map(aL => {
        return { searchText: aL.name + ' (' + (aL.belongs_to && this.mapData.locations.obj[aL.belongs_to] ? this.mapData.locations.obj[aL.belongs_to].name + ', ' : '') + 'id: ' + aL.id + ')', data: aL }
      })
    },
    belongsToList () {
      return this.mapData.locations.list.map(aL => {
        return { searchText: aL.name + ' (' + (aL.type ? this.mapData.locationTypes.obj[aL.type].name : 'Err: No type!') + ', ' + (aL.belongs_to && this.mapData.locations.obj[aL.belongs_to] ? this.mapData.locations.obj[aL.belongs_to].name + ', ' : '') + 'id: ' + aL.id + ')', data: aL }
      }).sort((a, b) => { return a.data.type < b.data.type ? -1 : (a.data.type > b.data.type ? 1 : 0) })
    },
    autoSearchText () {
      return this.aLocation ? 'schottland ' + (this.aLocation.belongs_to && this.mapData.locations.obj[this.aLocation.belongs_to] ? this.mapData.locations.obj[this.aLocation.belongs_to].name + ' ' : '') + this.aLocation.name : ''
    }
  },
  watch: {
    search (nVal) {
      if (nVal.length === 0) {
        this.results = []
      }
    },
    'mapData.data.selected' () {
      this.updateData()
      this.aLocation = this.mapData.data.selected ? _.cloneDeep(this.mapData.locations.obj[this.mapData.data.selected]) : null
      this.results = []
      this.search = this.autoSearchText
    }
  },
  components: {
  }
}
</script>

<style scoped>
.cont {
  max-height: 55vh;
  overflow-y: auto;
}
.horizontal-div .cont {
  max-height: calc(100vh - 160px);
}
.sbtns {
  min-width: 0;
  padding: 0 0.25rem;
  height: 18px;
  font-size: 0.8rem;
}
</style>
