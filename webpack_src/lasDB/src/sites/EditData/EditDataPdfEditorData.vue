<template>
  <div ref="main">
    <v-card flat style="padding-bottom:300px;">
      <v-card-text>
        <div class="variable-place-frame">
          <div v-if="newVariable">
            <v-layout row wrap>
              <v-flex xs12>
                <h2 class="mb-2">variable</h2>
                <b>OCR identifier:</b> {{ newVariable.pdf_ocr_identifier }}
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model="newVariable.variable"
                  :rules="[(value => value && value.length > 1 ? value.length <= 255 ? true : 'Max 255 characters' : 'Min 2 characters')]"
                  label="variable"
                  counter
                  maxlength="255"
                  autofocus
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-textarea
                  label="comment"
                  v-model="newVariable.comment"
                  rows="1"
                  auto-grow
                ></v-textarea>
              </v-flex>
              <v-flex xs12>
                <h2 class="mb-2">question{{ newVariable.in_question.id > 0 ? ' (id: ' + newVariable.in_question.id + ')' : '' }}</h2>
              </v-flex>
              <v-flex xs12 md4 pr-2>
                <v-text-field
                  v-model="newVariable.in_question.survey_number"
                  :rules="[(value => value > 0 || 'This field is required')]"
                  label="survey_number"
                  type="number"
                  @input="inputIntNumber(newVariable.in_question, 'survey_number')"
                  :readonly="newVariable.in_question.id > 0"
                ></v-text-field>
              </v-flex>
              <v-flex xs12 md4 pr-2>
                <v-text-field
                  v-model="newVariable.in_question.question_number"
                  :rules="[(value => value && value.length >= 1 || 'This field is required')]"
                  label="question_number"
                  :readonly="newVariable.in_question.id > 0"
                ></v-text-field>
              </v-flex>
              <v-flex xs12 md4>
                <v-checkbox
                  label="postal_survey"
                  v-model="newVariable.in_question.postal_survey"
                  :readonly="newVariable.in_question.id > 0"
                ></v-checkbox>
              </v-flex>
              <v-flex xs12>
                <v-textarea
                  label="question"
                  v-model="newVariable.in_question.question"
                  :rules="[(value => value && value.length > 1 || 'Min 1 characters')]"
                  rows="1"
                  auto-grow
                  :readonly="newVariable.in_question.id > 0"
                ></v-textarea>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model="newVariable.in_question.question_type"
                  :rules="[(value => !value || value.length <= 120 || 'Max 120 characters')]"
                  label="question_type"
                  counter
                  maxlength="120"
                  :readonly="newVariable.in_question.id > 0"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-textarea
                  label="comment"
                  v-model="newVariable.in_question.comment"
                  rows="1"
                  auto-grow
                  :readonly="newVariable.in_question.id > 0"
                ></v-textarea>
              </v-flex>
              <v-flex xs12>
                <v-btn color="primary" @click="createVariable">Create variable{{ 1 > newVariable.in_question.id ? ' and question' : '' }}</v-btn>
              </v-flex>
            </v-layout>
          </div>
          <div v-else>
            <div v-if="selectedVariable > 0">
              <v-btn @click="loadVariable" flat fab small style="position:absolute;right:30px;top:0px;width:20px;height:20px;"><v-icon>mdi-reload</v-icon></v-btn>
              <v-btn @click="selectedVariable = -1" flat fab small style="position:absolute;right:0px;top:0px;width:20px;height:20px;"><v-icon>mdi-close</v-icon></v-btn>
              <template v-if="selectedVariableObj">
                <div style="border-left:solid 5px #bbb;" class="pl-3">
                  <div class="fx-header">Variable</div>
                  <h2 :title="'variable id: ' + selectedVariableObj.lex_variable.id + ' - question id: ' + selectedVariableObj.lex_variable.in_question.id">{{ selectedVariableObj.lex_variable.variable }} (PQ{{ selectedVariableObj.lex_variable.in_question.survey_number }}, {{ selectedVariableObj.lex_variable.in_question.question_number }})</h2>
                  <p>{{ selectedVariableObj.lex_variable.comment }}</p>
                </div>
                <div v-for="(pVal, pKey) in dataPlaceList" :key="'pl' + pKey">
                  <div style="border-left:solid 5px #ddd;" class="pl-3 mb-3">
                    <div class="fx-header">Place</div>
                    <h3>{{ pVal.place.name }}</h3>
                  </div>
                  <v-layout mb-3 row wrap>
                    <v-flex xs12 md3 pr-3><div class="fx-header fx-header-bb">Variant</div></v-flex>
                    <v-flex xs12 md9 pl-3><div class="fx-header fx-header-bb">Informants</div></v-flex>
                  </v-layout>
                  <v-layout v-for="(vtVal, vtKey) in pVal.list" :key="'pl' + pKey + 'vt' + vtKey" class="var-infs" mb-2 row wrap>
                    <v-flex xs12 md3 pr-3>
                      <b class="variant"
                        :title="'variant id:' + vtVal.lex_variant.id + '\ncomment: ' + (vtVal.lex_variant.comment ? vtVal.lex_variant.comment : 'none')"
                        @click="editData(vtVal)"
                      >{{ vtVal.lex_variant.variant }}</b>
                    </v-flex>
                    <v-flex xs12 md9 pl-3>
                      <div class="informant"
                        :title="'informant id: ' + dVal.by_inf + '\nfor_district: ' + baseData.locations.obj[baseData.informants.obj[dVal.by_inf].for_district].name + '\nsort: ' + dVal.sort"
                        v-for="(dVal, dKey) in vtVal.list" :key="'pl' + pKey + 'vt' + vtKey + 'd' + dKey"
                      >{{ baseData.informants.obj[dVal.by_inf].las_num + (dVal.plus ? '+' : '') + (dVal.star ? '*' : '') + (dVal.italics ? '/' : '') + (dVal.superscript && dVal.superscript.length > 0 ? '[' + dVal.superscript + ']' : '') }}</div>
                    </v-flex>
                    <v-flex xs12 v-if="showEditData === vtVal">
                      <EditData @close="closeEditData" :showEditData="showEditData" :placeId="pVal.place.id" :showAddData="false" :selectedVariableObj="selectedVariableObj" :dataPlaceList="dataPlaceList" :selectedPdfFile="selectedPdfFile" :baseData="baseData" :user="user" :options="options" :csrf="csrf" />
                    </v-flex>
                  </v-layout>
                  <v-layout mb-4>
                    <v-btn @click="addData(pVal)" color="primary" small :disabled="showAddData !== false || showEditData !== false" v-if="showAddData !== pVal" :title="pVal.place.name">add data to place</v-btn>
                    <EditData @close="closeEditData" :showAddData="showAddData" :showEditData="false" :selectedVariableObj="selectedVariableObj" :dataPlaceList="dataPlaceList" :selectedPdfFile="selectedPdfFile" :baseData="baseData" :user="user" :options="options" :csrf="csrf" v-if="showAddData === pVal" />
                  </v-layout>
                </div>
                <v-layout mb-4>
                  <v-btn @click="addData(null)" color="primary" small :disabled="showAddData !== false || showEditData !== false" v-if="showAddData !== null && showAddData !== 'OCR'">add data</v-btn>
                  <EditData ref="ocrEditData" @close="closeEditData" :ocrEditData="ocrEditData" :showAddData="showAddData" :showEditData="false" :selectedVariableObj="selectedVariableObj" :dataPlaceList="dataPlaceList" :selectedPdfFile="selectedPdfFile" :baseData="baseData" :user="user" :options="options" :csrf="csrf" v-if="showAddData === null || showAddData === 'OCR'" />
                </v-layout>
              </template>
              <div v-else>
                variable {{ selectedVariable }}: No Data!
              </div>
            </div>
            <div v-else>
              <SelectVariable @select="selectVariable" :user="user" :options="options" :csrf="csrf" />
            </div>
          </div>
        </div>
      </v-card-text>
    </v-card>
    <v-layout class="vpc-frm" align-center justify-center v-if="loading">
      <v-progress-circular :size="100" :width="15" indeterminate color="primary" class="vpc-loading text-center">
        <span class="loading-text">Loading data</span>
      </v-progress-circular>
    </v-layout>
  </div>
