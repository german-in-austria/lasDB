<template>
  <v-layout row class="lvtv-main">
    <v-flex xs12 md2>
      <DBFormSelect ref="dbformselect"
        :tabledata="tableData"
        :user="user"
        :options="options"
        :csrf="csrf"
        :contentID="contentID"
        @loadcontent="loadContent"
        v-if="!loading && tableData.data" />
    </v-flex>
    <v-flex xs12 md10>
      <div class="pa-4 h-100 p-relative" v-if="contentID !== 0 && !update">
        <template v-if="mapData && contentID > 0 && !editMap">
          <v-btn @click="contentID = 0" flat fab small style="position:absolute;right:0px;top:0px;width:20px;height:20px;"><v-icon>mdi-close</v-icon></v-btn>
          <h1>
            {{ mapData.values.name.val }} (ID: {{ mapData.values.id.val }}) {{ mapData.values.public.val ? ' Public!' : ''}}
            <v-btn @click="editMap = true" color="primary" fab small dark><v-icon>edit</v-icon></v-btn>
          </h1>
          <h2 class="mt-1" v-if="mapData.values.title.val">{{ mapData.values.title.val }}</h2>
          <h3 class="mt-1" v-if="mapData.values.legend_title.val">{{ mapData.values.legend_title.val }}</h3>
          <div class="mt-2" v-if="mapData.values.comment.val">
            <b>Comment:</b>
            <div v-html="nl2br(mapData.values.comment.val)" />
          </div>
          <div class="mt-2" v-if="mapData.values.description.val">
            <b>Description:</b>
            <div v-html="nl2br(mapData.values.description.val)" />
          </div>
          <v-layout row class="mt-3">
            <v-flex xs12 md3 align-self-center>
              <ForeignKey
                ref="variable"
                :csrf="csrf"
                :field="{field_name: 'variable'}"
                :edit="true"
                :values="selectedVariable"
                :value="selectedVariable.variable.val"
                :fieldTitle="'Select variable'"
                :orgField="{related_model: 'lex_variable', related_db_table_count: 999, internal_type: 'table'}"
                :needValue="false"
              />
            </v-flex>
            <v-flex xs12 md3 align-self-center>
              <ForeignKey
                :csrf="csrf"
                :field="{field_name: 'group'}"
                :edit="true"
                :values="selectedGroup"
                :value="selectedGroup.group.val"
                :fieldTitle="'Select variant group'"
                :orgField="{related_model: 'lex_variantgroup', related_db_table_count: 999, internal_type: 'table'}"
                :filter="selectedVariable.variable.val > 0 ? ['lex_variable', selectedVariable.variable.val] : null"
                :needValue="false"
              />
            </v-flex>
              <!-- {{ selectedVariable.variable.val > 0 ? ['lex_variable', selectedVariable.variable.val] : null }} -->
            <v-flex xs12 md2 align-self-center>
              <v-btn color="info" @click="addMapToVariantgroup(selectedGroup.group.val)" :disabled="!(selectedGroup && selectedGroup.group && selectedGroup.group.val > 0)">Add variant group</v-btn>
            </v-flex>
          </v-layout>
          <div class="py-3" v-if="sortedMapToVariantgroupData">
            <v-data-table
              :headers="[
                {value: 'order', text: '#', right: true, compact: true},
                {value: 'id', text: 'Id', right: true, compact: true},
                {value: 'variantgroup', text: 'Group', notsortable: true},
                {value: 'preset_color', text: 'Color'},
                {value: '', text: 'Tools', right: true},
              ]"
              :items="sortedMapToVariantgroupData"
              :pagination.sync="pagination"
              class="nooverflow elevation-1 mt-3"
            >
              <template v-slot:headers="props">
                <tr>
                  <th
                    v-for="header in props.headers"
                    :key="header.text"
                    :class="[
                      'column',
                      header.right ? 'text-xs-right' : '',
                      header.compact ? 'px-3' : ''
                    ]"
                    style="text-align: left;"
                    :title="header.title"
                  >
                    {{ header.text }}
                  </th>
                </tr>
              </template>
              <template v-slot:items="props">
                <tr :style="props.item.delete ? 'background-color:#f99;' : ''">
                  <td class="text-xs-right px-3" width="10">{{ props.item.order }}</td>
                  <td class="text-xs-right px-3" width="10">{{ props.item.id }}</td>
                  <td
                    :title="'variable: ' + props.item.variantgroup.lexVariableStr + ' (id: ' + props.item.variantgroup.lexVariable + ')'"
                    :style="
                      (!props.item.variantgroup.lexVariable ? 'font-style: italic; color: gray;' : '')
                      + (props.item.variantgroup.lexVariable && selectedVariable.variable.val !== props.item.variantgroup.lexVariable ? 'font-weight: bold; color: red;' : '')
                    "
                  >
                    {{ props.item.variantgroup.name }} - {{ props.item.variantgroup.lexVariableStr }}
                  </td>
                  <td>
                    <verte @close="changedMapToVariantgroupData" picker="square" model="hex" :draggable="false" :enableAlpha="false" :colorHistory.sync="colorHistory" menuPosition="top" class="d-inline-flex" v-model="props.item.preset_color" />
                    <span class="preset-color">{{ props.item.preset_color }}</span>
                  </td>
                  <td class="text-xs-right">
                    <template v-if="!props.item.delete">
                      <v-btn @click="deleteMapToVariantgroup(props.item)" color="red" icon flat small><v-icon>delete_forever</v-icon></v-btn>
                      <v-btn @click="moveMapToVariantgroup(props.item, -1.5)" icon flat small class="mx-1" :disabled="props.index === 0"><v-icon>mdi-chevron-up</v-icon></v-btn>
                      <v-btn @click="moveMapToVariantgroup(props.item, 1.5)" icon flat small class="ml-0 mr-1" :disabled="props.index === sortedMapToVariantgroupData.length - 1"><v-icon>mdi-chevron-down</v-icon></v-btn>
                    </template>
                  </td>
                </tr>
              </template>
            </v-data-table>
          </div>
        </template>
        <template v-else-if="contentID === -1 || editMap">
          <DBFormContent ref="dbformcontent"
            :tabledata="tableData"
            :user="user"
            :options="options"
            :csrf="csrf"
            :contentID="contentID"
            :startEdit="true"
            @contentUpdated="contentUpdated"
            @close="contentID === -1 ? contentID = 0 : editMap = false"
            v-if="!loading && tableData.data && contentID"
          />
        </template>
        <template v-else>
          Loading ... id: {{ contentID }}
        </template>
      </div>
      <div class="pa-4" v-else>
        <v-btn @click="contentID = -1" color="primary" class="pl-2"><v-icon>mdi-plus</v-icon> New Entrie</v-btn>
        <p class="mt-1 ml-3">or select Map!</p>
      </div>
    </v-flex>
    <v-dialog v-model="loadingMap" persistent width="300">
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
import _ from 'lodash'
import verte from 'verte'
import 'verte/dist/verte.css'
import DBFormSelect from '../components/DBForm/DBFormSelect.vue'
import DBFormContent from '../components/DBForm/DBFormContent.vue'
import ForeignKey from '../components/DBForm/DBFormContentField/ForeignKey.vue'

