<template>
  <div id="diagrammframe">
    <svg id="diagrammsvg" ref="diagrammSVG" v-on:mousedown="startDrag" v-on:mousemove="drag" v-on:mouseup="endDrag" v-on:mouseleave="endDrag">
      <defs>
      </defs>
      <g id="svg-g-workspace" ref="workspace" :transform="'translate(' + posX + ',' + posY + ')scale(' + scale + ',' + scale + ')'">
        <g class="svg-g-db-fk-links">
          <g class="svg-g-db-fk-link"
            v-for="(fkLink, key) in foreignKeyLinks" :key="'fkl' + key">
            <path :d="getPathForeignKeyLinks(fkLink)"/>
          </g>
        </g>
        <g class="svg-g-db-models">
          <g class="svg-g-db-model" ref="modelGroup"
            :transform="'translate(' + model.xt + ',' + model.yt + ')'"
            v-for="(model, key) in dbModels" :key="'dbm' + key">
            <rect class="bg" x="0" y="0" :width="(model.svgSet ? model.svgTxtMaxWidth + 10 : 99)" :height="28 + model.fields.length * 20 + 4" />
            <g class="db-model-title" :title="getTitle({'verbose_name': model.verbose_name, 'app': model.app, 'model': model.model, 'db_table': model.db_table})">
              <rect x="0" y="0" :width="(model.svgSet ? model.svgTxtMaxWidth + 10 : 99)" height="28" ref="modelTitleRect" />
              <text ref="modelTitleTxt" transform="translate(5,5)">{{ model.model }} ({{ model.count }})</text>
            </g>
            <g class="db-model-fields" transform="translate(0,30)">
              <g :class="{'db-model-field': true, 'pk': field.pk, 'showInfo': (fieldInformations != null && fieldInformations.field == field)}"
                :title="getTitle(field)"
                :transform="'translate(0,' + (key2 * 20) + ')'"
                @click="fieldInformations = {model: model, field: field}"
                v-for="(field, key2) in model.fields" :key="'dbm' + key + '-f' + key2">
                <rect x="0" y="0" :width="(model.svgSet ? model.svgTxtMaxWidth + 10 : 99)" height="19" />
                <text :ref="'modelFieldTxt' + key" transform="translate(5,0)">{{ field.related_db_table ? '> ' : '' }}{{ field.field_name }}{{ !field.blank || field.blank === 'false' ? ' *' : '' }}</text>
              </g>
            </g>
            <rect class="frm" x="0" y="0" :width="(model.svgSet ? model.svgTxtMaxWidth + 10 : 99)" :height="28 + model.fields.length * 20 + 4" />
          </g>
        </g>
      </g>
    </svg>
    <v-card id="infos" v-if="fieldInformations !== null">
      <v-card-title primary-title class="py-3">
        <div class="w-100">
          <h3 class="headline d-block w-100">{{ fieldInformations.model.model }} ({{ fieldInformations.model.count }}) <v-btn @click="fieldInformations = null" flat icon small class="ma-0 f-r"><v-icon>close</v-icon></v-btn></h3>
          <div>
            verbose_name: <b>{{ fieldInformations.model.verbose_name || 'None'  }}</b><br>
            verbose_name_plural: <b>{{ fieldInformations.model.verbose_name_plural || 'None'  }}</b><br>
            db_table: <b>{{ fieldInformations.model.db_table || 'None'  }}</b><br>
          </div>
          <h3 class="mt-2">{{ fieldInformations.field.field_name }}</h3>
          <div>
            verbose_name: <b>{{ fieldInformations.field.verbose_name || 'None' }}</b><br>
            internal_type: <b>{{ fieldInformations.field.internal_type || 'None' }}</b><br>
            blank: <b>{{ fieldInformations.field.blank || 'False' }}</b><br>
            null: <b>{{ fieldInformations.field.null || 'False' }}</b><br>
            pk: <b>{{ fieldInformations.field.pk || 'None' }}</b><br>
            related_db_table: <b>{{ fieldInformations.field.related_db_table || 'None' }}</b><br>
            <template v-if="fieldInformations.field.related_db_table">
              related_name: <b>{{ fieldInformations.field.related_name || 'None' }}</b><br>
              related_db_table_count: <b>{{ fieldInformations.field.related_db_table_count || 'None' }}</b><br>
              related_db_table_count_related: <b>{{ fieldInformations.field.related_db_table_count_related || 'None' }}</b><br>
            </template>
          </div>
        </div>
      </v-card-title>
    </v-card>
  </div>
