<template>
  <v-card flat>
    <v-card-text>
      <div v-if="textContent">
        <div class="mb-2">
          <b>PDF:</b> Page: {{ selectedPdfFile.localData.selectedPdfSite }} - Width: {{ optionsOverlay.orgWidth.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) }} - Height: {{ optionsOverlay.orgHeight.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) }}<br>
          <b>OCR:</b> Elements:{{ textContent.length.toLocaleString() }}
        </div>
        <v-layout row>
          <v-flex xs12 md6 xl4><v-switch v-model="selectedPdfFile.options.showOCR" label="OCR data"></v-switch></v-flex>
          <v-flex xs12 md6 xl4><v-switch v-model="selectedPdfFile.options.showVarInfs" label="Variant/Infs" :disabled="!selectedPdfFile.options.showOCR"></v-switch></v-flex>
          <v-flex xs12 md6 xl4><v-switch v-model="selectedPdfFile.options.showOCRElements" label="OCR elements"></v-switch></v-flex>
        </v-layout>
        <div v-if="pageOptions && pageOptions.variables">
          <v-layout mb-3>
            <h2><div class="colbox variable"></div>Variable-Areas</h2>
            <v-spacer />
            <v-btn @click="addVariable(false)" color="purple" dark small :disabled="!user.staff">Add</v-btn>
            <v-btn @click="addVariable(true)" small :disabled="!user.staff">Add OCR</v-btn>
          </v-layout>
          <div v-for="(vVal, vKey) in pageOptions.variables" :key="'vOp' + vKey">
            <v-layout>
              <div class="colcount mr-2">{{ vKey + 1 }}</div>
              <v-layout row wrap>
                <v-flex xs12 md6 lg3 px-1><v-text-field v-model="vVal.x" @input="inputFloatNumber(vVal, 'x')" type="number" label="x" placeholder="None" step="0.5" class="pt-0" :readonly="!user.staff"></v-text-field></v-flex>
                <v-flex xs12 md6 lg3 px-1><v-text-field v-model="vVal.y" @input="inputFloatNumber(vVal, 'y')" type="number" label="y" placeholder="None" step="0.5" class="pt-0" :readonly="!user.staff"></v-text-field></v-flex>
                <v-flex xs12 md6 lg3 px-1><v-text-field v-model="vVal.width" @input="inputFloatNumber(vVal, 'width')" type="number" label="width" placeholder="None" step="0.5" class="pt-0" :readonly="!user.staff"></v-text-field></v-flex>
                <v-flex xs12 md6 lg3 px-1><v-text-field v-model="vVal.height" @input="inputFloatNumber(vVal, 'height')" type="number" label="height" placeholder="None" step="0.5" class="pt-0" :readonly="!user.staff"></v-text-field></v-flex>
              </v-layout>
              <v-btn @click="delEntry(pageOptions.variables, vKey)" color="red" class="xsmall" fab small dark :disabled="!user.staff"><v-icon>delete</v-icon></v-btn>
            </v-layout>
          </div>
        </div>
        <div v-if="pageOptions && pageOptions.ignore">
          <v-layout mb-3>
            <h2><div class="colbox ignore"></div>Ignore-Areas</h2>
            <v-spacer />
            <v-btn @click="addIgnore(false)" color="purple" dark small :disabled="!user.staff">Add</v-btn>
            <v-btn @click="addIgnore(true)" small :disabled="!user.staff">Add OCR</v-btn>
          </v-layout>
          <div v-for="(iVal, iKey) in pageOptions.ignore" :key="'ip' + iKey">
            <v-layout>
              <div class="colcount mr-2">{{ iKey + 1 }}</div>
              <v-layout row wrap>
                <v-flex xs12 md6 lg3 px-1><v-text-field v-model="iVal.x" @input="inputFloatNumber(iVal, 'x')" type="number" label="x" placeholder="None" step="0.5" class="pt-0" :readonly="!user.staff"></v-text-field></v-flex>
                <v-flex xs12 md6 lg3 px-1><v-text-field v-model="iVal.y" @input="inputFloatNumber(iVal, 'y')" type="number" label="y" placeholder="None" step="0.5" class="pt-0" :readonly="!user.staff"></v-text-field></v-flex>
                <v-flex xs12 md6 lg3 px-1><v-text-field v-model="iVal.width" @input="inputFloatNumber(iVal, 'width')" type="number" label="width" placeholder="None" step="0.5" class="pt-0" :readonly="!user.staff"></v-text-field></v-flex>
                <v-flex xs12 md6 lg3 px-1><v-text-field v-model="iVal.height" @input="inputFloatNumber(iVal, 'height')" type="number" label="height" placeholder="None" step="0.5" class="pt-0" :readonly="!user.staff"></v-text-field></v-flex>
              </v-layout>
              <v-btn @click="delEntry(pageOptions.ignore, iKey)" color="red" class="xsmall" fab small dark :disabled="!user.staff"><v-icon>delete</v-icon></v-btn>
            </v-layout>
          </div>
        </div>
        <div v-if="pageOptions && pageOptions.cols">
          <v-layout mb-3>
            <h2><div class="colbox col"></div>Columns-Areas</h2>
            <v-icon color="red" class="alert-icon" v-if="pageOptions.cols.length < 1 || pageOptions.cols.length > 4 || allColsContentCount !== variantContent.length">mdi-alert</v-icon>
            <v-spacer />
            <v-btn @click="sortCols" color="blue" class="xsmall" fab small dark title="sort" :disabled="!user.staff"><v-icon>mdi-sort</v-icon></v-btn>
            <v-btn @click="addCol(false)" color="purple" dark small :disabled="!user.staff">Add</v-btn>
            <v-btn @click="addCol(true)" small :disabled="!user.staff">Add OCR</v-btn>
          </v-layout>
          <div v-for="(cVal, cKey) in pageOptions.cols" :key="'cp' + cKey">
            <v-layout>
              <div class="colcount mr-2">{{ cKey + 1 }}</div>
              <v-layout row wrap>
                <v-flex xs12 md4 px-1><v-text-field v-model="cVal.x1" @input="inputFloatNumber(cVal, 'x1')" type="number" label="x1" placeholder="None" step="0.5" class="pt-0" :readonly="!user.staff"></v-text-field></v-flex>
                <v-flex xs12 md4 px-1><v-text-field v-model="cVal.x2" @input="inputFloatNumber(cVal, 'x2')" type="number" label="x2" placeholder="None" step="0.5" class="pt-0" :readonly="!user.staff"></v-text-field></v-flex>
                <v-flex xs12 md4 px-1 class="text-center">
                  Elements:<br>
                  {{ (100 / variantContent.length * getContentOfArea(variantContent, [{ x: cVal.x1, y: 0, width: cVal.x2 - cVal.x1, height: optionsOverlay.orgHeight }]).length).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) }} %</v-flex>
              </v-layout>
              <v-btn @click="splitCol(cKey)" color="blue" class="xsmall" fab small dark v-if="pageOptions.cols.length < 4" :disabled="!user.staff"><v-icon>mdi-arrow-split-vertical</v-icon></v-btn>
              <v-btn @click="delEntry(pageOptions.cols, cKey)" color="red" class="xsmall" fab small dark :disabled="!user.staff"><v-icon>delete</v-icon></v-btn>
            </v-layout>
          </div>
          <div v-if="pageOptions.cols.length > 0">
            Used elements in columns: <b :class="allColsContentCount !== variantContent.length ? 'red--text' : ''">{{ allColsContentCount.toLocaleString() }} / {{ variantContent.length.toLocaleString() }}</b>
          </div>
        </div>
        <div v-if="pageOptions && pageOptions.colsplitter">
          <v-layout mb-3>
            <h2><div class="colbox colsplitter"></div>Columns-Splitter</h2>
            <v-spacer />
            <v-btn @click="pageOptions.colsplitter.col = 0; pageOptions.colsplitter.y = pageOptions.variables[0].y - 1;" small :disabled="!user.staff || !(pageOptions.variables && pageOptions.variables.length > 0)">Set by Variant</v-btn>
          </v-layout>
          <v-layout row wrap>
            <v-flex xs12 md6 px-1><v-text-field v-model="pageOptions.colsplitter.col" @input="inputIntNumber(pageOptions.colsplitter, 'col')" type="number" label="col" placeholder="None" step="1" class="pt-0" :readonly="!user.staff"></v-text-field></v-flex>
            <v-flex xs12 md6 px-1><v-text-field v-model="pageOptions.colsplitter.y" @input="inputFloatNumber(pageOptions.colsplitter, 'y')" type="number" label="y" placeholder="None" step="0.5" class="pt-0" :readonly="!user.staff"></v-text-field></v-flex>
          </v-layout>
        </div>
        <v-btn @click="savePdfOptions" color="info" class="mt-3" :loading="loading" :disabled="loading || !user.staff">Save PDF options</v-btn>
      </div>
      <div v-else>
        Wait for OCR data!
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'EditDataPdfEditorOCR',
  props: ['selectedPdfFile', 'textContent', 'optionsOverlay', 'user', 'options', 'csrf'],
  data () {
    return {
      loading: false
    }
  },
  mounted () {
    console.log('EditDataPdfEditorOCR', this.selectedPdfFile)
    this.$nextTick(() => {
      if (this.textContent) {
        this.setInternalOcrData()
      }
    })
  },
  methods: {
    savePdfOptions () {
      console.log('savePdfOptions', this.selectedPdfFile)
      this.loading = true
      this.$http
        .post('/editData/', {
          set: 'setPdfOptions',
          data: JSON.stringify(this.selectedPdfFile)
        }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
        .then((response) => {
          this.loading = false
        })
        .catch((err) => {
          console.log(err)
          this.loading = false
        })
    },
    setInternalOcrData () {
      this.selectedPdfFile.internalOcrData.page = this.selectedPdfFile.localData.selectedPdfSite
      this.setInternalOcrDataBlocks()
      this.setInternalOcrVariable()
      console.log('internalOcrData', this.selectedPdfFile.internalOcrData)
    },
    setInternalOcrVariable () {
      if (this.textContent) {
        let aCont = this.getContentOfArea(this.textContent, this.pageOptions.ignore, true)
        this.selectedPdfFile.internalOcrData.variables = this.pageOptions.variables.map(v => {
          let vEl = this.getContentOfArea(aCont, [v])
          let aX = vEl.map(e => e.transform[4]).sort((a, b) => a - b)[0]
          let aY = vEl.map(e => e.transform[5]).sort((a, b) => a - b)[0]
          let objVarQuest = vEl.slice().sort((a, b) => b.transform[5] - a.transform[5])
          objVarQuest = objVarQuest.filter(vq => objVarQuest[0].transform[5] - 13 < vq.transform[5])
          objVarQuest = vEl.filter(e => objVarQuest.indexOf(e) > -1)
          let strVarQuest = objVarQuest.map(e => e.str).join('').trim()
          let strVarQuestMatch = strVarQuest.match(/^(\d{0,99})(.+)(\([^()]+\))$/)
          let strVariable = strVarQuestMatch && strVarQuestMatch[2] ? strVarQuestMatch[2].trim() : null
          let strQuestion = strVarQuestMatch && strVarQuestMatch[3] ? strVarQuestMatch[3].trim().substring(1, strVarQuestMatch[3].trim().length - 1) : null
          if (strQuestion) {
            strQuestion = strQuestion.replace('P0', 'PQ')
          }
          let strComment = vEl.filter(e => objVarQuest.indexOf(e) < 0).map(e => e.str).join('').trim()
          // console.log([strVarQuest, strVariable, strQuestion, strComment])
          return {
            strings: {
              id: strVarQuest,
              all: vEl.map(e => e.str).join('').trim(),
              variable: strVariable,
              question: strQuestion,
              comment: strComment
            },
            el: vEl,
            x: aX,
            y: aY,
            width: vEl.map(e => e.transform[4] + e.width).sort((a, b) => b - a)[0] - aX,
            height: vEl.map(e => e.transform[5] + e.transform[3]).sort((a, b) => b - a)[0] - aY
          }
        })
      }
    },
    setInternalOcrDataBlocks () {
      let aBlocks = []
      // Aus mehreren Spalten eine machen und alle Elemente sortieren
      let aRowData = []
      let aRow = 0
      let colList = []
      if (this.pageOptions.colsplitter && this.pageOptions.colsplitter.col > -1) {
        colList = [
          ...this.pageOptions.cols.filter((c, k) => k < this.pageOptions.colsplitter.col).map(c => { return {x: c.x1, y: 0, width: c.x2 - c.x1, height: this.optionsOverlay.orgHeight} }),
          ...this.pageOptions.cols.filter((c, k) => k >= this.pageOptions.colsplitter.col).map(c => { return {x: c.x1, y: this.pageOptions.colsplitter.y, width: c.x2 - c.x1, height: this.optionsOverlay.orgHeight - this.pageOptions.colsplitter.y} }),
          ...this.pageOptions.cols.filter((c, k) => k >= this.pageOptions.colsplitter.col).map(c => { return {x: c.x1, y: 0, width: c.x2 - c.x1, height: this.pageOptions.colsplitter.y} })
        ]
      } else {
        colList = this.pageOptions.cols.map(c => { return {x: c.x1, y: 0, width: c.x2 - c.x1, height: this.optionsOverlay.orgHeight} })
      }
      console.log('colList', colList)
      let cDg = 0
      colList.forEach(col => {
        let aColElements = this.getContentOfArea(this.variantContent, [{ x: col.x, y: col.y, width: col.width, height: col.height }])
        let yData = []
        let aColElData = aColElements.map(el => {
          yData.push(el.transform[5])
          return {
            orgEl: el,
            str: el.str,
            x: el.transform[4] - col.x1,
            y: el.transform[5],
            oX: el.transform[4],
            oY: el.transform[5],
            col: cDg,
            row: -1,
            width: el.width,
            height: el.transform[3]
          }
        })
        yData.sort((a, b) => a < b ? 1 : a > b ? -1 : 0)
        let lY = null
        yData = yData.filter(yD => {
          if (lY !== null && lY - yD < 3) {
            return false
          } else {
            lY = yD
            return true
          }
        })
        let rDg = -1
        yData = yData.map(yD => { rDg += 1; return {y: yD, row: rDg} })
        aColElData.forEach(el => {
          el.row = aRow + yData.filter(yD => ((el.y <= yD.y) && (yD.y - el.y < 3)))[0].row
        })
        aColElData.sort((a, b) => a.row < b.row ? -1 : a.row > b.row ? 1 : a.x < b.x ? -1 : a.x > b.x ? 1 : 0)
        aRowData = [...aRowData, ...aColElData]
        aRow += yData.length
        cDg += 1
      })
      console.log('aRowData', aRow, aRowData)
      // Zeilen zusammenfassen
      let elByRow = {}
      aRowData.forEach(rD => {
        if (!elByRow[rD.row]) {
          elByRow[rD.row] = {
            str: '',
            x1: Infinity,
            y1: Infinity,
            x2: -Infinity,
            y2: -Infinity,
            width: 0,
            height: 0,
            el: []
          }
        }
        if (elByRow[rD.row].x1 > rD.oX) {
          elByRow[rD.row].x1 = rD.oX
        }
        if (elByRow[rD.row].y1 > rD.oY) {
          elByRow[rD.row].y1 = rD.oY
        }
        if (elByRow[rD.row].x2 < (rD.oX + rD.width)) {
          elByRow[rD.row].x2 = rD.oX + rD.width
        }
        if (elByRow[rD.row].y2 < (rD.oY + rD.height)) {
          elByRow[rD.row].y2 = rD.oY + rD.height
        }
        elByRow[rD.row].width = elByRow[rD.row].x2 - elByRow[rD.row].x1
        elByRow[rD.row].height = elByRow[rD.row].y2 - elByRow[rD.row].y1
        elByRow[rD.row].str += rD.str
        elByRow[rD.row].el.push(rD)
      })
      elByRow = Object.keys(elByRow).map(erKey => elByRow[erKey])
      // console.log('elByRow', elByRow)
      // Zeilen zu zusammenhängende Informationen zusammenfügen
      let elByData = []
      let aElByData = []
      let nextData = false
      elByRow.forEach(erD => {
        if (aElByData.length > 0 && (/^[^\d]{2,}/.test(erD.str) || nextData)) {
          let aEl = aElByData.flatMap(ed => ed.el)
          elByData.push({
            str: aEl.map(e => e.str).join(''),
            x1: aElByData.map(e => e.x1).sort((a, b) => a - b)[0],
            y1: aElByData.map(e => e.y1).sort((a, b) => a - b)[0],
            x2: aElByData.map(e => e.x2).sort((a, b) => b - a)[0],
            y2: aElByData.map(e => e.y2).sort((a, b) => b - a)[0],
            el: aEl
          })
          aElByData = []
        }
        aElByData.push(erD)
        nextData = erD.str.toLowerCase().indexOf('cont\'d') > -1
      })
      if (aElByData.length > 0) {
        let aEl = aElByData.flatMap(ed => ed.el)
        elByData.push({
          str: aEl.map(e => e.str).join(''),
          x1: aElByData.map(e => e.x1).sort((a, b) => a - b)[0],
          y1: aElByData.map(e => e.y1).sort((a, b) => a - b)[0],
          x2: aElByData.map(e => e.x2).sort((a, b) => b - a)[0],
          y2: aElByData.map(e => e.y2).sort((a, b) => b - a)[0],
          el: aEl
        })
      }
      // console.log('elByData', elByData)
      // Information zu Place mit Variant/Informant umwandeln
      let getVarInfsBoxes = (aData) => {
        let aVarInfsBoxes = []
        let aVarInfsBoxesEl = []
        let aCol = null
        aData.forEach(beD => {
          beD.el.forEach(aEl => {
            if (aCol !== null && aEl.col !== aCol) {
              aVarInfsBoxes.push(aVarInfsBoxesEl)
              aVarInfsBoxesEl = []
            }
            aCol = aEl.col
            aVarInfsBoxesEl.push(aEl)
          })
        })
        aVarInfsBoxes.push(aVarInfsBoxesEl)
        aVarInfsBoxes = aVarInfsBoxes.map(beD => {
          let aX = beD.map(e => e.oX).sort((a, b) => a - b)[0]
          let aY = beD.map(e => e.oY).sort((a, b) => a - b)[0]
          return {
            x: aX,
            y: aY,
            width: beD.map(e => e.oX + e.width).sort((a, b) => b - a)[0] - aX,
            height: beD.map(e => e.oY + e.height).sort((a, b) => b - a)[0] - aY,
            col: beD[0].col
          }
        })
        return aVarInfsBoxes
      }
      let aPlace = null
      let aBlockElByData = []
      elByData.forEach(eD => {
        if (/^[^\d]+$/.test(eD.str) && !(/-\w+[^\d]{1,2}$/.test(eD.str.trim())) && eD.str.trim().length < 26) {
          if (aBlockElByData.length > 0) {
            let aData = [aPlace, ...aBlockElByData].filter(d => d !== null)
            let aX = aData.map(e => e.x1).sort((a, b) => a - b)[0]
            let aY = aData.map(e => e.y1).sort((a, b) => a - b)[0]
            aBlocks.push({
              place: aPlace,
              varInfs: aBlockElByData,
              varInfsBoxes: getVarInfsBoxes(aData),
              x: aX,
              y: aY,
              width: aData.map(e => e.x2).sort((a, b) => b - a)[0] - aX,
              height: aData.map(e => e.y2).sort((a, b) => b - a)[0] - aY
            })
          }
          aPlace = eD
          aBlockElByData = []
        } else {
          aBlockElByData.push(eD)
        }
      })
      if (aBlockElByData.length > 0) {
        let aData = [aPlace, ...aBlockElByData]
        let aX = aData.map(e => e.x1).sort((a, b) => a - b)[0]
        let aY = aData.map(e => e.y1).sort((a, b) => a - b)[0]
        aBlocks.push({
          place: aPlace,
          varInfs: aBlockElByData,
          varInfsBoxes: getVarInfsBoxes(aData),
          x: aX,
          y: aY,
          width: aData.map(e => e.x2).sort((a, b) => b - a)[0] - aX,
          height: aData.map(e => e.y2).sort((a, b) => b - a)[0] - aY
        })
      }
      // console.log('aBlocks', aBlocks)
      this.selectedPdfFile.internalOcrData.blocks = aBlocks
    },
    addVariable (ocr) {
      if (this.pageOptions && this.pageOptions.variables) {
        if (ocr) {
          this.pageOptions.variables = [...this.pageOptions.variables, ...this.variableGroup.map(vg => { return {x: vg.x, y: vg.y, width: vg.width, height: vg.height} })]
        } else {
          this.pageOptions.variables.push({x: 5, y: parseInt(this.optionsOverlay.orgHeight - 5), width: 10, height: 10})
        }
      }
    },
    addIgnore (ocr) {
      if (this.pageOptions && this.pageOptions.ignore) {
        if (ocr) {
          this.pageOptions.ignore = [...this.pageOptions.ignore, ...this.ignoreObjects.map(vg => { return {x: vg.x, y: vg.y, width: vg.width, height: vg.height} })]
        } else {
          this.pageOptions.ignore.push({x: 5, y: parseInt(this.optionsOverlay.orgHeight - 5), width: 10, height: 10})
        }
      }
    },
    addCol (ocr) {
      if (this.pageOptions && this.pageOptions.cols) {
        if (ocr) {
          this.pageOptions.cols = [...this.pageOptions.cols, ...this.variantCols.map(vg => { return {x1: vg.x1, x2: vg.x2} })]
        } else {
          this.pageOptions.cols.push({x1: 10, x2: 20})
        }
      }
    },
    splitCol (key) {
      if (this.pageOptions && this.pageOptions.cols && this.pageOptions.cols[key] && confirm('Really split column?')) {
        let aCol = this.pageOptions.cols[key]
        let nCol = { x1: aCol.x1 + (aCol.x2 - aCol.x1) / 2 + 1, x2: aCol.x2 }
        aCol.x2 = aCol.x1 + (aCol.x2 - aCol.x1) / 2 - 1
        this.pageOptions.cols.push(nCol)
      }
    },
    sortCols () {
      this.pageOptions.cols.sort((a, b) => { return a.x1 < b.x1 ? -1 : (a.x1 > b.x1 ? 1 : 0) })
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
    },
    delEntry (val, key) {
      if (Array.isArray(val) && key > -1 && confirm('Really delete?')) {
        val.splice(key, 1)
      }
    },
    getContentOfArea (tc, bounderies, ignore = false) {
      let tcList = []
      tc.forEach(tc => {
        let isInIt = false
        bounderies.forEach(i => {
          if (tc.transform[4] >= i.x && tc.transform[4] <= i.x + i.width && tc.transform[5] >= i.y && tc.transform[5] <= i.y + i.height) {
            isInIt = true
          }
        })
        if (isInIt !== ignore) {
          tcList.push(tc)
        }
      })
      return tcList
    }
  },
  computed: {
    pageOptions () {
      return this.selectedPdfFile.page_options[this.selectedPdfFile.localData.selectedPdfSite]
    },
    allColsContentCount () {
      let aCount = 0
      this.pageOptions.cols.forEach(c => {
        aCount += this.getContentOfArea(this.variantContent, [{ x: c.x1, y: 0, width: c.x2 - c.x1, height: this.optionsOverlay.orgHeight }]).length
      })
      return aCount
    },
    variantCols () {
      console.log(this.textContent.length, this.variantContent.length, this.variantContent)
      if (this.variantContent) {
        let mergeCols = (cols) => {
          let oLen = cols.length
          cols.forEach(aC => {
            cols.forEach(bC => {
              if (aC !== bC && !aC.del && !bC.del && ((aC.x1 >= bC.x1 && aC.x1 <= bC.x2) || (aC.x2 >= bC.x1 && aC.x2 <= bC.x2))) {
                if (bC.x1 < aC.x1) {
                  aC.x1 = bC.x1
                }
                if (bC.x2 > aC.x2) {
                  aC.x2 = bC.x2
                }
                bC.del = true
              }
            })
          })
          cols = cols.filter(c => !c.del)
          while (oLen !== cols.length) {
            oLen = cols.length
            cols = mergeCols(cols)
          }
          return cols
        }
        var aCols = []
        this.variantContent.forEach(vc => {
          let newCol = true
          aCols.some(c => {
            if (
              (vc.transform[4] >= c.x1 && vc.transform[4] <= c.x2) ||
              (vc.transform[4] + vc.width >= c.x1 && vc.transform[4] + vc.width <= c.x2)
            ) {
              if (vc.transform[4] < c.x1) {
                c.x1 = vc.transform[4]
              }
              if (vc.transform[4] + vc.width > c.x2) {
                c.x2 = vc.transform[4] + vc.width
              }
              newCol = false
              return true
            }
          })
          if (newCol) {
            aCols.push({x1: vc.transform[4], x2: vc.transform[4] + vc.width})
          } else if (aCols.length > 0) {
            aCols = mergeCols(aCols)
          }
        })
        if (aCols.length > 0) {
          return aCols
        }
      }
      return []
    },
    variantContent () {
      if (this.textContent) {
        let ignoreList = [...(this.pageOptions.variables ? this.pageOptions.variables : []), ...(this.pageOptions.ignore ? this.pageOptions.ignore : [])]
        return this.getContentOfArea(this.textContent, ignoreList, true)
      }
      return []
    },
    ignoreObjects () {
      if (this.textContent) {
        let maxY = Infinity
        let maxObj = null
        this.textContent.forEach(i => {
          if (i.transform[5] < maxY) {
            maxY = i.transform[5]
            maxObj = i
          }
        })
        if (maxObj) {
          // console.log([{x: maxObj.transform[4], y: maxObj.transform[5], width: maxObj.width, height: maxObj.transform[3]}])
          return [{x: maxObj.transform[4], y: maxObj.transform[5], width: maxObj.width, height: maxObj.transform[3]}]
        }
      }
      return []
    },
    variableGroup () {
      if (this.textGroupedBySize) {
        let aVariableGroup = { textGroups: [], allTextElements: [], x: 0, y: 0, width: 10, height: 10 }
        this.textGroupedBySize.forEach(tg => {
          if (tg.size >= 9) {
            let tgClean = tg.text.trim().replace(/[0-9,.;-_:]/g, '')
            // console.log(tgClean)
            if (tgClean.length > 2) {
              aVariableGroup.textGroups.push(tg)
            }
          }
        })
        aVariableGroup.allTextElements = aVariableGroup.textGroups.flatMap(tg => tg.list)
        if (aVariableGroup.allTextElements.length > 0) {
          let minX = Infinity
          let minY = Infinity
          let maxX = -Infinity
          let maxY = -Infinity
          aVariableGroup.allTextElements.forEach(at => {
            if (at.transform[4] < minX) {
              minX = at.transform[4]
            }
            if (at.transform[4] + at.width > maxX) {
              maxX = at.transform[4] + at.width
            }
            if (at.transform[5] < minY) {
              minY = at.transform[5]
            }
            if (at.transform[5] - at.transform[3] > maxY) {
              maxY = at.transform[5] + at.transform[3]
            }
          })
          aVariableGroup.x = minX
          aVariableGroup.y = minY
          aVariableGroup.width = maxX - minX
          aVariableGroup.height = maxY - minY
        }
        if (aVariableGroup.width > 100 && aVariableGroup.height > 5) {
          // console.log(aVariableGroup)
          return [aVariableGroup]
        }
      }
      return []
    },
    textGroupedBySize () {
      if (this.textContent) {
        let lSize = -Infinity
        let aTextGroupedBySize = []
        let aTextItems = { size: -Infinity, list: [] }
        this.textContent.forEach(i => {
          if (lSize !== i.transform[3]) {
            lSize = i.transform[3]
            if (aTextItems.list.length > 0) {
              aTextItems.text = aTextItems.list.map(i => i.str).join('')
              aTextGroupedBySize.push(aTextItems)
            }
            aTextItems = { size: i.transform[3], list: [], text: '' }
          }
          aTextItems.list.push(i)
        })
        aTextItems.text = aTextItems.list.map(i => i.str).join('')
        aTextGroupedBySize.push(aTextItems)
        // console.log(aTextGroupedBySize)
        return aTextGroupedBySize
      }
      return null
    }
  },
  watch: {
    'textContent' (nVal) {
      // console.log('textContent', nVal)
      if (nVal) {
        if (!this.selectedPdfFile.page_options[this.selectedPdfFile.localData.selectedPdfSite]) {
          this.$set(this.selectedPdfFile.page_options, this.selectedPdfFile.localData.selectedPdfSite, {})
        }
        let aOpt = this.selectedPdfFile.page_options[this.selectedPdfFile.localData.selectedPdfSite]
        if (!aOpt.variables) {
          this.$set(aOpt, 'variables', this.variableGroup.map(vg => { return {x: vg.x, y: vg.y, width: vg.width, height: vg.height} }))
        }
        if (!aOpt.ignore) {
          this.$set(aOpt, 'ignore', this.ignoreObjects.map(vg => { return {x: vg.x, y: vg.y, width: vg.width, height: vg.height} }))
        }
        if (!aOpt.cols) {
          this.$set(aOpt, 'cols', this.variantCols.map(vg => { return {x1: vg.x1, x2: vg.x2} }))
        }
        if (!aOpt.colsplitter) {
          this.$set(aOpt, 'colsplitter', {col: -1, y: 300})
        }
        this.sortCols()
        this.setInternalOcrData()
      }
      console.log('pageOptions', this.pageOptions)
    }
  }
}
</script>

<style scoped>
.colbox {
  display: inline-block;
  width: 15px;
  height: 15px;
  margin-right: 0.5rem;
  border: 1px solid #f00;
  background-color: rgba(255,0,0,0.1)
}
.colbox.variable {
  border: 1px solid #00f;
  background-color: rgba(0,0,255,0.1)
}
.colbox.col {
  border: 1px solid #ff0;
  background-color: rgba(255,255,0,0.1)
}
.colbox.ignore {
  border: 1px solid #f00;
  background-color: rgba(255,0,0,0.1)
}
.colbox.colsplitter {
  border: 1px solid #f0f;
  background-color: rgba(255,0,255,0.1)
}
.colcount {
  width: 1.5rem;
  height: 1.5rem;
  min-width: 1.5rem;
  text-align: center;
  border: 1px solid #000;
  line-height: 1.4rem;
  border-radius: 100%;
}
.v-btn.xsmall {
  width: 28px;
  height: 28px;
}
.v-btn.xsmall .v-icon {
  font-size: 17px;
}
.alert-icon {
  position: relative;
  top: -4px;
  margin-left: 0.5rem;
}
</style>
