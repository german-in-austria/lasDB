<template>
  <div class="add-data">
    <v-btn @click="$emit('close')" flat fab small style="position:absolute;right:0px;top:0px;width:20px;height:20px;z-index:3;"><v-icon>mdi-close</v-icon></v-btn>
    <v-layout row wrap>
      <v-flex xs12>
        <div v-if="editData.placeOcrStr"><b>OCR String - place:</b> {{ editData.placeOcrStr }}</div>
        <v-autocomplete
          v-model="editData.placeId"
          :items="baseData.locations.listCounty"
          label="place"
          item-text="name"
          item-value="id"
        />
      </v-flex>
    </v-layout>
    <template v-if="editData.placeId > 0">
      <v-layout row wrap v-for="(vVal, vKey) in editData.variants" :key="'ev' + vKey">
        <v-flex xs12 v-if="editData.variants.length > 1">
          <hr class="fx-hr my-2">
        </v-flex>
        <v-flex xs12 v-if="vVal.variantInfsOcrStr">
          <b>OCR String:</b> {{ vVal.variantInfsOcrStr }}
        </v-flex>
        <v-flex xs12 md4 pr-2>
          <v-text-field
            v-model="vVal.variantText"
            label="variant string"
            append-icon="mdi-magnify"
            @click:append="searchVariant(vKey)"
            @keypress.enter="searchVariant(vKey)"
            spellcheck="false"
          ></v-text-field>
        </v-flex>
        <v-flex xs12 md8 pl-2>
          <v-text-field
            v-model="vVal.informants.informantsText"
            :rules="[(value => value && value.length > 0 || 'This field is required')]"
            label="informants string"
            append-icon="mdi-elevator-down"
            @click:append="searchInformants(vKey)"
            @keypress.enter="searchInformants(vKey)"
            spellcheck="false"
          >
            <v-tooltip slot="append" top>
              <v-icon @click="searchInformants(vKey)" slot="activator">mdi-elevator-down</v-icon>
              <span>
                "7+" for the raised +<br>
                "7*" for the raised *<br>
                "7/" for italics<br>
                "7[a]" for superscripted alphabetics<br>
              </span>
            </v-tooltip>
          </v-text-field>
        </v-flex>
        <v-flex xs12 md4 pr-2>
          <v-select
            v-model="vVal.id"
            :items="vVal.variantSelect"
            label="variant database"
            item-text="variant"
            item-value="id"
            :hint="vVal.variantText.trim().length < 2 ? 'Need variant string' : 'variants found: ' + vVal.variantSelect.filter(v => v.id > 0).length + ' - id: ' + vVal.id"
            :persistent-hint="true"
            :loading="loading"
          ></v-select>
        </v-flex>
        <v-flex xs12 md8 pl-2>
          <div class="fx-header">informants database</div>
          <div>
            <div class="informant"
              :title="'informant id: ' + iVal.id + '\nfor_district: ' + baseData.locations.obj[iVal.infObj.for_district].name"
              v-for="(iVal, iKey) in vVal.informants.list" :key="'ev' + vKey + 'i' + iKey"
            >{{ iVal.infObj.las_num + (iVal.plus ? '+' : '') + (iVal.star ? '*' : '') + (iVal.italics ? '/' : '') + (iVal.superscript && iVal.superscript.length > 0 ? '[' + iVal.superscript + ']' : '') }}</div>
          </div>
          <div class="missing-informants" v-if="missingInformants[vKey] && missingInformants[vKey].length > 0">
            missing informants: {{ missingInformants[vKey].join(', ') }}
          </div>
          <div class="duplicated-informants" v-if="duplicatedInformants[vKey] && duplicatedInformants[vKey].length > 0">
            duplicated informants: {{ duplicatedInformants[vKey].join(', ') }}
          </div>
        </v-flex>
      </v-layout>
      <v-layout mt-3>
        <v-btn @click="deleteData" color="warning" v-if="showEditData !== false">Delete Data</v-btn>
        <v-spacer />
        <v-btn @click="saveData" color="primary" :disabled="error">Save Data (variant/informants)</v-btn>
      </v-layout>
    </template>
    <div v-else>
      Please select place!
    </div>
    <v-layout class="vpc-frm" align-center justify-center v-if="saving">
      <v-progress-circular :size="100" :width="15" indeterminate color="primary" class="vpc-saving text-center">
        <span class="saving-text">Saving data</span>
      </v-progress-circular>
    </v-layout>
  </div>
</template>

