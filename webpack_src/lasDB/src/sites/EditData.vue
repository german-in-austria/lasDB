<template>
  <v-layout id="edit-data" justify-start column fill-height>
    <v-layout justify-start shrink>
      <h1>Data</h1>
      <EditDataPdfSelect v-model="selectedPdfFile" :user="user" :options="options" :csrf="csrf" :select="true" v-if="selectedPdfFile" />
      <v-spacer />
      <EditDataPdfPagination :selectedPdfFile="selectedPdfFile" :user="user" :options="options" :csrf="csrf" v-if="selectedPdfFile && selectedPdfFile.localData && selectedPdfFile.localData.maxPdfSite > 0" />
    </v-layout>
    <EditDataPdfEditor
      :selectedPdfFile="selectedPdfFile"
      :pdfPath="pdfPath"
      :baseData="baseData"
      :user="user" :options="options" :csrf="csrf"
      v-if="selectedPdfFile && !update" />
    <EditDataPdfSelect v-model="selectedPdfFile" :user="user" :options="options" :csrf="csrf" v-else-if="!update" />
    <v-layout class="vpc-frm" align-center justify-center v-if="loading">
      <v-progress-circular :size="100" :width="15" indeterminate color="primary" class="vpc-loading text-center">
        <span class="loading-text">Loading data</span>
      </v-progress-circular>
    </v-layout>
  </v-layout >
</template>

<script>
import EditDataPdfSelect from './EditData/EditDataPdfSelect.vue'
import EditDataPdfEditor from './EditData/EditDataPdfEditor.vue'
import EditDataPdfPagination from './EditData/EditDataPdfPagination.vue'

export default {
  name: 'EditData',
  props: ['user', 'options', 'csrf'],
  data () {
    return {
      pdfPath: '/private-media/pdf/',
      selectedPdfFile: null,
      update: false,
      loading: true,
      baseData: {
        informants: {list: [], obj: {}},
        locations: {list: [], obj: {}, listCounty: [], listTown: []},
        loc_types: {list: [], obj: {}}
      }
    }
  },
  mounted () {
    console.log('EditData mounted ...')
    if (!this.options.edit.data) {
      this.$set(this.options.edit, 'data', {panelWidth: [33.3, 33.3, 33.4]})
    }
    this.loadBaseData()
  },
  methods: {
    loadBaseData () {
      console.log('loadBaseData')
      this.loading = true
      this.$http
        .post('/editData/', {
          get: 'getBaseData'
        }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
        .then((response) => {
          if (!response.data || response.data.errors) {
            alert('Error: ' + (!response.data ? 'No data!' : response.data.errors))
            console.log('loadBaseData - Error', response)
          } else {
            let aLocTyp = {list: response.data.loc_types, obj: {}}
            aLocTyp.list.forEach(t => {
              aLocTyp.obj[t.id] = t
            })
            let aLocs = {list: response.data.locations, obj: {}, listCounty: [], listTown: []}
            aLocs.listCounty = aLocs.list.filter(l => l.type === 1)
            aLocs.listTown = aLocs.list.filter(l => l.type === 2)
            aLocs.list.forEach(l => {
              l.informants = []
              aLocs.obj[l.id] = l
            })
            let aInfs = {list: response.data.informants, obj: {}}
            aInfs.list.forEach(i => {
              i.for_county = i.for_district
              if (!/^(\d{1,99})([a-z]{0,1})$/.test(i.las_num.toLowerCase().trim())) {
                alert('Error in las_num "' + i.las_num + '" id: ' + i.id + ' !')
                console.log('Errror in las_num!', i)
              } else {
                let aMatch = i.las_num.toLowerCase().trim().match(/^(\d{1,99})([a-z]{0,1})$/)
                i.lnZahl = aMatch ? parseInt(aMatch[1]) : parseInt(i.las_num)
                i.lnBuchstabe = aMatch ? aMatch[2] || '' : ''
              }
              if (i.for_district > 0) {
                if (aLocs.obj[i.for_district]) {
                  aLocs.obj[i.for_district].informants.push(i)
                }
              }
              aInfs.obj[i.id] = i
            })
            aInfs.list.sort((a, b) => a.lnZahl > b.lnZahl ? 1 : a.lnZahl < b.lnZahl ? -1 : a.lnBuchstabe.toLowerCase().localeCompare(b.lnBuchstabe.toLowerCase()))
            aLocs.list.forEach(l => {
              if (l.belongs_to > 0 && aLocs.obj[l.belongs_to]) {
                l.informants.forEach(i => {
                  i.for_county = l.belongs_to
                })
                aLocs.obj[l.belongs_to].informants = [...aLocs.obj[l.belongs_to].informants, ...l.informants]
              }
            })
            aLocs.list.forEach(l => {
              l.informants.sort((a, b) => a.lnZahl > b.lnZahl ? 1 : a.lnZahl < b.lnZahl ? -1 : a.lnBuchstabe.toLowerCase().localeCompare(b.lnBuchstabe.toLowerCase()))
            })
            console.log('Sorted informants:', aInfs.list.map(i => i.las_num))
            console.log('Informants by countys:', [aLocs.listCounty.map(l => { return l.name + ':\n' + l.informants.map(i => i.las_num).join(', ') }).join('\n')])
            this.$set(this.baseData, 'informants', aInfs)
            this.$set(this.baseData, 'locations', aLocs)
            this.$set(this.baseData, 'loc_types', aLocTyp)
            console.log('baseData', this.baseData)
          }
          this.loading = false
        })
        .catch((err) => {
          alert('Error: Can\'t load "baseData"!')
          console.log('loadBaseData', err)
          this.loading = false
        })
    }
  },
  watch: {
    selectedPdfFile (nVal) {
      this.update = true
      this.$nextTick(() => {
        this.update = false
      })
    }
  },
  components: {
    EditDataPdfSelect,
    EditDataPdfEditor,
    EditDataPdfPagination
  }
}
</script>

<style scoped>
  .vpc-loading >>> .v-progress-circular__overlay {
    -webkit-transition: none;
    transition: none;
  }
  .vpc-frm {
    position: absolute;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;
    z-index: 11111;
    background: rgba(0,0,0,0.25);
  }
  .loading-text {
    color: #fff;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.75);
  }
</style>