</template>

<script>
export default {
  name: 'HcbDiagram',
  props: ['dbModels'],
  data () {
    return {
      foreignKeyLinks: [],
      posX: 0,
      posY: 0,
      scale: 1.0,
      dragObj: null,
      dragOffsetX: 0,
      dragOffsetY: 0,
      fieldInformations: null
    }
  },
  mounted () {
    console.log(this.dbModels)
    this.$nextTick(() => this.updateSvgData())
  },
  methods: {
    updateSvgData () {
      this.scale = 1.0
      this.updateSvgDataWidth()
      this.$nextTick(() => this.updateSvgDataModel())
    },
    updateSvgDataWidth () {
      this.$refs.modelTitleTxt.forEach((modelTitleRef, key) => {
        let aMaxWidth = modelTitleRef.getBBox().width
        if (!this.dbModels[key].svgTxtMaxWidth || this.dbModels[key].svgTxtMaxWidth < aMaxWidth) {
          this.$set(this.dbModels[key], 'svgTxtMaxWidth', aMaxWidth)
        }
        this.$refs['modelFieldTxt' + key].forEach((modelFieldRef, sKey) => {
          let aMaxWidth2 = modelFieldRef.getBBox().width
          if (!this.dbModels[key].svgTxtMaxWidth || this.dbModels[key].svgTxtMaxWidth < aMaxWidth2) {
            this.$set(this.dbModels[key], 'svgTxtMaxWidth', aMaxWidth2)
          }
        }, this)
        this.$set(this.dbModels[key], 'svgSet', true)
      }, this)
    },
    updateSvgDataModel () {
      this.$refs.modelGroup.forEach((modelRef, key) => {
        let modelBBox = modelRef.getBBox()
        this.$set(this.dbModels[key], 'svgWidth', modelBBox.width)
        this.$set(this.dbModels[key], 'svgHeight', modelBBox.height)
      }, this)
      this.fitWorkspace()
      this.createForeignKeyLinks()
    },
    fitWorkspace () {
      this.scale = 1.0
      this.$nextTick(() => {
        let frmSpacer = 15
        let svgBCRect = this.$refs.diagrammSVG.getBoundingClientRect()
        let svgWidth = svgBCRect.width - frmSpacer * 2
        let svgHeight = svgBCRect.height - frmSpacer * 2
        let wsBBox = this.$refs.workspace.getBBox()
        let wsWidth = wsBBox.width
        let wsHeight = wsBBox.height
        if (wsWidth > svgWidth) {
          this.scale = svgWidth / wsWidth
          wsWidth = wsWidth * this.scale
          wsHeight = wsHeight * this.scale
        }
        if (wsHeight > svgHeight) {
          this.scale = svgHeight / wsHeight
          wsWidth = wsWidth * this.scale
          wsHeight = wsHeight * this.scale
        }
        this.posX = (svgWidth - wsWidth) / 2 - (wsBBox.x * this.scale) + frmSpacer
        this.posY = (svgHeight - wsHeight) / 2 - (wsBBox.y * this.scale) + frmSpacer
      })
    },
    createForeignKeyLinks () {
      this.foreignKeyLinks = []
      this.dbModels.forEach((dbModel, key) => {
        dbModel.fields.forEach((field, key2) => {
          if (field.internal_type === 'ForeignKey') {
            let fromModelKey = this.getModelKeyByDbTableName(field.related_db_table)
            this.foreignKeyLinks.push({
              toModelKey: key,
              toModel: dbModel,
              toFieldKey: key2,
              toField: field,
              fromModelKey: fromModelKey,
              fromModel: this.dbModels[fromModelKey]
            })
          }
        }, this)
      }, this)
      console.log(this.foreignKeyLinks)
    },
    getPathForeignKeyLinks (fkLink) {
      let startPointX = fkLink.fromModel.xt + fkLink.fromModel.svgWidth / 2
      let startPointY = fkLink.fromModel.yt + fkLink.fromModel.svgHeight / 2
      let endPointX = fkLink.toModel.xt + fkLink.toModel.svgWidth / 2
      let endPointY = fkLink.toModel.yt + fkLink.toModel.svgHeight / 2
      let mX = startPointX + (endPointX - startPointX) / 2
      let path = 'M'
      path += startPointX + ' '
      path += startPointY
      path += 'L' + mX + ' ' + startPointY
      path += 'L' + mX + ' ' + endPointY
      path += 'L' + endPointX + ' ' + endPointY
      return path
    },
    getModelKeyByDbTableName (dbTableName) {
      let foundDbModelKey = null
      this.dbModels.some((dbModel, key) => {
        if (dbModel.db_table === dbTableName) {
          foundDbModelKey = key
          return true
        }
      }, this)
      return foundDbModelKey
    },
    getTitle (d) {
      var o = ''
      for (var p in d) {
        o = o + p + ' = "' + d[p] + '"<br>'
      }
      return o
    },
    startDrag (e) {
      if (e.target === this.$refs.diagrammSVG) {
        e.preventDefault()
        this.dragObj = -1
        this.dragOffsetX = e.clientX - this.posX
        this.dragOffsetY = e.clientY - this.posY
      } else if (this.$refs.modelTitleRect && this.$refs.modelTitleRect.indexOf(e.target) > -1) {
        e.preventDefault()
        this.dragObj = this.$refs.modelTitleRect.indexOf(e.target)
        this.dragOffsetX = e.clientX / this.scale - this.dbModels[this.dragObj].xt
        this.dragOffsetY = e.clientY / this.scale - this.dbModels[this.dragObj].yt
      }
    },
    drag (e) {
      if (this.dragObj !== null) {
        e.preventDefault()
        if (this.dragObj === -1) {
          this.posX = e.clientX - this.dragOffsetX
          this.posY = e.clientY - this.dragOffsetY
        } else {
          this.dbModels[this.dragObj].xt = e.clientX / this.scale - this.dragOffsetX
          this.dbModels[this.dragObj].yt = e.clientY / this.scale - this.dragOffsetY
        }
      }
    },
    endDrag (e) {
      if (this.dragObj !== null) {
        e.preventDefault()
        this.dragObj = null
      }
    }
  }
}
</script>

