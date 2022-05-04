<template>
  <div class="pdf-page white elevation-2 my-3 grow">
    <v-layout class="h-100" align-center justify-center v-if="loading">
      <v-progress-circular :rotate="-90" :size="100" :width="15" :value="progress * 100" color="primary" class="vpc-loading">
        {{ (progress * 100).toLocaleString(undefined, {minimumFractionDigits: 1, maximumFractionDigits: 1}) }}
      </v-progress-circular>
    </v-layout>
    <Split style="min-height: 500px" v-else-if="options.edit.data" @onDragEnd="onDragEnd">
      <SplitArea :size="options.edit.data.panelWidth[0]" :minSize="200">
        <div class="layout justify-start column fill-height p-relative">
          <div class="scroll flex">
            <div id="pdf-overview" :class="{'pdf-frame': true, 'show-text': pdfImageText, 'rendering': pageRendering}">
              <canvas id="pdf-overview-canvas" :style="'filter:contrast(' + selectedPdfFile.options.contrast + ')brightness(' + selectedPdfFile.options.brightness + ');'"/>
              <div id="pdf-overview-text-overlay" :class="'textLayer' + (selectedPdfFile.options.showOCRElements ? ' show-elements' : '')"></div>
              <div class="pdf-options-overlayer" :style="'left:' + (optionsOverlay.x) + 'px;top:' + (optionsOverlay.y) + 'px;'" v-if="selectedPdfFile.options.showOCR && !pageRendering && pageOptions">
                <template v-if="pageOptions && pageOptions.cols && pageOptions.cols.length > 0">
                  <div class="box col"
                    :style="'left:' + (cvVal.x1 * optionsOverlay.xFac) + 'px;top:-2px;width:' + ((cvVal.x2 - cvVal.x1) * optionsOverlay.xFac) + 'px;height:99%;'"
                    v-for="(cvVal, vcKey) in pageOptions.cols" :key="'vC' + vcKey"
                  ></div>
                </template>
                <template v-if="pageOptions.variables && pageOptions.variables.length > 0">
                  <div class="box variable"
                    :style="'left:' + ((vVal.x) * optionsOverlay.xFac) + 'px;top:' + (optionsOverlay.height + (vVal.y + vVal.height) * optionsOverlay.yFac) + 'px;width:' + (vVal.width * optionsOverlay.xFac) + 'px;height:' + (vVal.height * -optionsOverlay.yFac) + 'px;'"
                    v-for="(vVal, vKey) in pageOptions.variables" :key="'vg' + vKey"
                    @mouseover="ocrVariableHover = vKey"
                    @mouseleave="ocrVariableHover = null"
                    @click="clickVariable(vKey)"
                  ></div>
                </template>
                <template v-if="pageOptions.ignore && pageOptions.ignore.length > 0">
                  <div class="box ignore"
                    :style="'left:' + ((iVal.x) * optionsOverlay.xFac) + 'px;top:' + (optionsOverlay.height + (iVal.y + iVal.height) * optionsOverlay.yFac) + 'px;width:' + (iVal.width * optionsOverlay.xFac) + 'px;height:' + (iVal.height * -optionsOverlay.yFac) + 'px;'"
                    v-for="(iVal, iKey) in pageOptions.ignore" :key="'iO' + iKey"
                  ></div>
                </template>
                <template v-if="selectedPdfFile.internalOcrData && selectedPdfFile.internalOcrData.page === selectedPdfFile.localData.selectedPdfSite && selectedPdfFile.internalOcrData.blocks.length > 0">
                  <template v-for="(bVal, bKey) in selectedPdfFile.internalOcrData.blocks">
                    <div :class="'box block' + (ocrBlockObj === bVal ? ' selected' : '')"
                      :data-block="bKey"
                      :style="'left:' + ((bbVal.x) * optionsOverlay.xFac) + 'px;top:' + (optionsOverlay.height + (bbVal.y + bbVal.height) * optionsOverlay.yFac) + 'px;width:' + (bbVal.width * optionsOverlay.xFac) + 'px;height:' + (bbVal.height * -optionsOverlay.yFac) + 'px;'"
                      v-for="(bbVal, bbKey) in bVal.varInfsBoxes" :key="'b' + bKey + 'b' + bbKey"
                      :title="'Place: ' + (bVal.place && bVal.place.str ? bVal.place.str : 'Unbekannt!')"
                      @mouseover="ocrBlockHover = bKey"
                      @mouseleave="ocrBlockHover = null"
                      @click="clickBlock(bKey, bbKey)"
                    ></div>
                    <template v-if="bVal.place">
                      <div class="box place"
                        :style="'left:' + ((pVal.oX) * optionsOverlay.xFac) + 'px;top:' + (optionsOverlay.height + (pVal.oY + pVal.height) * optionsOverlay.yFac) + 'px;width:' + (pVal.width * optionsOverlay.xFac) + 'px;height:' + (pVal.height * -optionsOverlay.yFac) + 'px;'"
                        v-for="(pVal, pKey) in bVal.place.el" :key="'b' + bKey + 'p' + pKey"
                      ></div>
                    </template>
                    <template v-if="selectedPdfFile.options.showVarInfs || bKey === ocrBlockHover">
                      <div class="box varinfs"
                        :style="'left:' + ((bvVal.oX) * optionsOverlay.xFac) + 'px;top:' + (optionsOverlay.height + (bvVal.oY + bvVal.height) * optionsOverlay.yFac) + 'px;width:' + (bvVal.width * optionsOverlay.xFac) + 'px;height:' + (bvVal.height * -optionsOverlay.yFac) + 'px;'"
                        v-for="(bvVal, bvKey) in bVal.varInfs.flatMap(vi => vi.el)" :key="'b' + bKey + 'v' + bvKey"
                      ></div>
                    </template>
                  </template>
                </template>
                <template v-if="pageOptions.colsplitter && pageOptions.colsplitter.col > -1">
                  <div class="box colsplitter"
                    :style="'left:' + ((pageOptions.cols[pageOptions.colsplitter.col] ? pageOptions.cols[pageOptions.colsplitter.col].x1 : 0) * optionsOverlay.xFac) + 'px;top:' + (optionsOverlay.height + pageOptions.colsplitter.y * optionsOverlay.yFac) + 'px;width:auto;height:3px;right:10px;'"
                  ></div>
                </template>
              </div>
            </div>
            <v-slider
              v-model="views[0].zoom"
              thumb-label
              :step="0.05"
              :min="0.5"
              :max="5"
              class="slider"
            ></v-slider>
          </div>
        </div>
      </SplitArea>
      <SplitArea :size="options.edit.data.panelWidth[1]" class="d-flex layout column" :minSize="400">
        <v-tabs v-model="colTab" grow :hide-slider="colTab < 1" class="form-tab layout justify-start column" style="height: auto;" color="blue lighten-5" v-if="pageOptions && pageOptions.cols && pageOptions.cols.length > 0">
          <v-tab style="max-width:1px;"></v-tab>
          <v-tab v-for="(cvVal, vcKey) in pageOptions.cols" :key="'vcT' + vcKey">{{ vcKey + 1 }}</v-tab>
        </v-tabs>
        <div class="layout justify-start column fill-height p-relative">
          <div class="scroll flex" ref="prevScroll" @scroll="pdfPrevScroll">
            <div id="pdf-zoom" :class="{'pdf-frame': true, 'show-text': pdfImageText}">
              <canvas id="pdf-zoom-canvas" :style="'filter:contrast(' + selectedPdfFile.options.contrast + ')brightness(' + selectedPdfFile.options.brightness + ');'"/>
              <div id="pdf-zoom-text-overlay" class="textLayer"></div>
              <div class="pdf-preview-overlayer" :style="'left:' + (optionsPreview.x) + 'px;top:' + (optionsPreview.y) + 'px;'" v-if="selectedPdfFile.options.showOCR && !pageRendering && pageOptions">
                <template v-if="ocrBlockObj">
                  <div class="box block"
                    :style="'left:' + ((bbVal.x - 5) * optionsPreview.xFac) + 'px;top:' + (optionsPreview.height + (bbVal.y + 5 + bbVal.height) * optionsPreview.yFac) + 'px;width:' + ((bbVal.width + 10) * optionsPreview.xFac) + 'px;height:' + ((bbVal.height + 10) * -optionsPreview.yFac) + 'px;'"
                    v-for="(bbVal, bbKey) in ocrBlockObj.varInfsBoxes" :key="'pb' + bbKey"
                  ></div>
                </template>
              </div>
            </div>
            <v-slider
              v-model="views[1].zoom"
              thumb-label
              :step="0.05"
              :min="0.5"
              :max="5"
              class="slider"
            ></v-slider>
          </div>
        </div>
      </SplitArea>
      <SplitArea :size="options.edit.data.panelWidth[2]" :minSize="400">
        <div>
          <v-tabs v-model="formTab" fixed-tabs class="form-tab layout justify-start column fill-height" color="blue lighten-5">
            <v-tab>PDF</v-tab>
            <v-tab-item>
              <EditDataPdfEditorOptions
                :selectedPdfFile="selectedPdfFile"
                :pdfImageText="pdfImageText" @changePdfImageText="changePdfImageText"
                :defaultOptions="defaultOptions"
                :user="user" :options="options" :csrf="csrf"
              />
            </v-tab-item>
            <v-tab title="Staff only">OCR</v-tab>
            <v-tab-item>
              <EditDataPdfEditorOCR
                :selectedPdfFile="selectedPdfFile"
                :textContent="textContent"
                :optionsOverlay="optionsOverlay"
                :user="user" :options="options" :csrf="csrf"
              />
            </v-tab-item>
            <v-tab>Data</v-tab>
            <v-tab-item>
              <EditDataPdfEditorData
                @unselectVariable="ocrVariableSelected=null"
                :selectedPdfFile="selectedPdfFile"
                :baseData="baseData"
                :ocrVariableSelected="ocrVariableSelected"
                :ocrBlockObj="ocrBlockObj"
                :user="user" :options="options" :csrf="csrf"
              />
            </v-tab-item>
          </v-tabs>
        </div>
      </SplitArea>
    </Split>
  </div>