export default {
  name: 'MapVariantgroups',
  props: ['user', 'options', 'csrf'],
  data () {
    return {
      loading: false,
      update: false,
      tableData: { data: null },
      contentID: 0,
      loadingMap: false,
      mapData: null,
      editMap: false,
      mapToVariantgroupData: null,
      pagination: {
        sortBy: 'variant',
        rowsPerPage: 25
      },
      colorHistory: [],
      selectedVariable: {
        variable: {
          val: null,
          nVal: -1,
          str: 'empty'
        }
      },
      selectedGroup: {
        group: {
          val: null,
          nVal: -1,
          str: 'empty'
        }
      }
    }
  },
  mounted () {
    console.log('MapVariantgroups mounted ...')
    this.getTable()
  },
  methods: {
    loadContent (aId) {
      this.contentID = 0
      this.$nextTick(() => { this.contentID = aId })
    },
    getTable () {
      this.loading = true
      this.$http
        .post('/form/', {
          get: 'getTable',
          getModel: 'map',
          getOptions: 'map'
        }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
        .then((response) => {
          console.log('getTable', response.data)
          this.tableData.data = response.data
          this.loading = false
        })
        .catch((err) => {
          console.log(err)
          this.loading = false
        })
    },
    getMap () {
      console.log('getMap')
      this.loadingMap = true
      this.$http
        .post('/form/', {
          get: 'getContent',
          getValues: true,
          app: 'db',
          model: 'map',
          pk: this.contentID
        }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
        .then((response) => {
          console.log(response.data)
          this.mapData = response.data
          this.loadingMap = false
          this.GetMapToVariantgroupData()
        })
        .catch((err) => {
          console.log(err)
          this.loadingMap = false
        })
    },
    GetMapToVariantgroupData () {
      console.log('GetMapToVariantgroupData')
      this.loadingMap = true
      this.$http
        .post('/maptovariantgroups/', {
          get: 'getMapToVariantgroupData',
          mapID: this.contentID
        }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
        .then((response) => {
          console.log(response.data)
          let dg = 0
          response.data.map_to_variantgroup.forEach(mvg => {
            if (!mvg.preset_color) {
              let rCol = Math.floor(Math.random() * 16777215).toString(16)
              while (rCol.length < 6) {
                rCol = '0' + rCol
              }
              mvg.preset_color = '#' + rCol
              this.changedMapToVariantgroupData()
            }
            if (mvg.order !== dg) {
              mvg.order = dg
              this.changedMapToVariantgroupData()
            }
            dg++
          })
          this.mapToVariantgroupData = response.data
          if (this.mapToVariantgroupData && this.mapToVariantgroupData.map_to_variantgroup && this.mapToVariantgroupData.map_to_variantgroup[0] && this.mapToVariantgroupData.map_to_variantgroup[0].variantgroup && this.mapToVariantgroupData.map_to_variantgroup[0].variantgroup.lexVariable) {
            this.$refs.variable.selectByVal(this.mapToVariantgroupData.map_to_variantgroup[0].variantgroup.lexVariable)
          }
          this.loadingMap = false
        })
        .catch((err) => {
          console.log(err)
          this.loadingMap = false
        })
    },
    addMapToVariantgroup (gId) {
      console.log('addMapToVariantgroup', gId)
      let rCol = Math.floor(Math.random() * 16777215).toString(16)
      while (rCol.length < 6) {
        rCol = '0' + rCol
      }
      this.mapToVariantgroupData.map_to_variantgroup.push({
        id: -1,
        order: 99999999,
        preset_color: '#' + rCol,
        variantgroup: {
          id: gId,
          name: 'Added now ... (ID: ' + gId + ')'
        }
      })
      let dg = 0
      this.sortedMapToVariantgroupData.forEach(mtv => {
        mtv.order = dg++
      })
      this.changedMapToVariantgroupData()
    },
    deleteMapToVariantgroup (mtvObj) {
      console.log('deleteMapToVariantgroup', mtvObj)
      if (confirm('Are you sure you want to delete this element?')) {
        this.$set(mtvObj, 'delete', true)
        this.changedMapToVariantgroupData()
      }
    },
    moveMapToVariantgroup (mtvObj, add) {
      console.log('upMapToVariantgroup', mtvObj)
      mtvObj.order += add
      let dg = 0
      this.sortedMapToVariantgroupData.forEach(mtv => {
        mtv.order = dg++
      })
      this.changedMapToVariantgroupData()
    },
    changedMapToVariantgroupData: _.debounce(function () {
      console.log('changedMapToVariantgroupData')
      this.loadingMap = true
      this.$http
        .post('/maptovariantgroups/', {
          set: 'setMapToVariantgroupData',
          mapID: this.contentID,
          mtvObjs: JSON.stringify(this.sortedMapToVariantgroupData)
        }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
        .then((response) => {
          console.log(response.data)
          this.loadingMap = false
          this.GetMapToVariantgroupData()
        })
        .catch((err) => {
          console.log(err)
          this.loadingMap = false
          alert('Saving Error!')
        })
    }, 150),
    contentUpdated (id, sortFieldValue, oldSortFieldValue) {
      this.$refs.dbformselect.contentUpdated(id, sortFieldValue, oldSortFieldValue, id !== this.contentID)
      if (id > 0) {
        this.loadContent(id)
      } else {
        this.contentID = 0
      }
    },
    nl2br (t) {
      return t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/(?:\r\n|\r|\n)/g, '<br />')
    },
    changeSort (column) {
      if (this.pagination.sortBy === column) {
        this.pagination.descending = !this.pagination.descending
      } else {
        this.pagination.sortBy = column
        this.pagination.descending = false
      }
    }
  },
  computed: {
    sortedMapToVariantgroupData () {
      return this.mapToVariantgroupData && this.mapToVariantgroupData.map_to_variantgroup && this.mapToVariantgroupData.map_to_variantgroup.slice().sort((a, b) => { return a.order < b.order ? -1 : (a.order > b.order ? 1 : 0) })
    }
  },
  watch: {
    contentID () {
      if (this.contentID > 0) {
        this.editMap = false
        this.pagination.page = 1
        this.getMap()
        this.update = true
        this.selectedVariable = {
          variable: {
            val: null,
            nVal: -1,
            str: 'empty'
          }
        }
        this.selectedGroup = {
          group: {
            val: null,
            nVal: -1,
            str: 'empty'
          }
        }
      }
    },
    editMap () {
      if (!this.editMap && this.contentID > 0) {
        this.pagination.page = 1
        this.getMap()
      }
    },
    update (nVal) {
      if (nVal) {
        this.$nextTick(() => {
          this.update = false
        })
      }
    }
  },
  components: {
    DBFormSelect,
    DBFormContent,
    ForeignKey,
    verte
  }
}
</script>

<style scoped>
.lvtv-main {
  border: 1px solid #ddd;
  height: 100%;
}
span.group {
  border-radius: 3px;
  border: 1px solid #bbb;
  padding: 0.1rem 0.25rem;
  margin-right: 0.25rem;
}
span.group:hover {
  border-color: #fbb;
  color: #f00;
}
span.group:hover >>> .v-icon {
  color: #f00;
}
.preset-color {
  margin-left: 10px;
  position: relative;
  top: -7px;
}
.nooverflow >>> .v-table__overflow {
  overflow: visible!important;
}
</style>
