<template>
  <v-layout row class="lvtv-main">
    <v-flex xs12 md2>
      <DBFormSelect
        :tabledata="tableData"
        :user="user"
        :options="options"
        :csrf="csrf"
        :contentID="contentID"
        @loadcontent="loadContent"
        v-if="!loading && tableData.data"
      />
    </v-flex>
    <v-flex xs12 md10>
      <div class="pa-4" v-if="variableVariantData.data">
        <h2>{{ variableVariantData.data.variable.str }}</h2>
        <div class="pb-3">
          {{ variableVariantData.data.variable.comment }}
        </div>
        <h3>
          Variants ({{ variableVariantData.data.variants.length }}):
          <v-btn title="Export list as XLSX" color="info" icon flat @click="exportXls" :disabled="variableVariantData.data.variants.length < 1"><v-icon>mdi-file-excel-outline</v-icon></v-btn>
          <span></span>
        </h3>
        <template v-if="variableVariantData.data.variants.length > 0">
          <v-data-table
            :headers="[
              {value: 'id', text: 'Id', right: true, compact: true},
              {value: 'variant', text: 'Variant'},
              {value: 'group', text: 'Group'},
              {value: 'comment', text: 'Comment'},
              {value: 'infCount', text: 'Inf', title: 'Informant Count', right: true, compact: true},
              {value: 'infDistCount', text: 'Dist', title: 'District Count', right: true, compact: true},
              {value: 'infBelongCount', text: 'Bel', title: 'Belong to Count', right: true, compact: true}
            ]"
            :items="variableVariantData.data.variants"
            :pagination.sync="pagination"
            v-model="selectedVariants"
            select-all
            class="elevation-1 mt-3"
          >
            <template v-slot:headers="props">
              <tr>
                <th class="px-3" width="10">
                  <v-checkbox
                    :input-value="props.all"
                    :indeterminate="props.indeterminate"
                    primary
                    hide-details
                    @click.stop="toggleAll"
                  ></v-checkbox>
                </th>
                <th
                  v-for="header in props.headers"
                  :key="header.text"
                  :class="[
                    'column sortable',
                    pagination.descending ? 'desc' : 'asc',
                    header.value === pagination.sortBy ? 'active' : '',
                    header.right ? 'text-xs-right' : '',
                    header.compact ? 'px-3' : ''
                  ]"
                  style="text-align: left;"
                  :title="header.title"
                  @click="changeSort(header.value)"
                >
                  <template v-if="header.right">
                    <v-icon small>arrow_upward</v-icon>
                    {{ header.text }}
                  </template>
                  <template v-else>
                    {{ header.text }}
                    <v-icon small>arrow_upward</v-icon>
                  </template>
                </th>
              </tr>
            </template>
            <template v-slot:items="props">
              <tr :active="props.selected" @click="props.selected = !props.selected">
                <td class="px-3">
                  <v-checkbox :input-value="props.selected" primary hide-details></v-checkbox>
                </td>
                <td class="text-xs-right px-3" width="10">{{ props.item.id }}</td>
                <td>{{ props.item.variant }}</td>
                <td>
                  <template v-if="props.item.group && props.item.group.length > 0">
                    <span class="group" v-for="group in props.item.group" :key="group.id" :title="'ID: ' + group.id + '\ngID: ' + (group.group ? group.group.id : 'Err')">
                      <template v-if="group.group">
                        {{ group.group.name }}
                      </template>
                      <b v-else>
                        Error (Delete me!)
                      </b>
                      <v-icon small @click.stop="deleteGroupAssignation(group.id)">delete</v-icon>
                    </span>
                  </template>
                  <template v-else>
                    No group assigned
                  </template>
                </td>
                <td>{{ props.item.comment }}</td>
                <td class="text-xs-right px-3" width="10">{{ props.item.infCount }}</td>
                <td class="text-xs-right px-3" width="10">{{ props.item.infDistCount }}</td>
                <td class="text-xs-right px-3" width="10">{{ props.item.infBelongCount }}</td>
              </tr>
            </template>
          </v-data-table>
          <template v-if="selectedVariants.length > 0">
            <v-layout row class="mt-3">
              <v-flex xs12 md3 align-self-center>
                <ForeignKey
                  :csrf="csrf"
                  :field="{field_name: 'group'}"
                  :edit="true"
                  :values="selectedGroup"
                  :value="selectedGroup.group.val"
                  :fieldTitle="'Select variant group'"
                  :orgField="{related_model: 'lex_variantgroup', related_db_table_count: 999, internal_type: 'table'}"
                  :filter="['lex_variable', contentID]"
                  :needValue="false"
                />
              </v-flex>
              <template v-if="selectedGroup.group.val === -1">
                <v-flex xs12 md7 align-self-center>
                  <v-text-field label="Name" v-model="newGroupName"></v-text-field>
                </v-flex>
              </template>
              <v-flex xs12 md2 align-self-center>
                <v-btn color="info" @click="saveGroup" :disabled="!(selectedGroup.group.val > 0 || (selectedGroup.group.val === -1 && newGroupName.trim().length > 1))">Save</v-btn>
              </v-flex>
            </v-layout>
            <div class="mt-1">
              {{ selectedVariants.length }} variant{{ selectedVariants.length > 1 ? 's' : '' }} selected: {{ selectedVariants.map(v => v.str).join(', ') }}
            </div>
          </template>
        </template>
      </div>
      <div class="pa-4" v-else>
        {{ contentID > 0 ? 'Loading ...' : 'Select Variant!' }}<br>
        <v-btn @click="fxUpdate" small v-if="contentID < 1" class="mt-5 mx-0">fx update</v-btn>
      </div>
    </v-flex>
    <v-dialog v-model="loadingVariant" persistent width="300">
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
import DBFormSelect from '../components/DBForm/DBFormSelect.vue'
import ForeignKey from '../components/DBForm/DBFormContentField/ForeignKey.vue'
const ExcelJS = require('exceljs')