</template>

<script>
/* global pdfjsLib TextLayerBuilder */
import _ from 'lodash'
import EditDataPdfEditorOptions from './EditDataPdfEditorOptions.vue'
import EditDataPdfEditorOCR from './EditDataPdfEditorOCR.vue'
import EditDataPdfEditorData from './EditDataPdfEditorData.vue'

export default {
  name: 'EditDataPdfEditor',
  props: ['selectedPdfFile', 'pdfPath', 'baseData', 'user', 'options', 'csrf'],
  data () {
    return {
      maxPdfSite: 1,
      formTab: 0,
      colTab: 0,
      pdfImageText: false,
      pdfObj: null,
      loading: true,
      pageRendering: false,
      progress: 0,
      defaultOptions: {
        brightness: 1,
        contrast: 1,
        showOCR: true,
        showOCRElements: false,
        showVarInfs: false
      },
      optionsOverlay: {
        x: 0,
        y: 0,
        width: 100,
        height: 100,
        xFac: 1,
        yFac: -1,
        orgWidth: 100,
        orgHeight: 100
      },
      optionsPreview: {
        x: 0,
        y: 0,
        width: 100,
        height: 100,
        xFac: 1,
        yFac: -1
      },
      textContent: null,
      ocrBlockHover: null,
      ocrBlockObj: null,
      ocrVariableHover: null,
      ocrVariableSelected: null,
      views: [
        {canvas: 'pdf-overview-canvas', textOverlay: 'pdf-overview-text-overlay', zoom: 0.95},
        {canvas: 'pdf-zoom-canvas', textOverlay: 'pdf-zoom-text-overlay', zoom: 3.8}
      ],
      viewsLastZoom: [0.95, 3.8]
    }
  },
  mounted () {
    if (!this.selectedPdfFile.localData) {
      this.$set(this.selectedPdfFile, 'localData', {
        selectedPdfSite: 1,
        maxPdfSite: 1
      })
    }
    if (!this.selectedPdfFile.options) {
      this.$set(this.selectedPdfFile, 'options', {})
    }
    if (!this.selectedPdfFile.page_options) {
      this.$set(this.selectedPdfFile, 'page_options', {})
    }
    if (!this.selectedPdfFile.internalOcr) {
      this.$set(this.selectedPdfFile, 'internalOcrData', {
        page: 0,
        blocks: [],
        variables: []
      })
    }
    Object.keys(this.defaultOptions).forEach(aKey => {
      if (!this.selectedPdfFile.options[aKey]) {
        this.$set(this.selectedPdfFile.options, aKey, this.defaultOptions[aKey])
      }
    })
    if (this.selectedPdfFile.edit_data) {
      this.formTab = (!this.selectedPdfFile.page_options[this.selectedPdfFile.localData.selectedPdfSite]) ? 1 : 2
    }
    console.log('selectedPdfFile', this.selectedPdfFile)
    this.debouncedInitPdfFile()
  },
  computed: {
    pageOptions () {
      return this.selectedPdfFile.page_options[this.selectedPdfFile.localData.selectedPdfSite]
    }
  },
  methods: {
    clickBlock (bKey, bbKey) {
      this.ocrBlockObj = this.selectedPdfFile.internalOcrData.blocks[bKey] === this.ocrBlockObj ? null : this.selectedPdfFile.internalOcrData.blocks[bKey]
      if (this.ocrBlockObj) {
        this.colTab = this.ocrBlockObj.varInfsBoxes[bbKey].col + 1
        this.$refs.prevScroll.scrollTop = this.optionsPreview.height + (this.ocrBlockObj.varInfsBoxes[bbKey].y + this.ocrBlockObj.varInfsBoxes[bbKey].height + 8) * this.optionsPreview.yFac
        // console.log('clickBlock', bbKey, (this.ocrBlockObj.place && this.ocrBlockObj.place.str ? this.ocrBlockObj.place.str : 'Unbekannt!'), this.ocrBlockObj.varInfs.map(vi => vi.el.map(e => e.str).join('').trim()), this.ocrBlockObj)
      } else {
        // console.log('clickBlock - unselect', bKey, bbKey)
      }
    },
    clickVariable (vKey) {
      let vVal = this.selectedPdfFile.internalOcrData.variables[vKey]
      this.ocrVariableSelected = vVal
      this.formTab = 2
      console.log('clickVariable', [vVal.strings.id, vVal.strings.variable, vVal.strings.question, vVal.strings.comment, vVal.strings.all], vVal)
    },
    pdfPrevScroll (e) {
      if (this.pageOptions.cols && this.pageOptions.cols.length > 0) {
        let sCenter = e.target.scrollLeft + e.target.clientWidth / 2
        this.colTab = 0
        let cDg = 0
        this.pageOptions.cols.forEach(c => {
          if (sCenter > this.optionsPreview.x + c.x1 * this.optionsPreview.xFac && sCenter < this.optionsPreview.x + c.x2 * this.optionsPreview.xFac) {
            this.colTab = cDg + 1
          }
          cDg += 1
        })
        // console.log('pdfPrevScroll', sCenter)
      }
    },
    changePdfImageText (nVal) {
      this.pdfImageText = nVal
    },
    onDragEnd (size) {
      this.options.edit.data.panelWidth = size
    },
    debouncedInitPdfFile: _.debounce(function () {
      this.initPdfFile()
    }, 150),
    initPdfFile () {
      this.selectedPdfFile.localData.selectedPdfSite = 1
      this.selectedPdfFile.localData.maxPdfSite = 0
      this.textContent = null
      var vThis = this
      console.log(this.selectedPdfFile)
      this.loading = true
      var loadingTask = pdfjsLib.getDocument(this.pdfPath + this.selectedPdfFile.filename)
      console.log(loadingTask)
      loadingTask.onProgress = function (p) {
        vThis.progress = p.loaded / p.total
      }
      loadingTask.promise.then(function (pdf) {
        vThis.loading = false
        console.log('pdf loadingTask', vThis.selectedPdfFile.localData.maxPdfSite, pdf.numPages)
        vThis.selectedPdfFile.localData.maxPdfSite = pdf.numPages
        vThis.pdfObj = pdf
        vThis.debouncedRenderCurrentPage()
      }, function (reason) {
        // PDF loading error
        console.error(reason)
      })
    },
    renderCurrentPage (s) {
      console.log('renderCurrentPage', s)
      if (!this.pageRendering) {
        this.pageRendering = true
        this.textContent = null
        var vThis = this
        this.pdfObj.getPage(this.selectedPdfFile.localData.selectedPdfSite).then(function (page) {
          console.log('Page loaded', page)
          let aViews = vThis.views
          if (typeof s === 'number') {
            aViews = [aViews[s]]
          }
          aViews.forEach(function (aView) {
            var viewport = page.getViewport(aView.zoom)
            var canvas = document.getElementById(aView.canvas)
            var context = canvas.getContext('2d')
            canvas.height = viewport.height
            canvas.width = viewport.width
            var renderContext = {
              canvasContext: context,
              viewport: viewport
            }
            if (aView.canvas === 'pdf-overview-canvas') {
              vThis.optionsOverlay.x = viewport.transform[4]
              vThis.optionsOverlay.y = viewport.transform[5] - viewport.height
              vThis.optionsOverlay.width = viewport.width
              vThis.optionsOverlay.height = viewport.height
              vThis.optionsOverlay.xFac = viewport.transform[0]
              vThis.optionsOverlay.yFac = viewport.transform[3]
              vThis.optionsOverlay.orgWidth = page.view[2] - page.view[0]
              vThis.optionsOverlay.orgHeight = page.view[3] - page.view[1]
              // console.log('page', page.view, vThis.optionsOverlay.orgWidth, vThis.optionsOverlay.orgHeight)
              // console.log('viewport', viewport)
            } else {
              vThis.optionsPreview.x = viewport.transform[4]
              vThis.optionsPreview.y = viewport.transform[5] - viewport.height
              vThis.optionsPreview.width = viewport.width
              vThis.optionsPreview.height = viewport.height
              vThis.optionsPreview.xFac = viewport.transform[0]
              vThis.optionsPreview.yFac = viewport.transform[3]
              console.log('optionsPreview', vThis.optionsPreview)
            }
            var renderTask = page.render(renderContext)
            renderTask.then(function () {
              return page.getTextContent()
            }).then(function (textContent) {
              var textLayerDiv = document.getElementById(aView.textOverlay)
              textLayerDiv.innerHTML = ''
              var textLayer = new TextLayerBuilder({
                textLayerDiv: textLayerDiv,
                pageIndex: page.pageIndex,
                viewport: viewport
              })
              textLayer.setTextContent(textContent)
              textLayer.render()
            })
            renderTask.promise.then(function () {
              if (aView.canvas === 'pdf-overview-canvas') {
                page.getTextContent().then(function (txt) {
                  vThis.textContent = txt.items
                })
              }
              vThis.pageRendering = false
              console.log('Page rendered')
            })
          }, this)
        })
      } else {
        this.debouncedRenderCurrentPage()
      }
    },
    debouncedRenderCurrentPage: _.debounce(function (s) {
      this.renderCurrentPage(s)
    }, 50),
    debouncedSlowRenderCurrentPage: _.debounce(function (s) {
      this.renderCurrentPage(s)
    }, 500)
  },
  watch: {
    colTab (nVal) {
      if (nVal > 0 && this.pageOptions.cols && this.pageOptions.cols.length > 0) {
        let aCol = this.pageOptions.cols[nVal - 1]
        if (aCol) {
          let x1 = this.optionsPreview.x + aCol.x1 * this.optionsPreview.xFac
          let x2 = this.optionsPreview.x + aCol.x2 * this.optionsPreview.xFac
          // console.log(x1, x2, x1 + (x2 - x1) / 2, this.$refs.prevScroll.clientWidth / 2, x1 + (x2 - x1) / 2 - this.$refs.prevScroll.clientWidth / 2)
          this.$refs.prevScroll.scrollLeft = x1 + (x2 - x1) / 2 - this.$refs.prevScroll.clientWidth / 2
        }
      }
    },
    formTab (nVal) {
      if (nVal > 0) {
        this.pdfImageText = false
      }
    },
    'selectedPdfFile.localData.selectedPdfSite' () {
      if (!this.loading) {
        this.colTab = 0
        this.ocrBlockObj = null
        this.ocrVariableSelected = null
        this.$nextTick(() => {
          if (this.$refs.prevScroll) {
            this.$refs.prevScroll.scrollTop = 0
            this.$refs.prevScroll.scrollLeft = 0
          }
        })
        this.debouncedRenderCurrentPage()
        if (!this.selectedPdfFile.page_options[this.selectedPdfFile.localData.selectedPdfSite]) {
          this.formTab = 1
        }
      }
    },
    views: {
      handler () {
        for (let i = 0; i < 2; i++) {
          if (this.viewsLastZoom[i] !== this.views[i].zoom) {
            this.viewsLastZoom[i] = this.views[i].zoom
            this.debouncedSlowRenderCurrentPage(i)
          }
        }
      },
      deep: true
    }
  },
  components: {
    EditDataPdfEditorOptions,
    EditDataPdfEditorOCR,
    EditDataPdfEditorData
  }
}
</script>