<style scoped>
  #diagrammframe {
    height: 100%;
    position: relative;
  }
  #infos {
    position: absolute;
    right: 10px;
    bottom: 10px;
    min-width: 20vw;
    min-height: 25vh;
  }
  #diagrammsvg {
    width: 100%;
    height: 100%;
  }
  #diagrammsvg text {
    pointer-events: none;
  }
  .svg-g-db-model > rect.bg {
    fill: #fff;
  }
  .svg-g-db-model > rect.frm {
    fill: transparent;
    stroke: #bbb;
    stroke-width: 1;
    pointer-events: none;
  }
  .svg-g-db-model:hover > rect.frm {
    stroke: #666;
  }
  .db-model-title {
    cursor: all-scroll;
  }
  .db-model-title > rect {
    fill: #aaa;
    opacity: 0.33;
  }
  .db-model-title:hover > rect {
    opacity: 1;
  }
  .svg-g-db-model:hover > .db-model-title > rect {
    fill: #aaf;
  }
  .db-model-title > text {
    font-size: 16px;
    font-weight: bold;
    dominant-baseline: text-before-edge;
  }
  .db-model-field > rect {
    fill: transparent;
    cursor: pointer;
  }
  .db-model-field:hover > rect {
    fill: #eee;
  }
  .db-model-field.showInfo > rect {
    fill: #eef;
  }
  .db-model-field.showInfo:hover > rect {
    fill: #ddf;
  }
  .db-model-field > text {
    font-size: 14px;
    dominant-baseline: text-before-edge;
  }
  .db-model-field.pk > text {
    font-weight: bold;
  }
  .svg-g-db-fk-link > path {
    stroke: #333;
    stroke-width: 5px;
    fill: none;
    stroke-opacity: 0.3;
  }
</style>