export default {
  name: 'AssignmentVariantgroups',
  props: ['user', 'options', 'csrf'],
  data () {
    return {
      loading: false,
      tableData: { data: null },
      contentID: 0,
      loadingVariant: false,
      variableVariantData: { data: null },
      selectedVariants: [],
      newGroupName: '',
      selectedGroup: {
        group: {
          val: -1,
          nVal: -1,
          str: 'New group'
        }
      },
      pagination: {
        sortBy: 'variant',
        rowsPerPage: 10
      }
    }
  },
  mounted () {
    console.log('AssignmentVariantgroups mounted ...')
    this.getTable()
  },
  methods: {
    exportXls () {
      let aTime = new Date()
      let aDateTime = aTime.toLocaleString('en-US')
      const wb = new ExcelJS.Workbook()
      wb.title = 'Variable/Variants'
      wb.subject = 'Variants'
      wb.creator = 'lasDB'
      wb.created = aTime
      var ws
      ws = wb.addWorksheet('Variants')
      ws.addRow([this.variableVariantData.data.variable.str])
      if (this.variableVariantData.data.variable.comment) {
        ws.addRow([this.variableVariantData.data.variable.comment])
      }
      ws.addRow([aDateTime])
      ws.addRow()
      let aRow = ws.addRow(['Id', 'Variant', 'Group', 'Comment', 'Informant Count', 'District Count', 'Belong to Count'])
      ws.columns = [
        { key: 'id', width: 5 },
        { key: 'variant', width: 20 },
        { key: 'group', width: 30 },
        { key: 'comment', width: 30 },
        { key: 'infCount', width: 10 },
        { key: 'infDistCount', width: 10 },
        { key: 'infBelongCount', width: 10 }
      ]
      aRow.style = { font: { bold: true } }
      aRow.border = { bottom: { style: 'medium' } }
      aRow.eachCell(c => {
        c.style = { font: { bold: true } }
        c.border = { bottom: { style: 'medium' } }
      })
      this.variableVariantData.data.variants.forEach(dRow => {
        ws.addRow([
          dRow.id,
          dRow.variant,
          dRow.group ? dRow.group.map(gRow => gRow.group.name + ' (' + gRow.group.id + ')').join(', ') : null,
          dRow.comment,
          dRow.infCount,
          dRow.infDistCount,
          dRow.infBelongCount
        ])
      })
      wb.xlsx.writeBuffer().then(this.saveFile.bind(null, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'xlsx', 'lasdb_vv_' + this.variableVariantData.data.variable.id + '_' + aTime.getFullYear() + '-' + ('0' + aTime.getMonth()).slice(-2) + '-' + ('0' + aTime.getDay()).slice(-2) + '_' + ('0' + aTime.getHours()).slice(-2) + '-' + ('0' + aTime.getMinutes()).slice(-2) + '-' + ('0' + aTime.getSeconds()).slice(-2)))
    },
    saveFile (mimeType, aFileType, aFilename, buffer) {
      if (buffer) {
        // console.log(buffer)
        if (buffer) {
          let blob = new Blob([buffer], {type: mimeType})
          const a = document.createElement('a')
          a.href = URL.createObjectURL(blob)
          a.download = aFilename + '.' + aFileType
          a.click()
        }
      } else {
        alert('Error on creating file!')
      }
    },
    deleteGroupAssignation (id) {
      console.log('deleteGroupAssignation', id)
      if (confirm('Really delete assignment?')) {
        this.loadingVariant = true
        this.$http
          .post('/variantgroups/', {
            del: 'delVariantgroup',
            id: id
          }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
          .then((response) => {
            console.log('deleteGroupAssignation', response.data)
            this.loadingVariant = false
            this.getVariantByVariable(false)
          })
          .catch((err) => {
            console.log(err)
            alert('Error while saving!')
            this.loadingVariant = false
          })
      }
    },
    saveGroup () {
      console.log('saveGroup', this.selectedGroup.group.val, this.newGroupName.trim())
      if (this.selectedGroup.group.val > 0 || (this.selectedGroup.group.val === -1 && this.newGroupName.trim().length > 0)) {
        this.loadingVariant = true
        this.$http
          .post('/variantgroups/', {
            set: 'setVariantgroup',
            variableID: this.contentID,
            variantIDs: JSON.stringify(this.selectedVariants.map(v => v.id)),
            groupID: this.selectedGroup.group.val,
            name: this.selectedGroup.group.val === -1 ? this.newGroupName.trim() : null
          }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
          .then((response) => {
            console.log('setVariantgroup', response.data)
            if (response.data.warnings && response.data.warnings.length > 0) {
              alert('Warnings:\n' + response.data.warnings.join('\n'))
            }
            this.loadingVariant = false
            this.getVariantByVariable()
          })
          .catch((err) => {
            console.log(err)
            alert('Error while saving!')
            this.loadingVariant = false
          })
      } else {
        alert('Not saved!!')
      }
      this.selectedVariants = []
      this.newGroupName = ''
    },
    fxUpdate () {
      console.log('fxUpdate')
      this.loading = true
      this.$http
        .post('/variantgroups/', {
          update: 'variantgroups'
        }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
        .then((response) => {
          console.log('fxUpdate', response.data)
          this.loading = false
        })
        .catch((err) => {
          console.log(err)
          alert('Error while saving!')
          this.loading = false
        })
    },
    loadContent (aId) {
      this.contentID = 0
      this.$nextTick(() => { this.contentID = aId })
    },
    getTable () {
      this.loading = true
      this.$http
        .post('/form/', {
          get: 'getTable',
          getModel: 'lex_variable',
          getOptions: ''
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
    getVariantByVariable (clean = true) {
      if (this.contentID > 0) {
        this.loadingVariant = true
        if (clean) {
          this.selectedGroup = {
            group: {
              val: -1,
              nVal: -1,
              str: 'New group'
            }
          }
          this.newGroupName = ''
          this.variableVariantData = { data: null }
        }
        this.$http
          .post('/variantgroups/', {
            get: 'getVariantByVariable',
            variableID: this.contentID
          }, {headers: {'X-CSRFToken': this.csrf}, emulateJSON: true})
          .then((response) => {
            console.log('getVariantByVariable', response.data)
            this.$set(this.variableVariantData, 'data', response.data)
            this.loadingVariant = false
          })
          .catch((err) => {
            console.log(err)
            this.loadingVariant = false
          })
      }
    },
    toggleAll () {
      if (this.selectedVariants.length) this.selectedVariants = []
      else this.selectedVariants = this.variableVariantData.data.variants.slice()
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
  watch: {
    contentID () {
      if (this.contentID > 0) {
        this.pagination.page = 1
        this.selectedVariants = []
        this.getVariantByVariable()
      }
    }
  },
  components: {
    DBFormSelect,
    ForeignKey
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
</style>