<style scoped>
  .split > div {
    height: 100%;
  }
  .scroll-y, .form-tab >>> .v-window {
    max-height: 100%;
    overflow-x: hidden;
    overflow-y: auto;
    flex: 1 0 0;
  }
  .scroll {
    max-height: 100%;
    overflow: auto;
    flex: 1 0 0;
  }
  #pdf-overview, #pdf-zoom {
    display: table;
    position: relative;
    opacity: 1;
  }
  #pdf-overview.rendering {
    opacity: 0.5;
  }
  #pdf-canvas {
    display: block;
    border: none;
    width: auto;
    height: auto;
    max-width: 100%;
    max-height: 100%;
    margin: auto auto;
    padding: 0;
  }
  .zeile >>> .v-input {
    margin-top: 0;
  }
  .zeile-input-fx >>> .v-input__slot {
    margin-bottom: 4px;
  }
  .pdf-frame.show-text > canvas {
    opacity: 0;
  }
  .pdf-frame.show-text > .textLayer {
    opacity: 1!important;
  }
  .pdf-frame.show-text >>> .textLayer > div {
    color: #000!important;
  }
  .textLayer.show-elements >>> div {
    border: 1px solid #000;
  }
  .zeile >>> .v-input__append-inner {
    display: none;
  }
  .zeile:hover >>> .v-input__append-inner {
    display: -webkit-inline-box;
    display: -ms-inline-flexbox;
    display: inline-flex;
  }
  .vpc-loading >>> .v-progress-circular__overlay {
    -webkit-transition: none;
    transition: none;
  }
  .pdf-options-overlayer, .pdf-preview-overlayer {
    position: absolute;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;
    overflow: hidden;
    pointer-events: none;
  }
  .pdf-options-overlayer .box, .pdf-preview-overlayer .box {
    position: absolute;
    left: 10px;
    top: 10px;
    width: 10px;
    height: 10px;
    border: 1px solid #f00;
    background-color: rgba(255,0,0,0.1);
  }
  .pdf-preview-overlayer .box {
    border: 1px solid #0f0;
    border-left-width: 10px;
    margin-left: -5px;
    background-color: transparent;
  }
  .pdf-options-overlayer .box.variable {
    border: 1px solid #00f;
    background-color: rgba(0,0,255,0.1);
    pointer-events: all;
    cursor: pointer;
  }
  .pdf-options-overlayer .box.col {
    border: 1px solid #ff0;
    background-color: rgba(255,255,0,0.1);
  }
  .pdf-options-overlayer .box.colsplitter {
    border: 1px solid #f0f;
    background-color: rgba(255,0,255,0.1);
  }
  .pdf-options-overlayer .box.ignore {
    border: 1px solid #f00;
    background-color: rgba(255,0,0,0.1);
  }
  .pdf-options-overlayer .box.block {
    border: 1px solid #0f0;
    background-color: rgba(0,255,0,0.2);
    opacity: 0.3;
    pointer-events: all;
    cursor: pointer;
  }
  .pdf-options-overlayer .box.block.selected {
    opacity: 1;
  }
  .pdf-options-overlayer .box.place {
    border: 1px solid #00f;
    background-color: rgba(0,0,255,0.1);
  }
  .pdf-options-overlayer .box.varinfs {
    border: 1px solid #f0f;
    background-color: rgba(255,0,255,0.1);
  }
  .slider {
    position: absolute;
    bottom: 2rem;
    left: 10%;
    width: 80%;
  }
  .slider >>> .v-messages {
    display: none;
  }
  .slider >>> .v-input__slot {
    margin-bottom: 0;
  }
</style>
