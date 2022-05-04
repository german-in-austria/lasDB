<template>
  <div>
    <v-menu offset-y v-if="select">
      <template v-slot:activator="{ on }">
        <v-btn flat v-on="on" class="not-upper">{{selectedPdfFile ? 'PDF: ' + (selectedPdfFile.title || selectedPdfFile.filename) : 'Select PDF'}}<v-icon class="ml-1">arrow_drop_down</v-icon></v-btn>
      </template>
      <v-list>
        <v-list-tile @click="selectedPdfFile = pdfFile" :class="(pdfFile.edit_data ? 'editdata' : 'noteditdata') + (pdfFile.filename === selectedPdfFile.filename ? ' selected' : '')" v-for="(pdfFile, key) in pdfFiles" :key="'pf' + key">
          <v-list-tile-title class="d-flex">
            <div class="filename">{{ pdfFile.title || pdfFile.filename }}</div>
            <div class="filesize">{{ (pdfFile.size / 1024000).toLocaleString(undefined, {minimumFractionDigits: 1, maximumFractionDigits: 1}) }} MB</div>
          </v-list-tile-title>
        </v-list-tile>
      </v-list>
    </v-menu>
    <div class="pdfselect" v-else>
      <h3 class="my-4">Select PDF</h3>
      <v-list>
        <v-list-tile @click="selectedPdfFile = pdfFile" :class="pdfFile.edit_data ? 'editdata' : 'noteditdata'" v-for="(pdfFile, key) in pdfFiles" :key="'pf' + key">
          <v-list-tile-title class="d-flex">
            <div class="filename">{{ pdfFile.title || pdfFile.filename }}</div>
            <div class="filesize">{{ (pdfFile.size / 1024000).toLocaleString(undefined, {minimumFractionDigits: 1, maximumFractionDigits: 1}) }} MB</div>
          </v-list-tile-title>
        </v-list-tile>
      </v-list>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EditDataPdfSelect',
  props: ['value', 'user', 'options', 'csrf', 'select'],
  data () {
    return {
      pdfFiles: [],
      selectedPdfFile: null,
      loading: false
    }
  },
  mounted () {
    this.selectedPdfFile = this.value
    this.getPdfFiles()
  },
  methods: {
    getPdfFiles () {
      console.log('getPdfFiles')
      this.loading = true
      this.$http
        .post('/editData/', {
          get: 'getPdfFiles'
        }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
        .then((response) => {
          this.pdfFiles = response.data.pdfFiles
          this.pdfFiles.forEach(aPdfFile => {
            if (aPdfFile.options) {
              aPdfFile.options = JSON.parse(aPdfFile.options)
            }
            if (aPdfFile.page_options) {
              aPdfFile.page_options = JSON.parse(aPdfFile.page_options)
            }
          })
          this.loading = false
        })
        .catch((err) => {
          console.log(err)
          this.loading = false
        })
    }
  },
  watch: {
    selectedPdfFile () {
      this.$emit('input', this.selectedPdfFile)
    }
  }
}
</script>

<style scoped>
.filesize {
  text-align: right;
  padding-left: 0.75rem;
  font-size:0.9rem;
  color: #999;
}
.noteditdata >>> a {
  color: #aaa;
}
.selected {
  background-color: #44f;
}
.selected >>> a {
  color: #eee;
}
</style>