<script>
export default {
  name: 'EditData',
  props: ['showEditData', 'placeId', 'ocrEditData', 'showAddData', 'selectedVariableObj', 'dataPlaceList', 'selectedPdfFile', 'baseData', 'user', 'options', 'csrf'],
  data () {
    return {
      loading: false,
      saving: false,
      editData: {
        variableId: null,
        placeId: null,
        placeOcrStr: null,
        variants: []
      },
      missingInformants: {},
      duplicatedInformants: {},
      searchVariantNext: []
    }
  },
  mounted () {
    this.editData.variableId = this.selectedVariableObj.lex_variable.id
    if (this.showAddData !== false) {
      if (this.showAddData === 'OCR') {
        let ocrPlaceStr = this.ocrEditData.place.toLowerCase().replace('cont\'d', '').trim()
        let pPlaceList = this.baseData.locations.listCounty.filter(l => l.name.trim().toLowerCase() === ocrPlaceStr)
        this.editData.placeId = pPlaceList && pPlaceList.length > 0 ? pPlaceList[0].id || null : null
        this.editData.placeOcrStr = this.ocrEditData.place
        this.editData.variants = []
        this.ocrEditData.datas.forEach((d, k) => {
          let ocrList = d.str.split(/-(.+)/)
          this.editData.variants.push({
            id: 0,
            variantText: ocrList[0].trim(),
            variantSelect: [],
            variantInfsOcrStr: d.str,
            variantInfsOcrId: d.ocrId,
            pdfFilename: this.selectedPdfFile.filename,
            pdfPage: this.selectedPdfFile.localData.selectedPdfSite,
            sort: 1 + k, // ToDo: Sort!
            informants: {
              informantsText: ocrList[1].trim(),
              list: []
            }
          })
        })
        this.editData.variants.forEach((v, k) => {
          this.searchVariant(k)
          if (this.editData.placeId) {
            this.searchInformants(k)
          }
        })
        console.log('ocrEditData', this.ocrEditData, this.editData.placeId)
      } else {
        this.editData.placeId = this.showAddData && this.showAddData.place ? this.showAddData.place.id : null
        this.editData.variants = [{
          id: 0,
          variantText: '',
          variantSelect: [],
          variantInfsOcrStr: null,
          variantInfsOcrId: null,
          pdfFilename: this.selectedPdfFile.filename,
          pdfPage: this.selectedPdfFile.localData.selectedPdfSite,
          sort: 1 + 0, // ToDo: Sort!
          informants: {
            informantsText: '',
            list: []
          }
        }]
      }
      console.log('showAddData', this.showAddData, this.baseData, this.editData)
    } else if (this.showEditData !== false) {
      // ToDo: OcrStr !!!!
      this.editData.placeId = this.placeId
      this.editData.variants = [{
        id: this.showEditData.lex_variant.id,
        variantText: this.showEditData.lex_variant.variant,
        variantSelect: [{id: this.showEditData.lex_variant.id, variant: this.showEditData.lex_variant.variant}],
        variantInfsOcrStr: null,
        variantInfsOcrId: this.showEditData.lex_variant.pdf_ocr_identifier,
        informants: {
          informantsText: this.showEditData.list.map(
            i => this.baseData.informants.obj[i.by_inf].las_num + (i.plus ? '+' : '') + (i.star ? '*' : '') + (i.italics ? '/' : '') + (i.superscript && i.superscript.length > 0 ? '[' + i.superscript + ']' : '')
          ).join(', '),
          list: this.showEditData.list.map(i => { return {plus: i.plus, star: i.star, italics: i.italics, superscript: i.superscript, infObj: this.baseData.informants.obj[i.by_inf]} })
        }
      }]
      console.log('showEditData', this.showEditData, this.placeId, this.editData)
    }
  },
  methods: {
    deleteData () {
      console.log('deleteData', this.editData)
      if (confirm('Really delete data records permanently?')) {
        this.saving = true
        this.$http
          .post('/editData/', {
            set: 'deleteData',
            data: JSON.stringify(this.editData)
          }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
          .then((response) => {
            if (response.data && response.data.ok) {
              console.log('deleteData', response.data)
              this.$emit('close', true)
            } else {
              alert('Error while deleting variable/question!')
            }
            this.saving = false
          })
          .catch((err) => {
            alert('Error while deleting variable/question!')
            console.log(err)
            this.saving = false
          })
      }
    },
    saveData () {
      if (!this.error) {
        console.log('saveData', this.editData)
        this.saving = true
        this.$http
          .post('/editData/', {
            set: 'saveData',
            data: JSON.stringify(this.editData)
          }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
          .then((response) => {
            if (response.data && response.data.ok) {
              console.log('saveData', response.data)
              this.$emit('close', true)
            } else {
              alert('Error while saving variable/question!')
            }
            this.saving = false
          })
          .catch((err) => {
            alert('Error while saving variable/question!')
            console.log(err)
            this.saving = false
          })
      }
    },
    searchInformants (key) {
      this.missingInformants[key] = []
      this.duplicatedInformants[key] = []
      let aInfList = []
      let aInfStrList = []
      let aInfText = this.editData.variants[key].informants.informantsText
      let aInfsList = this.baseData.locations.obj[this.editData.placeId].informants.filter(i => i.volume === this.selectedVariableObj.lex_variable.in_question.survey_number).map(i => i.las_num.trim().toLowerCase())
      let aInfSpezials = {}
      let getSpezial = (str) => {
        let aInfSpezial = {}
        if (str.indexOf('+') > -1) {
          aInfSpezial.plus = true
          str = str.replace('+', '')
        }
        if (str.indexOf('*') > -1) {
          aInfSpezial.star = true
          str = str.replace('*', '')
        }
        if (str.indexOf('/') > -1) {
          aInfSpezial.italics = true
          str = str.replace('/', '')
        }
        if (str.indexOf('[') > -1) {
          let suscMatch = str.match(/\[(.+)\]/)
          if (suscMatch && suscMatch[1] && suscMatch[1].trim().length > 0 && suscMatch[1].trim().length < 3) {
            aInfSpezial.superscript = suscMatch[1].trim()
            str = str.replace(/\[.+\]/, '')
          }
        }
        return [str, aInfSpezial]
      }
      aInfText.split(',').forEach(iStr => {
        let iStrC = iStr.trim().toLowerCase().replace(/\s/g, '').replace(/·/g, '-')
        if (iStrC.length > 0) {
          let iStrsC = []
          if (iStrC.indexOf('-') > -1) {
            iStrsC = iStrC.split('-').map(i => i.trim()).filter(i => i.length > 0)
            if (iStrsC.length === 1) {
              aInfStrList.push(iStrsC[0])
            } else if (iStrsC.length === 2) {
              let aInfSpezial = {}
              ;[iStrsC[1], aInfSpezial] = getSpezial(iStrsC[1])
              let iStart = aInfsList.indexOf(iStrsC[0])
              let iEnd = aInfsList.indexOf(iStrsC[1])
              if (iStart > -1 && iEnd > -1) {
                if (iStart > iEnd) { ;[iStart, iEnd] = [iEnd, iStart] }
                aInfStrList = [...aInfStrList, ...aInfsList.slice(iStart, iEnd + 1)]
                aInfsList.slice(iStart, iEnd + 1).forEach(i => { aInfSpezials[i.toLowerCase()] = aInfSpezial })
              } else if (iStart > -1) {
                aInfStrList.push(iStrsC[0])
                aInfSpezials[iStrsC[0].toLowerCase()] = aInfSpezial
                this.missingInformants[key].push(iStrsC[1])
              } else if (iEnd > -1) {
                aInfStrList.push(iStrsC[1])
                aInfSpezials[iStrsC[1].toLowerCase()] = aInfSpezial
                this.missingInformants[key].push(iStrsC[0])
              }
            }
          } else {
            let aInfSpezial = {}
            ;[iStrC, aInfSpezial] = getSpezial(iStrC)
            let abcMatch = iStrC.match(/^(\d{1,99})([a-z]+)$/)
            if (abcMatch && abcMatch[2] && abcMatch[2].length > 1) {
              for (var i = 0; i < abcMatch[2].length; i++) {
                let aStrC = abcMatch[1] + abcMatch[2].charAt(i)
                aInfStrList.push(aStrC)
                aInfSpezials[aStrC.toLowerCase()] = aInfSpezial
              }
            } else {
              aInfStrList.push(iStrC)
              aInfSpezials[iStrC.toLowerCase()] = aInfSpezial
            }
          }
        }
      })
      aInfStrList = aInfStrList.filter((i, k) => {
        let missing = aInfsList.indexOf(i) < 0
        if (missing) {
          this.missingInformants[key].push(i)
        }
        let duplicated = aInfStrList.indexOf(i) !== k
        if (duplicated) {
          this.duplicatedInformants[key].push(i)
        }
        return !duplicated && !missing
      })
      aInfList = aInfStrList.map(i => this.baseData.locations.obj[this.editData.placeId].informants.filter(i => i.volume === this.selectedVariableObj.lex_variable.in_question.survey_number)[aInfsList.indexOf(i)])
      this.editData.variants[key].informants.list = aInfList.sort(
        (a, b) => a.lnZahl > b.lnZahl ? 1 : a.lnZahl < b.lnZahl ? -1 : a.lnBuchstabe.toLowerCase().localeCompare(b.lnBuchstabe.toLowerCase())
      ).map(i => {
        let aInfSpezial = aInfSpezials[i.las_num.toLowerCase()] || {}
        console.log('aInfSpezials', aInfSpezials, i.las_num.toLowerCase(), aInfSpezial)
        return {
          plus: aInfSpezial.plus || false,
          star: aInfSpezial.star || false,
          italics: aInfSpezial.italics || false,
          superscript: aInfSpezial.superscript || null,
          infObj: i
        }
      })
      console.log('searchInformants', key, aInfText, '->', aInfStrList, aInfList.map(i => i.las_num).join(', '), aInfList, '<-', this.baseData.locations.obj[this.editData.placeId].informants.map(i => i.las_num), aInfsList)
    },
    searchVariant (key, nVar) {
      console.log('searchVariant', key, nVar)
      let aVar = nVar || this.editData.variants[key] || null
      if (aVar) {
        if (!this.loading) {
          if (aVar.variantText.trim().length > 1) {
            this.loading = true
            this.$http
              .post('/editData/', {
                get: 'searchVariant',
                str: aVar.variantText.trim()
              }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
              .then((response) => {
                if (!response.data || response.data.errors) {
                  alert('Error: ' + (!response.data ? 'No data!' : response.data.errors))
                  console.log('searchVariant - Error', response)
                } else {
                  if (response.data.variants && response.data.variants.length > 0) {
                    aVar.variantSelect = response.data.variants
                    aVar.id = -1
                    aVar.variantSelect.forEach(vs => {
                      if (vs.variant.toLowerCase() === aVar.variantText.trim().toLowerCase()) {
                        aVar.id = vs.id
                      }
                    })
                    if (aVar.id === -1) {
                      aVar.variantSelect = [{id: -1, variant: 'create variant'}, ...aVar.variantSelect]
                    }
                  } else {
                    aVar.id = -1
                    aVar.variantSelect = [{id: -1, variant: 'create variant'}]
                  }
                  console.log('searchVariant', response.data, this.selectedVariableObj)
                }
                this.loading = false
                if (this.searchVariantNext && this.searchVariantNext.length > 0) {
                  this.searchVariant(null, this.searchVariantNext.shift())
                }
              })
              .catch((err) => {
                alert('Error: Can\'t load "Variants"!')
                console.log('searchVariant', err)
                this.loading = false
              })
          } else {
            alert('Need variant string')
          }
        } else {
          this.searchVariantNext.push(aVar)
        }
      }
    }
  },
  computed: {
    error () {
      let vErr = false
      this.editData.variants.forEach(v => {
        // console.log(v.informants.list.length)
        if (!v.informants.list || v.informants.list.length < 1 || !(v.id === -1 || v.id > 0)) {
          vErr = true
        }
      })
      return vErr || this.editData.placeId < 1
    }
  },
  watch: {
    'editData.placeId' () {
      console.log('editData.placeId', this.editData.placeId)
      if (this.editData.placeId > 0) {
        this.editData.variants.forEach((v, k) => {
          this.searchInformants(k)
        })
      }
    }
  }
}
</script>

<style scoped>
  .fx-header {
    font-size: 12px;
    color: rgba(0,0,0,0.54);
  }
  .fx-hr {
    border: none;
    border-bottom: 3px solid #bbf;
  }
  .add-data {
    position: relative;
    width: 100%;
    border: 3px solid #ddf;
    padding: 0.5rem 0.75rem;
  }
  .informant {
    display: inline-block;
    border: 1px solid transparent;
    border-radius: 4px;
    cursor: pointer;
  }
  .informant:hover {
    border-color: #9f9
  }
  .informant:not(:last-child)::after {
    content: ", ";
  }
  .var-infs {
    border-bottom: 1px solid #eee;
  }
  .missing-informants, .duplicated-informants {
    color: #d00;
  }
  .vpc-frm {
    position: fixed;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;
    z-index: 11111;
    background: rgba(0,0,0,0.25);
  }
  .saving-text {
    color: #fff;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.75);
  }

</style>
