<template>
  <v-card flat class="px-3">
    <v-card-text>
      <div>
        All Towns without lat/lon: {{ towns && towns.length ? towns.length.toLocaleString() : '' }}
        <v-btn @click="searchNominatim" small v-if="towns && towns.length > 0 && !searching">Search by Nominatim</v-btn>
        <v-btn @click="searching = false" small v-if="towns && towns.length > 0 && searching">Stop Searching</v-btn>
        <v-btn @click="refreshTowns" small icon v-if="towns && towns.length > 0 && !searching"><v-icon>mdi-refresh</v-icon></v-btn>
        <v-btn @click="clearAllLatLon" small v-if="this.user.name === 'hcb'">Clear all Lat/Lon</v-btn>
        <v-layout row wrap>
          <v-flex xs12 md4 pr-3>
            <v-text-field
              label="country"
              v-model="country"
              hide-details
              dense
            ></v-text-field>
          </v-flex>
          <v-flex xs12 md4 pr-3>
            <v-checkbox v-model="sBelongsTo" dense label="belongs_to" v-if="towns && towns.length > 0" :disabled="searching" />
          </v-flex>
        </v-layout>
      </div>
      <div v-if="searching || sNum > 0">
        Searching: {{ sNum.toLocaleString() }} / {{ towns.length.toLocaleString() }}
      </div>
      <div class="results" v-if="results.length > 0">
        <ul>
          <li v-for="(result, rKey) in results" :key="'r' + rKey">{{ result }}</li>
        </ul>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'ToolsMapToolSearch',
  props: ['user', 'options', 'csrf', 'aObj', 'mapData'],
  data () {
    return {
      tab: null,
      country: 'schottland',
      towns: [],
      results: [],
      searching: false,
      sNum: 0,
      sBelongsTo: true,
      saving: false
    }
  },
  mounted () {
    this.refreshTowns()
  },
  watch: {
  },
  methods: {
    clearAllLatLon () {
      if (this.user.name === 'hcb' && prompt('Wirklich alle Koordinaten löschen?!?') === 'Ja das will ich!') {
        this.mapData.locations.list.forEach((aObj) => {
          this.$set(aObj, 'lat_new', null)
          this.$set(aObj, 'lon_new', null)
          this.$set(aObj, 'osm_id', null)
          this.$set(aObj, 'osm_type', null)
          this.$set(aObj, 'changed', true)
        })
      }
    },
    refreshTowns () {
      this.sNum = 0
      this.towns = this.mapData.locations.list.filter(aTown => aTown.type === 2 && !aTown.lat_new)
    },
    searchNominatim () {
      let aCounty = null
      if (this.towns[this.sNum].belongs_to && this.mapData.locations.obj[this.towns[this.sNum].belongs_to] && this.mapData.locations.obj[this.towns[this.sNum].belongs_to].name) {
        aCounty = this.mapData.locations.obj[this.towns[this.sNum].belongs_to].name
      }
      let aQuery = ((this.country && this.country.trim().length > 0) ? this.country.trim() + ' ' : '') + (this.sBelongsTo && aCounty ? aCounty + ' ' : '') + this.towns[this.sNum].name
      console.log('searchNominatim', aQuery)
      this.searching = true
      this.$http
        .get('https://nominatim.openstreetmap.org/search/?format=json&limit=1&q=' + encodeURIComponent(aQuery))
        .then((response) => {
          if (response.body && response.body[0]) {
            let aPlace = response.body[0]
            if (aPlace.lat && aPlace.lon && aPlace.osm_id && aPlace.osm_type) {
              this.$set(this.mapData.locations.obj[this.towns[this.sNum].id], 'lat_new', parseFloat(aPlace.lat))
              this.$set(this.mapData.locations.obj[this.towns[this.sNum].id], 'lon_new', parseFloat(aPlace.lon))
              this.$set(this.mapData.locations.obj[this.towns[this.sNum].id], 'osm_id', parseInt(aPlace.osm_id))
              this.$set(this.mapData.locations.obj[this.towns[this.sNum].id], 'osm_type', aPlace.osm_type)
              this.$set(this.mapData.locations.obj[this.towns[this.sNum].id], 'changed', true)
              // console.log(aPlace, this.towns[this.sNum])
              this.results.unshift(aQuery + ' - ' + aPlace.lat + ', ' + aPlace.lon + ' - ' + aPlace.osm_id + ' - ' + aPlace.osm_type)
            } else {
              this.results.unshift(aQuery + ' - Not found!')
            }
          } else {
            this.results.unshift(aQuery + ' - Not found!')
          }
          this.sNum += 1
          if (this.sNum > this.towns.length - 1) {
            this.searching = false
          }
          if (this.searching) {
            this.searchNominatim()
          }
        })
        .catch((err) => {
          console.log(err)
        })
    }
  },
  computed: {
  },
  components: {
  }
}
</script>

<style scoped>
  .results {
    max-height: 25vh;
    overflow-y: auto;
    padding: 0.5rem 1rem;
    border: 1px solid #ccc;
    border-radius: 0.5rem;
    margin: 0 -1rem;
  }
</style>