</template>

<script>
import SelectVariable from './EditDataPdfEditorData/SelectVariable.vue'
import EditData from './EditDataPdfEditorData/EditData.vue'

export default {
  name: 'EditDataPdfEditorData',
  props: ['baseData', 'selectedPdfFile', 'ocrVariableSelected', 'ocrBlockObj', 'user', 'options', 'csrf'],
  data () {
    return {
      loading: false,
      newVariable: null,
      selectedVariable: -1,
      selectedVariableObj: null,
      showAddData: false,
      showEditData: false,
      ocrEditData: null
    }
  },
  mounted () {
    console.log('EditDataPdfEditorData', this.selectedPdfFile, this.baseData)
    this.selectOcrVariable()
  },
  methods: {
    closeEditData (reload) {
      this.showAddData = false
      this.showEditData = false
      if (reload) {
        this.loadVariable()
      }
    },
    editData (v = null) {
      if (this.showAddData === false && this.showEditData === false) {
        this.resortData()
        this.showEditData = v
      }
    },
    addData (p = null) {
      if (this.showAddData === false && this.showEditData === false) {
        this.resortData()
        this.showAddData = p
      }
    },
    loadVariable () {
      console.log('loadVariable', this.selectedVariable)
      if (this.selectedVariable > 0) {
        this.loading = true
        this.$http
          .post('/editData/', {
            get: 'getVariableData',
            id: this.selectedVariable
          }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
          .then((response) => {
            if (!response.data || response.data.errors) {
              alert('Error: ' + (!response.data ? 'No data!' : response.data.errors))
              console.log('loadVariable - Error', response)
            } else {
              this.selectedVariableObj = {
                lex_variable: response.data.lex_variable[0],
                data: {list: response.data.data, obj: {}},
                lex_variant: {list: response.data.lex_variant, obj: {}}
              }
              this.selectedVariableObj.lex_variant.list.forEach(v => {
                this.selectedVariableObj.lex_variant.obj[v.id] = v
              })
              this.selectedVariableObj.data.list.forEach(d => {
                this.selectedVariableObj.data.obj[d.id] = d
              })
              this.resortData()
              console.log('loadVariable', response.data, this.selectedVariableObj)
            }
            this.loading = false
          })
          .catch((err) => {
            alert('Error: Can\'t load "OCR Variable"!')
            console.log('loadVariable', err)
            this.loading = false
          })
      }
    },
    resortData () {
      let aSort = 0
      this.dataPlaceList.forEach(p => {
        p.list.forEach(v => {
          v.list.forEach(d => {
            d.sort = aSort
            aSort += 1
          })
        })
      })
    },
    selectVariable (id) {
      // console.log('selectVariable', id)
      this.selectedVariable = id
    },
    createVariable () {
      console.log('createVariable', this.newVariable)
      if (this.newVariable) {
        let errors = []
        if (!this.newVariable.variable || this.newVariable.variable.trim().length < 2) {
          this.newVariable.variable = this.newVariable.variable.trim()
          errors.push('Variable needed!')
        }
        this.newVariable.in_question.survey_number = parseInt(this.newVariable.in_question.survey_number) || 0
        if (this.newVariable.in_question.survey_number < 1) {
          errors.push('Survey number needed!')
        }
        if (!this.newVariable.in_question.question_number || this.newVariable.in_question.question_number.trim().length < 1) {
          this.newVariable.in_question.question_number = this.newVariable.in_question.question_number.trim()
          errors.push('Question number needed!')
        }
        if (!this.newVariable.in_question.question || this.newVariable.in_question.question.trim().length < 1) {
          this.newVariable.in_question.question = this.newVariable.in_question.question.trim()
          errors.push('Question needed!')
        }
        if (errors.length > 0) {
          alert('Error!\n\n' + errors.join('\n'))
        } else {
          this.loading = true
          this.$http
            .post('/editData/', {
              set: 'setVariableByOCR',
              data: JSON.stringify(this.newVariable)
            }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
            .then((response) => {
              if (response.data && response.data.ok) {
                this.selectedVariable = response.data.variableId
                this.newVariable = null
              } else {
                alert('Error while saving variable/question!')
              }
              this.loading = false
            })
            .catch((err) => {
              alert('Error while saving variable/question!')
              console.log(err)
              this.loading = false
            })
        }
      }
    },
    selectOcrVariable () {
      if (this.ocrVariableSelected && (!this.selectedVariableObj || this.ocrVariableSelected.strings.id !== this.selectedVariableObj.lex_variable.pdf_ocr_identifier)) {
        this.newVariable = null
        this.selectedVariable = -1
        this.selectedVariableObj = null
        this.loading = true
        let aQuestSurv = (this.ocrVariableSelected.strings.question || '').split(',')
        if (aQuestSurv[0]) {
          aQuestSurv[0] = parseInt(aQuestSurv[0].trim().substring(2))
        }
        if (aQuestSurv[1]) {
          aQuestSurv[1] = aQuestSurv[1].trim()
        }
        this.$http
          .post('/editData/', {
            get: 'getVariableByOCR',
            ocrId: this.ocrVariableSelected.strings.id,
            survey_number: aQuestSurv[0] ? aQuestSurv[0] : 0,
            question_number: aQuestSurv[1] ? aQuestSurv[1] : ''
          }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
          .then((response) => {
            if (!response.data || response.data.errors) {
              alert('Error: ' + (!response.data ? 'No data!' : response.data.errors))
              console.log('ocrVariableSelected - Error', response)
            } else {
              this.selectedVariable = response.data.variableId || -1
              if (this.selectedVariable < 1) {
                this.newVariable = {
                  id: -1,
                  variable: this.ocrVariableSelected.strings.variable || this.ocrVariableSelected.strings.id || '',
                  in_question: {
                    id: -1,
                    survey_number: aQuestSurv[0] ? aQuestSurv[0] : null,
                    question_number: aQuestSurv[1] ? aQuestSurv[1] : '',
                    postal_survey: false,
                    question: '?',
                    question_type: '',
                    comment: ''
                  },
                  comment: this.ocrVariableSelected.strings.comment || '',
                  pdf_ocr_identifier: this.ocrVariableSelected.strings.id || null
                }
                if (response.data.question && response.data.question.length > 0) {
                  this.$set(this.newVariable, 'in_question', response.data.question[0])
                }
                console.log('newVariable', this.newVariable, response)
              }
            }
            this.loading = false
          })
          .catch((err) => {
            alert('Error: Can\'t load "OCR Variable"!')
            console.log('ocrVariableSelected', err)
            this.loading = false
          })
      }
    },
    inputFloatNumber (v, p) {
      if (typeof v[p] === 'string') {
        v[p] = parseFloat(v[p]) || 0
      }
    },
    inputIntNumber (v, p) {
      if (typeof v[p] === 'string') {
        v[p] = parseInt(v[p]) || 0
      }
    }
  },
  computed: {
    dataPlaceList () {
      if (this.selectedVariableObj && this.selectedVariableObj.data) {
        let byPlaceAndVariant = {}
        this.selectedVariableObj.data.list.forEach(d => {
          if (!byPlaceAndVariant[this.baseData.informants.obj[d.by_inf].for_county]) {
            byPlaceAndVariant[this.baseData.informants.obj[d.by_inf].for_county] = {}
          }
          if (!byPlaceAndVariant[this.baseData.informants.obj[d.by_inf].for_county][d.lex_variant]) {
            byPlaceAndVariant[this.baseData.informants.obj[d.by_inf].for_county][d.lex_variant] = []
          }
          byPlaceAndVariant[this.baseData.informants.obj[d.by_inf].for_county][d.lex_variant].push(d)
        })
        return Object.keys(byPlaceAndVariant).map(p => {
          return {
            place: this.baseData.locations.obj[p],
            list: Object.keys(byPlaceAndVariant[p]).map(v => {
              return {
                lex_variant: this.selectedVariableObj.lex_variant.obj[byPlaceAndVariant[p][v][0].lex_variant],
                list: byPlaceAndVariant[p][v]
              }
            }).sort((a, b) => a.lex_variant.variant.toLowerCase().localeCompare(b.lex_variant.variant.toLowerCase()))
          }
        }).sort((a, b) => a.place.sort - b.place.sort)
      } else {
        return []
      }
    }
  },
  watch: {
    selectedVariable () {
      if (this.selectedVariable > 0) {
        if (!this.selectedVariableObj || this.selectedVariable !== this.selectedVariableObj.lex_variable.id) {
          this.showAddData = false
          this.showEditData = false
          if (!this.selectedVariableObj) {
            this.loadVariable()
          }
        }
      } else {
        this.selectedVariableObj = null
        this.$emit('unselectVariable')
      }
    },
    ocrVariableSelected () {
      console.log('ocrVariableSelected', this.ocrVariableSelected)
      this.selectOcrVariable()
    },
    ocrBlockObj () {
      if (this.ocrBlockObj && this.selectedVariable > 0 && this.showAddData === false && this.showEditData === false) {
        let place = (this.ocrBlockObj.place && this.ocrBlockObj.place.str && this.ocrBlockObj.place.str.trim().length > 0 ? this.ocrBlockObj.place.str.trim() : null)
        this.ocrEditData = {
          place: place,
          datas: this.ocrBlockObj.varInfs.map(vi => {
            let str = vi.el.map(e => e.str).join('').trim()
            return {ocrId: (place || '') + ' > ' + str, str: str}
          })
        }
        this.ocrEditData.datas = this.ocrEditData.datas.filter(d => {
          return this.selectedVariableObj.data.list.filter(dl => dl.pdf_ocr_identifier === d.ocrId).length < 1
        })
        if (this.ocrEditData.datas.length > 0) {
          this.showAddData = 'OCR'
          this.$nextTick(() => {
            this.$refs.main.parentElement.parentElement.parentElement.scrollTop = this.$refs.ocrEditData.$el.offsetTop - 10
            console.log('scrollTo', this.$refs.ocrEditData.$el.offsetTop, this.$refs.main.parentElement.parentElement.parentElement.scrollTop)
          })
        } else {
          this.ocrEditData = null
          alert('All data already taken over!')
        }
        console.log('ocrBlockObj', this.ocrBlockObj, this.ocrEditData)
      }
    }
  },
  components: {
    SelectVariable,
    EditData
  }
}
</script>

<style scoped>
  .fx-header {
    font-size: 12px;
    color: rgba(0,0,0,0.54);
  }
  .fx-header-bb {
    border-bottom: 1px solid #ddd;
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
  .loading-text {
    color: #fff;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.75);
  }
  .variant {
    display: block;
    cursor: pointer;
  }
  .variant:hover {
    color: #00b;
    text-decoration: underline;
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
</style>
